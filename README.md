# Dungeon Buddy

## What is Dungeon Buddy?
Dungeon Buddy is a D&D pet project that is currently still in the works.

**What is here right now**

- A basic API that can pull data from the [Dungeons & Dragons 5th Edition compendium at roll20.net](https://roll20.net/compendium/)
- A single basic test that is about as extensive as the API is

**What is planned**

A web app or mobile app where you can...
- Make and store a character sheet
- Easily access skills, spells, and any information a player or DM could need
- User roles (player, dungeon master, etc.)
- Much, much more

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
