import codecs
import csv
from collections import namedtuple
from typing import BinaryIO

from app.qa.ad import AdProperties

FIELDS = [
    "campaign_name",
    "ad_set_name",
    "ad_name",
    "cta",
    "headline",
    "website_url",
]

# data = (
#     {
#         "campaign1": {
#             "adset1": {
#                 "ad1": {"landing_page": "landingpage1", "cta": "LEARN_MORE"},
#                 "ad2": {"landing_page": "landingpage1", "cta": "LEARN_MORE"},
#             }
#         },
#         "campaign2": {
#             "adset2": {"ad2": {"landing_page": "landingpage1", "cta": "LEARN_MORE"}}
#         },
#     },
# )


class QADataParser:
    @classmethod
    def parse(cls, file: BinaryIO, filter_for_ad_key: None | str = None):
        reader = QADataReader(file)
        data = QAData()
        for row in reader:
            if filter_for_ad_key and filter_for_ad_key not in row.ad_name:
                continue
            ad_properties = AdProperties(landing_page=row.website_url, cta=row.cta)
            data.add(row.campaign_name, row.ad_set_name, row.ad_name, ad_properties)

        return data.to_dict()


class QAData:
    def __init__(self):
        self.data = {}

    def add(
        self,
        campaign_name: str,
        ad_set_name: str,
        ad_name: str,
        ad_properties: AdProperties,
    ):
        if campaign_name not in self.data:
            self.data[campaign_name] = {}
        if ad_set_name not in self.data[campaign_name]:
            self.data[campaign_name][ad_set_name] = {}

        self.data[campaign_name][ad_set_name][ad_name] = ad_properties

    def to_dict(self):
        return self.data


class QADataReader(object):
    def __init__(self, file: BinaryIO):
        self.file = file
        self._length = None

    def __iter__(self):
        self._length = 0
        encoding = "utf-8-sig"
        reader = csv.reader(codecs.iterdecode(self.file, encoding))

        next(reader)  # Skip header row

        for row in map(Record.parse, reader):
            self._length += 1
            yield row
        self.file.close()

    def __len__(self):
        if self._length is None:
            for _ in self:
                continue

        return self._length


class Record(namedtuple("Record_", FIELDS)):
    @classmethod
    def parse(cls, row):
        row = list(row)
        row = row[: len(FIELDS)]
        # Add any mutations here
        return cls(*row)


if __name__ == "__main__":
    pass
