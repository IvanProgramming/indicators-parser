from re import findall
from typing import Set, Iterable

from pydantic import BaseModel, IPvAnyAddress, AnyUrl


class CollectedData(BaseModel):
    """ Represents the data collected from text """

    hashes: Set[str] = set()
    """ Set of hashes found in the text """
    ips: Set[IPvAnyAddress] = set()
    """ Set of IPs found in the text """
    urls: Set[AnyUrl] = set()
    """ Set of URLs found in the text """


def filter_already_found_hashes(new_hashes: list, already_found_hashes: list) -> list:
    """ Filters out hashes that are already found in the already_found_hashes list

    Args:
        new_hashes (list): List of hashes to filter
        already_found_hashes (list): List of hashes to filter out
    """
    for already_found_hash in already_found_hashes:
        filtered_hashes = []
        for md5_hash in new_hashes:
            if md5_hash not in already_found_hash:
                filtered_hashes.append(md5_hash)
        new_hashes = filtered_hashes.copy()
    return new_hashes


def filter_local_ips(ips: Iterable[str]) -> list:
    """
        Filter out local IPs from the list of IPs

        Args:
            ips (list): List of IPs to filter
    """
    filtered_ips = []
    for ip in ips:
        octets = list(map(int, ip.split(".")))
        if octets[0] == 10 or (octets[0] == 172 and 16 <= octets[1] <= 31) or (octets[0] == 192 and octets[1] == 168) \
                or octets[0] == 127:
            continue
        filtered_ips.append(ip)
    return filtered_ips


def filter_invalid_ips(ips: Iterable[str]) -> list:
    """
        Filter out invalid IPs from the list of IPs

        Args:
            ips (list): List of IPs to filter
    """
    filtered_ips = []
    for ip in ips:
        octets = list(map(int, ip.split(".")))
        if octets[0] == 0 or octets[0] == 255 or octets[3] == 0 or octets[3] == 255:
            continue
        filtered_ips.append(ip)
    return filtered_ips


def find_ioc(text: str) -> CollectedData:
    """
    Finds hashes, IPs and URLs in the text

    Args:
        text (str): Text to search for hashes, IPs and URLs

    Returns:
        CollectedData: CollectedData object with the found hashes, IPs and URLs
    """
    collected_data = CollectedData()
    sha256_hashes = findall(r"[a-f0-9]{64}", text)
    sha1_hashes = filter_already_found_hashes(findall(r"[a-f0-9]{40}$", text), sha256_hashes)
    md5_hashes = filter_already_found_hashes(findall(r"[a-f0-9]{32}", text), sha256_hashes + sha1_hashes)
    collected_data.hashes = set(sha256_hashes + sha1_hashes + md5_hashes)
    ipv4 = findall(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", text)
    collected_data.ips = set(filter_invalid_ips(filter_local_ips(ipv4)))
    urls = findall(
        r"(http|https|ftp)\://([a-zA-Z0-9\-\.]+\.+[a-zA-Z]{2,3})(:[a-zA-Z0-9]*)?/?([a-zA-Z0-9\-\._\?\,\'/\\"
        r"\+&amp;%\$#\=~]*)[^\.\,\)\(\s]?",
        text)
    for url in urls:
        collected_data.urls.add(url[0] + "://" + url[1] + (f":{url[2]}" if url[2] != "" else "") + "/" + url[3])
    return collected_data
