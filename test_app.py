import os

from app import classify_log, get_absolute_path, get_agent_label


def test_dependency_error():
    log = "ModuleNotFoundError: No module named 'requests'"
    result = classify_log(log)
    assert result["error_type"] == "dependency_error"


def test_test_failure():
    log = "AssertionError: expected True but got False"
    result = classify_log(log)
    assert result["error_type"] == "test_failure"


def test_test_failure_2():
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


def test_absolute_path():
    log = "error"
    result = get_absolute_path(log)
    assert result == "not found"


def test_absolute_path_2():
    log = "."
    result = get_absolute_path(log)
    abs_path = os.path.abspath(os.getcwd())
    assert result == abs_path


def test_get_bare_metal():
    """Test to always return baremetal node"""
    assert get_agent_label(force=True) == 'bare_metal'


def test_get_node():
    """Test to either return baremetal or aws"""
    assert get_agent_label() in ('aws', 'bare_metal')

def test_get_node_unknown():
    """Test to either return baremetal or aws"""
    assert get_agent_label('unknown', force=False) in ('unknown', 'aws', 'bare_metal')

def test_get_node_unknown_force():
    """Test to either return baremetal or aws"""
    assert get_agent_label('unknown', force=True) == 'unknown'


