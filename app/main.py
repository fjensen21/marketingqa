from typing import Optional
from fastapi import FastAPI

from app.qa.ad import AdProperties, Checks, ExpectedValues, QAChecker

app = FastAPI()


@app.post("/qa/ad")
def qa_ad(
    campaign_data: dict[str, dict[str, dict[str, AdProperties]]],
    expected_values: ExpectedValues,
    checks: Optional[Checks] = None,
):
    checker = (
        QAChecker(campaign_data, expected_values, checks)
        if checks
        else QAChecker(campaign_data, expected_values)
    )

    result = checker.run()
    return result
