import csv
from importlib import resources
from transport.trie import Trie

trie = Trie()


def setup_module():
    with resources.open_text('transport', 'station_codes.csv') as stations:
        rows = csv.reader(stations)
        next(rows)
        for row in rows:
            trie.insert(row[0], row)


def test_search_single_match_upper():
    result = trie.search('Q')
    assert len(result) == 7
    assert ['Quakers Yard', 'QYD'] in result
    assert ['Queenborough', 'QBR'] in result
    assert ['Queens Park (Glasgow)', 'QPK'] in result
    assert ['Queens Park (London)', 'QPW'] in result
    assert ['Queens Road (Peckham)', 'QRP'] in result
    assert ['Queenstown Road (Battersea)', 'QRB'] in result
    assert ['Quintrell Downs', 'QUI'] in result


def test_search_single_miss_upper():
    result = trie.search('Z')
    assert not result


def test_search_single_match_lower():
    result = trie.search('j')
    assert len(result) == 5
    assert ['James Cook', 'JCH'] in result
    assert ['Jewellery Quarter', 'JEQ'] in result
    assert ['Johnston (Pembs)', 'JOH'] in result
    assert ['Johnstone (Strathclyde)', 'JHN'] in result
    assert ['Jordanhill', 'JOR'] in result


def test_search_single_miss_lower():
    result = trie.search('x')
    assert not result


def test_empty():
    result = trie.search('')
    assert len(result) == 2570


def test_intermediate_lower():
    result = trie.search('shor')
    assert len(result) == 4
    assert ['Shoreditch High Street', 'SDC'] in result
    assert ['Shoreham (Kent)', 'SEH'] in result
    assert ['Shoreham-by-Sea', 'SSE'] in result
    assert ['Shortlands', 'SRT'] in result


def test_intermediate_upper():
    result = trie.search('TAL')
    assert len(result) == 3
    assert ['Talsarnau', 'TAL'] in result
    assert ['Talybont', 'TLB'] in result
    assert ['Tal-y-Cafn', 'TLC'] in result


def test_intermediate_mixed():
    result = trie.search('eWeLl')
    assert len(result) == 2
    assert ['Ewell East', 'EWE'] in result
    assert ['Ewell West', 'EWW'] in result


def test_full_lower():
    result = trie.search('formby')
    assert len(result) == 1
    assert ['Formby', 'FBY'] in result


def test_full_upper():
    result = trie.search('AYR')
    assert len(result) == 1
    assert ['Ayr', 'AYR'] in result


def test_full_mixed():
    result = trie.search('rUnCoRn eASt')
    assert len(result) == 1
    assert ['Runcorn East', 'RUE'] in result


def test_over_full_no_match():
    result = trie.search('AYRE')
    assert not result


def test_mid_match():
    result = trie.search('YSalisbury')
    assert not result


def test_space():
    result = trie.search('Small Heat')
    assert len(result) == 1
    assert ['Small Heath', 'SMA'] in result


def test_full_and_partial_match():
    result = trie.search('Derby')
    assert len(result) == 2
    assert ['Derby Road (Ipswich)', 'DBR'] in result
    assert ['Derby', 'DBY'] in result
