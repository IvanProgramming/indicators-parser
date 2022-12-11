import os

from parsers.text_parser import find_ioc
from parsers.pdf_parser import process_pdf
from requests import get


def test_no_collectable_data_in_text():
    text = "This is a test text"
    collected_data = find_ioc(text)
    assert collected_data.hashes == set()
    assert collected_data.ips == set()
    assert collected_data.urls == set()


def test_collect_hashes():
    text = "This is a test text with a hash 5d41402abc4b2a76b9719d911017c592"
    collected_data = find_ioc(text)
    assert collected_data.hashes == {"5d41402abc4b2a76b9719d911017c592"}
    assert collected_data.ips == set()
    assert collected_data.urls == set()


def test_collectable_ips():
    text = "Some text with an IP. 102.123.253.123"
    collected_data = find_ioc(text)
    assert collected_data.hashes == set()
    assert collected_data.ips == {"102.123.253.123"}
    assert collected_data.urls == set()


def test_collectable_ips_local():
    text = "Some text with an IP. But this one is local 127.0.0.1"
    collected_data = find_ioc(text)
    assert collected_data.hashes == set()
    assert collected_data.ips == set()
    assert collected_data.urls == set()


def test_collectable_urls():
    text = "Some text with a URL. https://www.google.com"
    collected_data = find_ioc(text)
    assert collected_data.hashes == set()
    assert collected_data.ips == set()
    assert collected_data.urls == {"https://www.google.com/"}


def test_parse_pdf_no_data():
    pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
    pdf_path = "dummy.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)
    collected_data = process_pdf(pdf_path)
    assert collected_data.hashes == set()
    assert collected_data.ips == set()
    assert collected_data.urls == set()

    os.remove(pdf_path)


def test_parse_pdf_with_data():
    pdf_url = "https://storage.yandexcloud.net/ivanprogramming/Network_Report.pdf"
    # This is my report for MTS Cybersecurity Challenge 2022, loaded to Yandex Cloud Storage (like AWS S3)
    pdf_path = "Network_Report.pdf"
    with open(pdf_path, "wb") as f:
        f.write(get(pdf_url).content)
    collected_data = process_pdf(pdf_path)
    correct_hashes = {"8cf2cddda8522975a22da3da429339be471234eacc0e11c099d6dcb732cf3cbb",
                      "f1b789be1126b557240dd0dfe98fc5f3ad6341bb1a5d8be0a954f65b486ad32a",
                      "d43159c8bf2e1bd866abdbb1687911e2282b1f98a7c063f85ffd53a7f51efed4",
                      "38c6c5b8d6fa71d9856758a5c0c2ac9d0a0a1450f75bb1004dd988e23d73a312",
                      "4c957072ab097d3474039f432466cd251d1dc7d91559b76d4e5ead4a8bd499d5",
                      "3abae6dd2ddae23b2de2ccbcc160a4a5773bef8934d0e6896d50197c3d3c417f"}
    for correct_hash in correct_hashes:
        assert correct_hash in collected_data.hashes

    correct_ips = {
        "209.141.55.226",
        "85.143.218.7",
        "46.249.62.199",
        "190.146.112.216",
        "87.236.22.142"
    }
    for correct_ip in correct_ips:
        assert correct_ip in collected_data.ips

    assert "http://www.rootscafeslc.com/" in collected_data.urls
    os.remove(pdf_path)
