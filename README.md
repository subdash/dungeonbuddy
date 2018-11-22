# Dungeon Buddy

## What is this?
A web scraper that can pull data from the Dungeons & Dragons 5th Edition compendium at [roll20.net](https://roll20.net/compendium/)

**Quick Demo**

```
>>> from retrieval import *
>>> db = DungeonBuddy()
>>> eldritch_blast = db.get_result('eldritch blast')
>>> eldritch_blast
'{"title": "Eldritch Blast | D&D 5th Edition on Roll20 Compendium", "Casting Time": "1 action", "Classes": "Warlock", "Components": "V S", "Duration": "Instantaneous", "Level": "0", "Name": "Eldritch Blast", "Range": "120 feet", "School": "Evocation", "Spell Attack": "Ranged", "Target": "A creature within range"}'
>>> eldritch_blast = json.loads(eldritch_blast)
>>> eldritch_blast['Casting Time']
'1 action'
>>> eldritch_blast['Duration']
'Instantaneous'
```
