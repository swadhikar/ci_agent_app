import pytest
from app import classify_log


def test_dependency_error():
    log = "ModuleNotFoundError: No module named 'requests'"
    result = classify_log(log)
    assert result["error_type"] == "dependency_error"


def test_test_failure():
    log = "AssertionError: expected True but got False"
    result = classify_log(log)
    assert result["error_type"] == "test_failure"


def test_infra_error():
    log = "Connection timed out while connecting to database"
    result = classify_log(log)
    assert result["error_type"] == "infra_error"


def test_unknown():
    log = "Some random unclassified error"
    result = classify_log(log)
    assert result["error_type"] == "unknown"
