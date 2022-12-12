import os

from requests import get

from integrations.s3 import save_report_to_s3, remove_report_from_s3, generate_report_url
from settings import S3_BASE_URL
from tests.fixtures.indicators import mts_report


def test_s3_file_load_public(mts_report):
    save_report_to_s3(mts_report, "test", is_public=True)

    url = S3_BASE_URL + "test.pdf"
    response = get(url)
    assert response.status_code == 200

    remove_report_from_s3("test")


def test_s3_file_load_private(mts_report):
    save_report_to_s3(mts_report, "test-private", is_public=False)

    url = S3_BASE_URL + "test.pdf"
    response = get(url)
    assert response.status_code == 403
    presigned_url = generate_report_url("test-private")
    response = get(presigned_url)
    assert response.status_code == 200

    remove_report_from_s3("test-private")
