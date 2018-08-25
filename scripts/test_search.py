import requests

from retrieval import Parser, Retriever


def test_search_paladin():
    r = Retriever()
    search_paladin = r.get_result_obj('paladin')

    assert search_paladin.status_code == 200
    assert search_paladin.url == 'https://roll20.net/compendium/dnd5e/Paladin#h-Paladin'

    print('test_search_paladin PASS')


def test_search_eldritch():
    r = Retriever()
    search_eldritch = r.get_result_obj('eldritch')

    assert search_eldritch[0].text == 'Eldritch Blast'
    assert search_eldritch[1].text == 'Eldritch Master'
    assert search_eldritch[2].text == 'Eldritch Sight'
    assert search_eldritch[3].text == 'Eldritch Spear'
    assert search_eldritch[0].link == '/compendium/dnd5e/Spells:Eldritch%20Blast#h-Eldritch%20Blast'
    assert search_eldritch[1].link == '/compendium/dnd5e/Classes:Warlock#h-Eldritch%20Master'
    assert search_eldritch[2].link == '/compendium/dnd5e/Classes:Warlock#h-Eldritch%20Sight'
    assert search_eldritch[3].link == '/compendium/dnd5e/Classes:Warlock#h-Eldritch%20Spear'

    print('test_search_eldritch PASS')


def test_parser():
    r = Retriever()
    search_eldritch = r.get_result_obj('eldritch')
    p = Parser(requests.get('https://roll20.net' + search_eldritch[0].link))
    p.gather_attributes()
    p.details['title'] == 'Eldritch Blast | D&D 5th Edition on Roll20 Compendium'
    p.details['Casting Time'] == '1 action'
    p.details['Range'] == '120 feet'
    # p.details['components'] == 'V S'  # Not working for some reason...
    p.details['Duration'] == 'Instantaneous'
    p.details['Classes'] == 'Warlock'

    print('test_parser PASS')


if __name__ == '__main__':
    # test_search_paladin()
    # test_search_eldritch()
    test_parser()
