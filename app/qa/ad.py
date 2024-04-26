from typing import List
from pydantic import BaseModel, Field
from typing_extensions import TypedDict
from collections import defaultdict


class ExpectedValues(TypedDict):
    ad_name: str
    landing_page: str
    cta: str
    cgens: dict[str, int]
    campaigns: dict[str, set[str]]


# TODO: Change this to a BaseModel
class AdProperties(TypedDict):
    landing_page: str
    cta: str


class Checks(BaseModel):
    cta: bool = Field(default=True)
    ad_name: bool = Field(default=True)
    cgen: bool = Field(default=True)
    landing_page: bool = Field(default=True)


class QAChecker:
    def __init__(
        self,
        campaigns: dict[str, dict[str, dict[str, AdProperties]]],
        expected: ExpectedValues,
        checks: Checks = Checks(),
    ):
        self.campaigns = campaigns
        self.expected = expected
        self.checks = checks

    def run(self):
        failure_messages = defaultdict(list)
        seen_ad_location = defaultdict(set)
        for campaign in self.campaigns:
            adsets = self.campaigns[campaign]
            for adset in adsets:
                ads = adsets[adset]
                for ad in ads:
                    error_path = f"{campaign} > {adset} > {ad}"
                    if self.checks.cta:
                        if not self.is_correct_cta(ads[ad]["cta"]):
                            failure_messages[error_path].append("Incorrect CTA")
                    if self.checks.ad_name:
                        if not self.is_correct_ad_name(ad):
                            failure_messages[error_path].append("Incorrect Ad Name")
                    if self.checks.landing_page:
                        landing_page = ads[ad]["landing_page"].split("?")[0]
                        if not self.is_correct_landing_page(landing_page):
                            failure_messages[error_path].append(
                                "Incorrect Landing Page"
                            )

                    if not self.is_expected_path(campaign, adset):
                        failure_messages[error_path].append(
                            "Ad in unexpected campaign and/or ad set"
                        )

                    seen_ad_location[campaign].add(adset)

        differences = self.compute_differences(
            self.expected["campaigns"], seen_ad_location
        )
        if differences:
            for difference in differences:
                failure_messages[difference].append(
                    "Ad is missing from expected ad set and campaign"
                )

        if len(failure_messages) > 0:
            return {"success": False, "failures": failure_messages}
        return {"success": True}

    def is_correct_cta(self, cta: str):
        correct_cta = self.expected["cta"]
        return correct_cta == cta

    def is_correct_ad_name(self, ad_name: str):
        correct_ad_name = self.expected["ad_name"]
        return correct_ad_name == ad_name

    def compute_differences(
        self,
        expected_structure: dict[str, set[str]],
        actual_structure: dict[str, set[str]],
    ) -> List[str]:
        differences = []
        for campaign in expected_structure:
            for ad_set in expected_structure[campaign]:
                if (
                    campaign not in actual_structure
                    or ad_set not in actual_structure[campaign]
                ):
                    differences.append(f"{campaign} > {ad_set}")
        return differences

    def is_correct_landing_page(self, landing_page: str):
        return self.expected["landing_page"] == landing_page

    def is_expected_path(self, campaign: str, ad_set: str):
        campaigns = self.expected["campaigns"]
        if campaign not in campaigns or ad_set not in campaigns[campaign]:
            return False
        return True


if __name__ == "__main__":
    expected: dict = {
        "expected": {
            "ad_name": "TestAd1",
            "landing_page": "testlandingpage",
            "cta": "LEARN_MORE",
            "cgens": {"NA": 1234, "LATAM": 1235},
        }
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {"ad1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
        }
    }

    # checker = QAChecker(qa_data, expected)
    # checker.run()
