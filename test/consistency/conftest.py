"""
Pytest configuration and fixtures for API consistency testing.
"""

import importlib
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest


@dataclass
class MethodSignature:
    """Represents a method signature for comparison."""

    name: str
    parameters: Dict[str, Any]
    return_annotation: Any
    is_async: bool
    docstring: Optional[str] = None


@dataclass
class APIClassInfo:
    """Information about an API class."""

    name: str
    module_path: str
    methods: Dict[str, MethodSignature]
    is_async: bool


class APIDiscovery:
    """Discovers and analyzes API classes."""

    def __init__(self, base_path: str = "src/evo_client"):
        self.base_path = Path(base_path)

    def discover_api_classes(self, module_type: str) -> Dict[str, APIClassInfo]:
        """
        Discover all API classes in a module type (sync or aio).

        Args:
            module_type: Either 'sync' or 'aio'

        Returns:
            Dictionary mapping class names to APIClassInfo objects
        """
        classes = {}
        api_path = self.base_path / module_type / "api"

        if not api_path.exists():
            return classes

        # Import the module
        module_name = f"evo_client.{module_type}.api"

        try:
            # Get all Python files in the API directory
            for file_path in api_path.glob("*.py"):
                if file_path.name.startswith("__"):
                    continue

                module_file = file_path.stem
                full_module_name = f"{module_name}.{module_file}"

                try:
                    module = importlib.import_module(full_module_name)
                    api_classes = self._extract_api_classes(
                        module, module_type == "aio"
                    )
                    classes.update(api_classes)
                except ImportError as e:
                    print(f"Warning: Could not import {full_module_name}: {e}")
                    continue

        except Exception as e:
            print(f"Error discovering API classes: {e}")

        return classes

    def _extract_api_classes(
        self, module: Any, is_async: bool
    ) -> Dict[str, APIClassInfo]:
        """Extract API classes from a module."""
        classes = {}

        for name, obj in inspect.getmembers(module, inspect.isclass):
            # Skip imported classes and non-API classes
            if obj.__module__ != module.__name__:
                continue

            # Check if it's an API class (ends with Api)
            if not name.endswith("Api"):
                continue

            # Extract methods
            methods = self._extract_methods(obj)

            class_info = APIClassInfo(
                name=name,
                module_path=module.__name__,
                methods=methods,
                is_async=is_async,
            )

            classes[name] = class_info

        return classes

    def _extract_methods(self, cls: type) -> Dict[str, MethodSignature]:
        """Extract public methods from a class."""
        methods = {}

        for name, method in inspect.getmembers(cls, inspect.isfunction):
            # Skip private methods and inherited methods
            if name.startswith("_") or name in ["__init__", "__new__"]:
                continue

            # Get method signature
            try:
                sig = inspect.signature(method)
                is_async = inspect.iscoroutinefunction(method)

                # Extract parameter information
                parameters = {}
                for param_name, param in sig.parameters.items():
                    if param_name == "self":
                        continue

                    parameters[param_name] = {
                        "annotation": param.annotation,
                        "default": param.default,
                        "kind": param.kind.name,
                    }

                method_sig = MethodSignature(
                    name=name,
                    parameters=parameters,
                    return_annotation=sig.return_annotation,
                    is_async=is_async,
                    docstring=inspect.getdoc(method),
                )

                methods[name] = method_sig

            except Exception as e:
                print(
                    f"Warning: Could not extract signature for {cls.__name__}.{name}: {e}"
                )

        return methods


