from typing import List, Optional
from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError
from app.parse_csv import QADataParser
from app.qa.ad import AdProperties, Checks, ExpectedValues, QAChecker

app = FastAPI()


class Config(BaseModel):
    expected_values: ExpectedValues
    checks: Optional[Checks] = None
    ad_search_key: str


def checker(config: str = Form(...)):
    try:
        return Config.model_validate_json(config)
    except ValidationError as e:
        raise HTTPException(
            detail=jsonable_encoder(e.errors()),
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


@app.get("/")
def get_home():
    return {"status": "ok", "Hello": "World!!!"}


@app.post("/ad/upload")
def qa_ad_file(
    config: Config = Depends(checker),
    file: UploadFile = File(...),
):
    expected_values = config.expected_values
    checks = config.checks

    campaign_data = QADataParser.parse(
        file.file, filter_for_ad_key=config.ad_search_key
    )
    checker = (
        QAChecker(campaign_data, expected_values, checks)
        if checks
        else QAChecker(campaign_data, expected_values)
    )
    result = checker.run()
    return result
