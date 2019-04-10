from transport.trie import Trie
import csv
from importlib import resources

trie = Trie()


def setup_module():
    with resources.open_text('config', 'station_codes.csv') as stations:
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
    assert len(result) == 0


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
    assert len(result) == 0


def test_empty():
    result = trie.search('')
    assert len(result) == 2570