class APIConsistencyValidator:
    """Validates consistency between sync and async APIs."""

    def __init__(self):
        self.discovery = APIDiscovery()

    def validate_api_consistency(self) -> Dict[str, Any]:
        """
        Validate consistency between sync and async APIs.

        Returns:
            Dictionary containing validation results
        """
        sync_classes = self.discovery.discover_api_classes("sync")
        async_classes = self.discovery.discover_api_classes("aio")

        results = {
            "sync_classes": list(sync_classes.keys()),
            "async_classes": list(async_classes.keys()),
            "missing_in_sync": [],
            "missing_in_async": [],
            "signature_mismatches": [],
            "consistent_classes": [],
            "total_issues": 0,
        }

        # Find missing classes
        sync_names = set(sync_classes.keys())
        async_names = set(async_classes.keys())

        # Convert class names for comparison (AsyncMembersApi <-> SyncMembersApi)
        sync_base_names = {self._get_base_name(name): name for name in sync_names}
        async_base_names = {self._get_base_name(name): name for name in async_names}

        # Find missing classes
        for base_name in sync_base_names:
            if base_name not in async_base_names:
                results["missing_in_async"].append(sync_base_names[base_name])

        for base_name in async_base_names:
            if base_name not in sync_base_names:
                results["missing_in_sync"].append(async_base_names[base_name])

        # Compare methods for common classes
        common_base_names = set(sync_base_names.keys()) & set(async_base_names.keys())

        for base_name in common_base_names:
            sync_class = sync_classes[sync_base_names[base_name]]
            async_class = async_classes[async_base_names[base_name]]

            method_comparison = self._compare_class_methods(sync_class, async_class)

            if method_comparison["issues"]:
                results["signature_mismatches"].append(
                    {
                        "sync_class": sync_class.name,
                        "async_class": async_class.name,
                        "issues": method_comparison["issues"],
                    }
                )
            else:
                results["consistent_classes"].append(
                    {
                        "sync_class": sync_class.name,
                        "async_class": async_class.name,
                        "method_count": len(sync_class.methods),
                    }
                )

        # Calculate total issues
        results["total_issues"] = (
            len(results["missing_in_sync"])
            + len(results["missing_in_async"])
            + len(results["signature_mismatches"])
        )

        return results

    def _get_base_name(self, class_name: str) -> str:
        """Get base name from class name (remove Sync/Async prefix)."""
        if class_name.startswith("Sync"):
            return class_name[4:]  # Remove "Sync"
        elif class_name.startswith("Async"):
            return class_name[5:]  # Remove "Async"
        return class_name

    def _compare_class_methods(
        self, sync_class: APIClassInfo, async_class: APIClassInfo
    ) -> Dict[str, Any]:
        """Compare methods between sync and async classes."""
        issues = []

        sync_methods = set(sync_class.methods.keys())
        async_methods = set(async_class.methods.keys())

        # Find missing methods
        missing_in_async = sync_methods - async_methods
        missing_in_sync = async_methods - sync_methods

        for method in missing_in_async:
            issues.append(f"Method '{method}' missing in async class")

        for method in missing_in_sync:
            issues.append(f"Method '{method}' missing in sync class")

        # Compare common methods
        common_methods = sync_methods & async_methods

        for method_name in common_methods:
            sync_method = sync_class.methods[method_name]
            async_method = async_class.methods[method_name]

            method_issues = self._compare_method_signatures(sync_method, async_method)
            issues.extend(
                [f"Method '{method_name}': {issue}" for issue in method_issues]
            )

        return {"issues": issues}

    def _compare_method_signatures(
        self, sync_method: MethodSignature, async_method: MethodSignature
    ) -> List[str]:
        """Compare signatures of sync and async methods."""
        issues = []

        # Check async/sync difference
        if sync_method.is_async:
            issues.append("Sync method should not be async")
        if not async_method.is_async:
            issues.append("Async method should be async")

        # Compare parameters
        sync_params = set(sync_method.parameters.keys())
        async_params = set(async_method.parameters.keys())

        if sync_params != async_params:
            missing_in_async = sync_params - async_params
            missing_in_sync = async_params - sync_params

            if missing_in_async:
                issues.append(f"Parameters missing in async: {missing_in_async}")
            if missing_in_sync:
                issues.append(f"Parameters missing in sync: {missing_in_sync}")

        # Compare parameter details for common parameters
        common_params = sync_params & async_params
        for param_name in common_params:
            sync_param = sync_method.parameters[param_name]
            async_param = async_method.parameters[param_name]

            # Compare annotations
            if sync_param["annotation"] != async_param["annotation"]:
                issues.append(f"Parameter '{param_name}' annotation mismatch")

            # Compare defaults
            if sync_param["default"] != async_param["default"]:
                issues.append(f"Parameter '{param_name}' default value mismatch")

        return issues


def generate_consistency_report(results: Dict[str, Any]) -> str:
    """Generate a human-readable consistency report."""
    report = []
    report.append("=" * 60)
    report.append("API CONSISTENCY REPORT")
    report.append("=" * 60)
    report.append(f"Total Issues Found: {results['total_issues']}")
    report.append("")

    # Summary
    report.append(f"Sync Classes: {len(results['sync_classes'])}")
    report.append(f"Async Classes: {len(results['async_classes'])}")
    report.append(f"Consistent Classes: {len(results['consistent_classes'])}")
    report.append("")

    # Missing classes
    if results["missing_in_sync"]:
        report.append("MISSING IN SYNC:")
        for cls in results["missing_in_sync"]:
            report.append(f"  - {cls}")
        report.append("")

    if results["missing_in_async"]:
        report.append("MISSING IN ASYNC:")
        for cls in results["missing_in_async"]:
            report.append(f"  - {cls}")
        report.append("")

    # Signature mismatches
    if results["signature_mismatches"]:
        report.append("SIGNATURE MISMATCHES:")
        for mismatch in results["signature_mismatches"]:
            report.append(f"  {mismatch['sync_class']} <-> {mismatch['async_class']}:")
            for issue in mismatch["issues"]:
                report.append(f"    - {issue}")
        report.append("")

    # Consistent classes
    if results["consistent_classes"]:
        report.append("CONSISTENT CLASSES:")
        for cls in results["consistent_classes"]:
            report.append(
                f"  - {cls['sync_class']} <-> {cls['async_class']} ({cls['method_count']} methods)"
            )

    return "\n".join(report)


# Pytest Fixtures
@pytest.fixture(scope="session")
def api_discovery():
    """Fixture providing API discovery functionality."""
    return APIDiscovery()


@pytest.fixture(scope="session")
def api_validator():
    """Fixture providing API consistency validator."""
    return APIConsistencyValidator()


@pytest.fixture(scope="session")
def sync_classes(api_discovery):
    """Fixture providing sync API classes."""
    return api_discovery.discover_api_classes("sync")


@pytest.fixture(scope="session")
def async_classes(api_discovery):
    """Fixture providing async API classes."""
    return api_discovery.discover_api_classes("aio")


@pytest.fixture(scope="session")
def consistency_results(api_validator):
    """Fixture providing API consistency validation results."""
    return api_validator.validate_api_consistency()


@pytest.fixture
def report_generator():
    """Fixture providing report generation functionality."""
    return generate_consistency_report
