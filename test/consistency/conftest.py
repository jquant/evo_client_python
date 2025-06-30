"""
Pytest configuration and fixtures for API consistency testing.
"""

import ast
import importlib
import inspect
import re
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
    api_route: Optional[str] = None  # New field for API route extraction


@dataclass
class APIClassInfo:
    """Information about an API class."""

    name: str
    module_path: str
    methods: Dict[str, MethodSignature]
    is_async: bool


class RouteExtractor:
    """Extracts API routes from method source code."""

    def extract_route_from_method(self, method_func) -> Optional[str]:
        """
        Extract the API route from a method's source code.

        Args:
            method_func: The method function to analyze

        Returns:
            The extracted API route or None if not found
        """
        try:
            source = inspect.getsource(method_func)
            return self._parse_resource_path(source)
        except (OSError, TypeError):
            # Can't get source (might be built-in or C extension)
            return None

    def _parse_resource_path(self, source_code: str) -> Optional[str]:
        """
        Parse source code to extract resource_path value.

        Args:
            source_code: The method's source code

        Returns:
            The resource path or None if not found
        """
        # Try to parse with AST first for more robust extraction
        try:
            tree = ast.parse(source_code)
            route = self._extract_route_from_ast(tree)
            if route:
                return route
        except SyntaxError:
            pass

        # Fallback to regex pattern matching
        return self._extract_route_with_regex(source_code)

    def _extract_route_from_ast(self, tree: ast.AST) -> Optional[str]:
        """Extract route using AST parsing."""

        class RouteVisitor(ast.NodeVisitor):
            def __init__(self):
                self.routes = []

            def visit_Call(self, node):
                # Look for call_api method calls
                if (
                    isinstance(node.func, ast.Attribute)
                    and node.func.attr == "call_api"
                ):

                    # Find resource_path argument
                    for keyword in node.keywords:
                        if keyword.arg == "resource_path":
                            route = self._extract_string_value(keyword.value)
                            if route:
                                self.routes.append(route)

                self.generic_visit(node)

            def _extract_string_value(self, node) -> Optional[str]:
                """Extract string value from AST node."""
                if isinstance(node, ast.Constant):
                    return str(node.value)
                elif isinstance(node, ast.JoinedStr):
                    # Handle f-strings
                    return self._reconstruct_fstring(node)
                elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
                    # Handle string concatenation
                    left = self._extract_string_value(node.left)
                    right = self._extract_string_value(node.right)
                    if left and right:
                        return left + right
                elif isinstance(node, ast.Attribute):
                    # Handle self.base_path style references
                    return self._extract_attribute_path(node)
                return None

            def _reconstruct_fstring(self, node: ast.JoinedStr) -> str:
                """Reconstruct f-string pattern."""
                parts = []
                for value in node.values:
                    if isinstance(value, ast.Constant):
                        parts.append(str(value.value))
                    elif isinstance(value, ast.FormattedValue):
                        # For formatted values, create a placeholder
                        if isinstance(value.value, ast.Attribute):
                            attr_path = self._extract_attribute_path(value.value)
                            parts.append(f"{{{attr_path}}}")
                        else:
                            parts.append("{param}")
                return "".join(parts)

            def _extract_attribute_path(self, node: ast.Attribute) -> str:
                """Extract attribute path like self.base_path."""
                if isinstance(node.value, ast.Name):
                    return f"{node.value.id}.{node.attr}"
                elif isinstance(node.value, ast.Attribute):
                    parent = self._extract_attribute_path(node.value)
                    return f"{parent}.{node.attr}"
                return node.attr

        visitor = RouteVisitor()
        visitor.visit(tree)

        # Return the first route found (most methods have only one)
        return visitor.routes[0] if visitor.routes else None

    def _extract_route_with_regex(self, source_code: str) -> Optional[str]:
        """Extract route using regex patterns as fallback."""
        patterns = [
            # Direct string literals
            r'resource_path\s*=\s*["\']([^"\']+)["\']',
            # f-string patterns
            r'resource_path\s*=\s*f["\']([^"\']+)["\']',
            # String concatenation with self.base_path
            r'resource_path\s*=\s*f?["\']?{([^}]+)}["\']?',
            # self.base_path variations
            r"resource_path\s*=\s*self\.([a-zA-Z_]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, source_code)
            if match:
                return match.group(1)

        return None


class APIDiscovery:
    """Discovers and analyzes API classes."""

    def __init__(self, base_path: str = "src/evo_client"):
        self.base_path = Path(base_path)
        self.route_extractor = RouteExtractor()

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

                # Extract API route
                api_route = self.route_extractor.extract_route_from_method(method)

                method_sig = MethodSignature(
                    name=name,
                    parameters=parameters,
                    return_annotation=sig.return_annotation,
                    is_async=is_async,
                    docstring=inspect.getdoc(method),
                    api_route=api_route,
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
            "route_mismatches": [],  # New field for route mismatches
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

            if method_comparison["issues"] or method_comparison["route_issues"]:
                mismatch_entry = {
                    "sync_class": sync_class.name,
                    "async_class": async_class.name,
                    "issues": method_comparison["issues"],
                }

                if method_comparison["route_issues"]:
                    results["route_mismatches"].append(
                        {
                            "sync_class": sync_class.name,
                            "async_class": async_class.name,
                            "route_issues": method_comparison["route_issues"],
                        }
                    )
                    mismatch_entry["route_issues"] = method_comparison["route_issues"]

                results["signature_mismatches"].append(mismatch_entry)
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
        route_issues = []

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

            # Compare API routes
            route_issue = self._compare_method_routes(sync_method, async_method)
            if route_issue:
                route_issues.append(f"Method '{method_name}': {route_issue}")

        return {"issues": issues, "route_issues": route_issues}

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

    def _compare_method_routes(
        self, sync_method: MethodSignature, async_method: MethodSignature
    ) -> Optional[str]:
        """Compare API routes between sync and async methods."""
        sync_route = sync_method.api_route
        async_route = async_method.api_route

        # Skip comparison if routes couldn't be extracted
        if sync_route is None and async_route is None:
            return None

        if sync_route is None:
            return f"Could not extract route from sync method (async: {async_route})"

        if async_route is None:
            return f"Could not extract route from async method (sync: {sync_route})"

        # Normalize routes for comparison (handle different f-string patterns)
        normalized_sync = self._normalize_route(sync_route)
        normalized_async = self._normalize_route(async_route)

        if normalized_sync != normalized_async:
            return f"Route mismatch - sync: '{sync_route}' vs async: '{async_route}'"

        return None

    def _normalize_route(self, route: str) -> str:
        """Normalize route for comparison."""
        # Replace common base path patterns
        route = re.sub(r"self\.base_path(?:_v\d+)?", "/api/v1/base", route)
        route = re.sub(r"\{[^}]+\}", "{param}", route)  # Normalize path parameters
        return route


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

    # Route mismatches (new section)
    if results.get("route_mismatches"):
        report.append("API ROUTE MISMATCHES:")
        for mismatch in results["route_mismatches"]:
            report.append(f"  {mismatch['sync_class']} <-> {mismatch['async_class']}:")
            for issue in mismatch["route_issues"]:
                report.append(f"    - {issue}")
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
