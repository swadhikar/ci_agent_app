import re
import glob
import pathlib
import random
import os


def classify_log(log: str) -> dict:
    """
    Analyze the log and classify the failure

    Returns:
            dict with:
                - error_type
                - summary
                - suggested_fix
    """
    log = log.lower()

    if "modulenotfound" in log or "importerror" in log:
        error_type = "dependency_error"
        summary = "missing python module detected"
        suggested_fix = "Install the required dependency using pip."
    elif "assertionerror" in log or "test failed" in log:
        error_type = "test_failure"
        summary = "A test case failed during execution."
        suggested_fix = "Check test assertions and expected outputs."
    elif "connection timed out" in log:
        error_type = "infra_error"
        summary = "Network timeout or infrastructure issue."
        suggested_fix = "Check network/firewall or cloud resources."
    else:
        error_type = "unknown"
        summary = "Could not identify a specific failure pattern."
        suggested_fix = "Review the full log manually."

    return {"error_type": error_type, "summary": summary, "suggested_fix": suggested_fix}


def get_absolute_path(directory: str) -> str:
    """
    Given the directory returns absolute path

    Args:
        directory: path

    Returns:
        Absolute path for current directory
    """
    if os.path.exists(directory):
        return os.path.abspath(directory)
    return 'not found'


def get_agent_label(label: str = 'bare_metal', force=False) -> str:
    """
        Either return baremetal or aws label for jenkins agent

        Forces bare_metal when force is set
    """
    if random.random() < 0.5 or force:
        return label
    return 'aws'


