"""
Unit tests for trie.py
"""
import pytest

from transport.app import Station, create_trie


@pytest.fixture(scope="module")
def trie():
    """
    Create a trie from the CSV list of stations for use in the unit tests.
    """
    trie = create_trie()
    return trie


def test_search_single_match_upper(trie):
    """
    Match on a single uppercase character
    """
    result = trie.search("Q")
    assert len(result) == 7
    assert Station("Quakers Yard", "QYD") in result
    assert Station("Queenborough", "QBR") in result
    assert Station("Queens Park (Glasgow)", "QPK") in result
    assert Station("Queens Park (London)", "QPW") in result
    assert Station("Queens Road (Peckham)", "QRP") in result
    assert Station("Queenstown Road (Battersea)", "QRB") in result
    assert Station("Quintrell Downs", "QUI") in result


def test_search_single_miss_upper(trie):
    """
    Mismatch on a single uppercase character
    """
    result = trie.search("Z")
    assert not result


def test_search_single_match_lower(trie):
    """
    Match on a single lowercase character
    """
    result = trie.search("j")
    assert len(result) == 5
    assert Station("James Cook", "JCH") in result
    assert Station("Jewellery Quarter", "JEQ") in result
    assert Station("Johnston (Pembs)", "JOH") in result
    assert Station("Johnstone (Strathclyde)", "JHN") in result
    assert Station("Jordanhill", "JOR") in result


def test_search_single_miss_lower(trie):
    """
    Mismatch on a single lowercase character
    """
    result = trie.search("x")
    assert not result


def test_empty(trie):
    """
    Search with an empty string
    """
    result = trie.search("")
    assert len(result) == 2570


def test_intermediate_lower(trie):
    """
    Match on a multiple lowercase characters
    """
    result = trie.search("shor")
    assert len(result) == 4
    assert Station("Shoreditch High Street", "SDC") in result
    assert Station("Shoreham (Kent)", "SEH") in result
    assert Station("Shoreham-by-Sea", "SSE") in result
    assert Station("Shortlands", "SRT") in result


def test_intermediate_upper(trie):
    """
    Match on a multiple uppercase characters
    """
    result = trie.search("TAL")
    assert len(result) == 3
    assert Station("Talsarnau", "TAL") in result
    assert Station("Talybont", "TLB") in result
    assert Station("Tal-y-Cafn", "TLC") in result


def test_intermediate_mixed(trie):
    """
    Match on a multiple mixed case characters
    """
    result = trie.search("eWeLl")
    assert len(result) == 2
    assert Station("Ewell East", "EWE") in result
    assert Station("Ewell West", "EWW") in result


def test_full_lower(trie):
    """
    Match on a full query in lowercase
    """
    result = trie.search("formby")
    assert len(result) == 1
    assert Station("Formby", "FBY") in result


def test_full_upper(trie):
    """
    Match on a full query in uppercase
    """
    result = trie.search("AYR")
    assert len(result) == 1
    assert Station("Ayr", "AYR") in result


def test_full_mixed(trie):
    """
    Match on a full query in mixed case
    """
    result = trie.search("rUnCoRn eASt")
    assert len(result) == 1
    assert Station("Runcorn East", "RUE") in result


def test_over_full_no_match(trie):
    """
    Mismatch due to extra characters at the end of the query
    """
    result = trie.search("AYRE")
    assert not result


def test_mid_match(trie):
    """
    Mismatch due to extra characters at the start of the query
    """
    result = trie.search("YSalisbury")
    assert not result


def test_space(trie):
    """
    Match with a space in the query string
    """
    result = trie.search("Small Heat")
    assert len(result) == 1
    assert Station("Small Heath", "SMA") in result


def test_full_and_partial_match(trie):
    """
    Match both full and partial
    """
    result = trie.search("Derby")
    assert len(result) == 2
    assert Station("Derby Road (Ipswich)", "DBR") in result
    assert Station("Derby", "DBY") in result
