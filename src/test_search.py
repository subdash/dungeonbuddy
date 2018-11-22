import requests

from retrieval import *


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
    search_eb = r.get_result_obj('eldritch blast')
    p = Parser(search_eb)
    p.gather_attributes()
    assert p.details['title'] == 'Eldritch Blast | D&D 5th Edition on Roll20 Compendium'
    assert p.details['Casting Time'] == '1 action'
    assert p.details['Range'] == '120 feet'
    assert p.details['Components'] == 'V S'
    assert p.details['Duration'] == 'Instantaneous'
    assert p.details['Classes'] == 'Warlock'

    print('test_parser PASS')


def test_dungeonbuddy():
    db = DungeonBuddy()
    assert db.get_result('eldritch blast') == '{"title": "Eldritch Blast | D&D 5th Edition on Roll20 Compendium", "Casting Time": "1 action", "Classes": "Warlock", "Components": "V S", "Duration": "Instantaneous", "Level": "0", "Name": "Eldritch Blast", "Range": "120 feet", "School": "Evocation", "Spell Attack": "Ranged", "Target": "A creature within range", "description": "A beam of crackling energy streaks toward a creature within range. Make a ranged spell Attack against the target. On a hit, the target takes 1d10 force damage.The spell creates more than one beam when you reach higher levels: two beams at 5th level, three beams at 11th level, and four beams at 17th level. You can direct the beams at the same target or at different ones. Make a separate Attack roll for each beam."}'
    assert db.get_result('eldritch') == '[{"Eldritch Blast": {"title": "Eldritch Blast | D&D 5th Edition on Roll20 Compendium", "Casting Time": "1 action", "Classes": "Warlock", "Components": "V S", "Duration": "Instantaneous", "Level": "0", "Name": "Eldritch Blast", "Range": "120 feet", "School": "Evocation", "Spell Attack": "Ranged", "Target": "A creature within range"}}, {"Eldritch Master": {"title": "Warlock | D&D 5th Edition on Roll20 Compendium", "Hit Die": "d8", "Spellcasting Ability": "Charisma", "Starting Gold": "4d4 x 10", "Subclass Name": "Otherworldly Patron", "Suggested Abilities": "Charisma, Consitution"}}, {"Eldritch Sight": {"title": "Warlock | D&D 5th Edition on Roll20 Compendium", "Hit Die": "d8", "Spellcasting Ability": "Charisma", "Starting Gold": "4d4 x 10", "Subclass Name": "Otherworldly Patron", "Suggested Abilities": "Charisma, Consitution"}}, {"Eldritch Spear": {"title": "Warlock | D&D 5th Edition on Roll20 Compendium", "Hit Die": "d8", "Spellcasting Ability": "Charisma", "Starting Gold": "4d4 x 10", "Subclass Name": "Otherworldly Patron", "Suggested Abilities": "Charisma, Consitution"}}]'

    print('test_dungeonbuddy PASS')

if __name__ == '__main__':
    test_search_paladin()
    test_search_eldritch()
    test_parser()
    test_dungeonbuddy()
