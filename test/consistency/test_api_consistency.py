"""
Test API consistency between sync and async implementations.
"""

import pytest


class TestAPIConsistency:
    """Test consistency between sync and async APIs."""

    def test_api_classes_exist(self, sync_classes, async_classes):
        """Test that both sync and async API classes exist."""
        assert len(sync_classes) > 0, "No sync API classes found"
        assert len(async_classes) > 0, "No async API classes found"

        print(
            f"Found {len(sync_classes)} sync classes and {len(async_classes)} async classes"
        )

    def test_full_api_consistency(self, consistency_results, report_generator):
        """Test full API consistency between sync and async implementations."""

        # Generate detailed report
        report = report_generator(consistency_results)
        print("\n" + report)

        # Assert no critical issues
        assert (
            consistency_results["total_issues"] == 0
        ), f"Found {consistency_results['total_issues']} consistency issues:\n{report}"

    @pytest.mark.parametrize(
        "api_name",
        ["MembersApi", "WebhookApi", "SalesApi", "ActivitiesApi", "WorkoutApi"],
    )
    def test_specific_api_consistency(
        self, api_name, sync_classes, async_classes, api_validator
    ):
        """Test consistency for specific API classes."""

        sync_class_name = f"Sync{api_name}"
        async_class_name = f"Async{api_name}"

        # Check if classes exist
        if sync_class_name not in sync_classes:
            pytest.skip(f"Sync class {sync_class_name} not found")
        if async_class_name not in async_classes:
            pytest.skip(f"Async class {async_class_name} not found")

        sync_class = sync_classes[sync_class_name]
        async_class = async_classes[async_class_name]

        # Compare methods
        method_comparison = api_validator._compare_class_methods(
            sync_class, async_class
        )

        if method_comparison["issues"]:
            issues_str = "\n".join(method_comparison["issues"])
            pytest.fail(f"Method inconsistencies in {api_name}:\n{issues_str}")

    def test_method_signature_consistency(self, consistency_results):
        """Test that method signatures are consistent between sync and async."""

        signature_issues = []
        for mismatch in consistency_results["signature_mismatches"]:
            for issue in mismatch["issues"]:
                if "annotation mismatch" in issue or "default value mismatch" in issue:
                    signature_issues.append(f"{mismatch['sync_class']}: {issue}")

        assert len(signature_issues) == 0, f"Method signature issues:\n" + "\n".join(
            signature_issues
        )

    def test_no_missing_classes(self, consistency_results):
        """Test that no API classes are missing in either sync or async."""

        missing_issues = []
        if consistency_results["missing_in_sync"]:
            missing_issues.extend(
                [
                    f"Missing in sync: {cls}"
                    for cls in consistency_results["missing_in_sync"]
                ]
            )
        if consistency_results["missing_in_async"]:
            missing_issues.extend(
                [
                    f"Missing in async: {cls}"
                    for cls in consistency_results["missing_in_async"]
                ]
            )

        assert len(missing_issues) == 0, f"Missing classes:\n" + "\n".join(
            missing_issues
        )

    def test_async_methods_are_async(self, async_classes):
        """Test that async API methods are properly marked as async."""

        non_async_methods = []
        for class_name, class_info in async_classes.items():
            for method_name, method_info in class_info.methods.items():
                if not method_info.is_async:
                    non_async_methods.append(f"{class_name}.{method_name}")

        assert (
            len(non_async_methods) == 0
        ), f"Async methods not marked as async:\n" + "\n".join(non_async_methods)

    def test_sync_methods_are_not_async(self, sync_classes):
        """Test that sync API methods are not marked as async."""

        async_methods = []
        for class_name, class_info in sync_classes.items():
            for method_name, method_info in class_info.methods.items():
                if method_info.is_async:
                    async_methods.append(f"{class_name}.{method_name}")

        assert len(async_methods) == 0, f"Sync methods marked as async:\n" + "\n".join(
            async_methods
        )


class TestConsistencyReporting:
    """Test consistency reporting functionality."""

    def test_generate_report(self, consistency_results, report_generator):
        """Test that consistency reports are generated properly."""
        report = report_generator(consistency_results)

        assert "API CONSISTENCY REPORT" in report
        assert "Total Issues Found:" in report
        assert "Sync Classes:" in report
        assert "Async Classes:" in report

    def test_report_includes_all_sections(self, report_generator):
        """Test that the report includes all expected sections."""
        # Create mock results with all types of issues
        mock_results = {
            "sync_classes": ["SyncMembersApi", "SyncWebhookApi"],
            "async_classes": ["AsyncMembersApi", "AsyncWebhookApi"],
            "missing_in_sync": ["AsyncOnlyApi"],
            "missing_in_async": ["SyncOnlyApi"],
            "signature_mismatches": [
                {
                    "sync_class": "SyncMembersApi",
                    "async_class": "AsyncMembersApi",
                    "issues": ["Method 'test': Parameter 'x' annotation mismatch"],
                }
            ],
            "consistent_classes": [
                {
                    "sync_class": "SyncWebhookApi",
                    "async_class": "AsyncWebhookApi",
                    "method_count": 5,
                }
            ],
            "total_issues": 3,
        }

        report = report_generator(mock_results)

        assert "MISSING IN SYNC:" in report
        assert "MISSING IN ASYNC:" in report
        assert "SIGNATURE MISMATCHES:" in report
        assert "CONSISTENT CLASSES:" in report
        assert "Total Issues Found: 3" in report


@pytest.mark.consistency
class TestAPIConsistencyMarked:
    """Tests marked with consistency marker for easy filtering."""

    def test_api_consistency_marked(self, consistency_results, report_generator):
        """Test marked with consistency marker."""
        report = report_generator(consistency_results)

        # This test is marked for easy running with: pytest -m consistency
        # It won't fail but will report current state
        print(f"\n=== API Consistency Status ===")
        print(f"Total Issues: {consistency_results['total_issues']}")
        print(f"Consistent Classes: {len(consistency_results['consistent_classes'])}")
        print(f"Total Classes: {len(consistency_results['sync_classes'])}")

        if consistency_results["total_issues"] > 0:
            print(f"\n=== Issues to Address ===")
            for mismatch in consistency_results["signature_mismatches"]:
                print(
                    f"- {mismatch['sync_class']} ↔ {mismatch['async_class']}: {len(mismatch['issues'])} issues"
                )


# Mock/Test Data Fixtures for testing
@pytest.fixture
def mock_api_classes():
    """Mock API classes for testing."""
    from .conftest import APIClassInfo, MethodSignature

    mock_method = MethodSignature(
        name="test_method",
        parameters={
            "param1": {
                "annotation": str,
                "default": None,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        },
        return_annotation=str,
        is_async=False,
    )

    sync_class = APIClassInfo(
        name="SyncTestApi",
        module_path="test.sync.api.test_api",
        methods={"test_method": mock_method},
        is_async=False,
    )

    async_method = MethodSignature(
        name="test_method",
        parameters={
            "param1": {
                "annotation": str,
                "default": None,
                "kind": "POSITIONAL_OR_KEYWORD",
            }
        },
        return_annotation=str,
        is_async=True,
    )

    async_class = APIClassInfo(
        name="AsyncTestApi",
        module_path="test.aio.api.test_api",
        methods={"test_method": async_method},
        is_async=True,
    )

    return {"sync": sync_class, "async": async_class}
