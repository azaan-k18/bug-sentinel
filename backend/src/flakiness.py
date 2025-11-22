# flakiness.py

from dataclasses import dataclass


@dataclass
class TestHistory:
    """
    Represents aggregated historical data for a test.
    """
    failure_count: int = 0
    total_runs: int = 0
    unique_error_signatures: int = 0
    distinct_frameworks: int = 1   # default 1 to avoid false penalties


def calculate_flakiness_score(
    label: str,
    failure_count: int,
    total_runs: int,
    unique_error_signatures: int,
    distinct_frameworks: int
) -> float:
    """
    Calculates a normalized flakiness score (0.0 to 1.0).

    Parameters:
        label (str): classified label ("real_bug", "environment_issue", etc.)
        failure_count (int): how many times this test failed in past runs
        total_runs (int): total historical runs
        unique_error_signatures (int): distinct normalized error texts
        distinct_frameworks (int): number of different frameworks where test failed

    Returns:
        float: flakiness score between 0.0 and 1.0
    """

    score = 0.0

    # A. Classification-based weighting
    label_weights = {
        "real_bug": 0.1,
        "script_issue": 0.5,
        "environment_issue": 0.8,
        "unknown": 0.4
    }
    score += label_weights.get(label, 0.4)

    # B. Repetition ratio (how consistently this error appears)
    if total_runs > 0:
        repetition_ratio = failure_count / total_runs
        score += (1 - repetition_ratio) * 0.5
    else:
        # No history means uncertain → partially flaky
        score += 0.3

    # C. Variability in normalized messages
    if unique_error_signatures > 5:
        score += 0.5
    elif unique_error_signatures > 2:
        score += 0.3

    # D. Framework variation (same test fails across frameworks)
    if distinct_frameworks > 1:
        score += 0.3

    # Clamp score between 0 and 1
    score = max(0.0, min(1.0, score))
    return round(score, 3)


def compute_flakiness(label: str, history: TestHistory) -> float:
    """
    Wrapper for easy usage when you already have a TestHistory object.

    Parameters:
        label (str): classification label from ML engine
        history (TestHistory): aggregated test history

    Returns:
        float: flakiness score
    """

    return calculate_flakiness_score(
        label=label,
        failure_count=history.failure_count,
        total_runs=history.total_runs,
        unique_error_signatures=history.unique_error_signatures,
        distinct_frameworks=history.distinct_frameworks
    )