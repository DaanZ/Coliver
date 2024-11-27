import copy
import os

from dotenv import load_dotenv
from pyairtable import Base

load_dotenv()

COLIVER_BASE_ID = os.environ.get("COLIVER_BASE_ID")
AIRTABLE_API_KEY = os.environ.get("AIRTABLE_API_KEY")
base = Base(AIRTABLE_API_KEY, COLIVER_BASE_ID)

QNA_TABLE_NAME = os.environ.get("QNA_TABLE_NAME")
company_table = base.table(QNA_TABLE_NAME)


def create_qna(data):
    return company_table.create(data)
