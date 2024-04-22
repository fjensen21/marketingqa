from app.qa.ad import AdProperties, Checks, ExpectedValues, QAChecker


def test_cta_is_correct():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "testlandingpage",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1", "adset2"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {"ad1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}},
            "adset2": {"ad2": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}},
        },
        "campaign2": {
            "adset2": {"ad2": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
        },
    }

    checks = Checks(ad_name=False, cgen=False, landing_page=False)
    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {"success": True}


def test_cta_is_not_correct():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "testlandingpage",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {"ad1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
        },
        "campaign2": {
            "adset2": {"ad2": {"landing_page": "landingpage1", "cta": "NOT_LEARN"}}
        },
    }

    checks = Checks(ad_name=False, cgen=False, landing_page=False)

    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {
        "success": False,
        "failures": {"campaign2 > adset2 > ad2": ["Incorrect CTA"]},
    }


def test_ad_name_is_incorrect():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "testlandingpage",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {"TestAd1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
        },
        "campaign2": {
            "adset2": {"ad2": {"landing_page": "landingpage1", "cta": "NOT_LEARN"}}
        },
    }

    checks = Checks(cta=False, cgen=False, landing_page=False)

    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {
        "success": False,
        "failures": {"campaign2 > adset2 > ad2": ["Incorrect Ad Name"]},
    }


def test_ad_name_correct():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "testlandingpage",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {"TestAd1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
        },
        "campaign2": {
            "adset2": {"TestAd1": {"landing_page": "landingpage1", "cta": "NOT_LEARN"}}
        },
    }

    checks = Checks(cta=False, cgen=False, landing_page=False)

    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {
        "success": True,
    }


def test_landing_page_incorrect():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "landingpage1.com/page",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {
                "TestAd1": {
                    "landing_page": "landingpage1.com/page?sdid=1234",
                    "cta": "LEARN_MORE",
                }
            }
        },
        "campaign2": {
            "adset2": {"TestAd1": {"landing_page": "landingpage1", "cta": "NOT_LEARN"}}
        },
    }

    checks = Checks(cta=False, ad_name=False, cgen=False)
    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {
        "success": False,
        "failures": {"campaign2 > adset2 > TestAd1": ["Incorrect Landing Page"]},
    }


def test_ad_in_invalid_ad_set():
    expected: ExpectedValues = {
        "ad_name": "TestAd1",
        "landing_page": "landingpage1.com/page",
        "cta": "LEARN_MORE",
        "cgens": {"NA": 1234, "LATAM": 1235},
        "campaigns": {"campaign1": {"adset1"}, "campaign2": {"adset2"}},
    }

    qa_data: dict = {
        "campaign1": {
            "adset1": {
                "TestAd1": {
                    "landing_page": "landingpage1.com/page?sdid=1234",
                    "cta": "LEARN_MORE",
                }
            },
            "adset2": {
                "TestAd1": {
                    "landing_page": "landingpage1.com/page?sdid=1234",
                    "cta": "LEARN_MORE",
                }
            },
        },
        "campaign2": {
            "adset2": {"TestAd1": {"landing_page": "landingpage1", "cta": "NOT_LEARN"}}
        },
    }

    checks = Checks(cta=False, ad_name=False, landing_page=False, cgen=False)

    checker = QAChecker(qa_data, expected, checks)

    assert checker.run() == {
        "success": False,
        "failures": {"campaign1 > adset2 > TestAd1": ["Incorrect Ad Placement"]},
    }
