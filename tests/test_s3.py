import os

from requests import get

from integrations.s3 import save_report_to_s3, remove_report_from_s3, generate_report_url
from settings import S3_BASE_URL


def test_s3_file_load_public():
    pdf_url = "https://storage.yandexcloud.net/ivanprogramming/Network_Report.pdf"
    pdf_path = "Network_Report.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)
    save_report_to_s3(pdf_path, "test", is_public=True)

    url = S3_BASE_URL + "test.pdf"
    response = get(url)
    assert response.status_code == 200

    remove_report_from_s3("test")
    os.remove(pdf_path)


def test_s3_file_load_private():
    pdf_url = "https://storage.yandexcloud.net/ivanprogramming/Network_Report.pdf"
    pdf_path = "Network_Report.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)
    save_report_to_s3(pdf_path, "test-private", is_public=False)

    url = S3_BASE_URL + "test.pdf"
    response = get(url)
    assert response.status_code == 403
    presigned_url = generate_report_url("test-private")
    response = get(presigned_url)
    assert response.status_code == 200

    remove_report_from_s3("test-private")
    os.remove(pdf_path)
