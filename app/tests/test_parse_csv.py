import codecs
import io
from app.parse_csv import QAData, QADataParser


# TODO: Test with certain columns empty: Campaign Name, Ad Set Name, Ad Name


def csv_string_to_bytes(csv_string: str) -> io.BytesIO:
    return io.BytesIO(codecs.encode(csv_string, "utf-8"))


def test_parse_two_ads_no_filtering():
    csv_string = "Campaign name,Ad Set Name,Ad name,call_to_action_type,headline,Website URL,Reporting starts,Reporting ends\ncampaign1,adset1,ad1,cta1,headline1,landingpage1,1/23/2044,1/23/2044\ncampaign1,adset2,ad1,cta1,headline1,landingpage1,1/23/2044,1/23/2044"
    expected = {
        "campaign1": {
            "adset1": {"ad1": {"landing_page": "landingpage1", "cta": "cta1"}},
            "adset2": {"ad1": {"landing_page": "landingpage1", "cta": "cta1"}},
        }
    }

    bytes_csv = csv_string_to_bytes(csv_string)
    res = QADataParser.parse(bytes_csv)
    assert expected == res


def test_parse_two_ads_filter_one():
    csv_string = "Campaign name,Ad Set Name,Ad name,call_to_action_type,headline,Website URL,Reporting starts,Reporting ends\ncampaign1,adset1,ad2,cta1,headline1,landingpage1,1/23/2044,1/23/2044\ncampaign1,adset2,ad1,cta1,headline1,landingpage1,1/23/2044,1/23/2044"
    expected = {
        "campaign1": {
            "adset2": {"ad1": {"landing_page": "landingpage1", "cta": "cta1"}},
        }
    }

    bytes_csv = csv_string_to_bytes(csv_string)
    res = QADataParser.parse(bytes_csv, filter_for_ad_key="ad1")
    assert expected == res


def test_add_row_qa_data_empty():
    qadata = QAData()
    test_row = [
        "campaign",
        "adset",
        "ad",
        {"landing_page": "landingpage", "cta": "cta"},
    ]

    expected = {
        "campaign": {"adset": {"ad": {"landing_page": "landingpage", "cta": "cta"}}}
    }

    qadata.add(*test_row)

    assert expected == qadata.to_dict()


def test_add_second_ad():
    qadata = QAData()
    qadata.data = {
        "campaign": {"adset": {"ad": {"landing_page": "landingpage", "cta": "cta"}}}
    }
    test_row = [
        "campaign",
        "adset",
        "ad2",
        {"landing_page": "landingpage", "cta": "cta"},
    ]
    qadata.add(*test_row)
    expected = {
        "campaign": {
            "adset": {
                "ad": {"landing_page": "landingpage", "cta": "cta"},
                "ad2": {"landing_page": "landingpage", "cta": "cta"},
            }
        }
    }
    assert qadata.to_dict() == expected
