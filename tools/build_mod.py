"""Build Boss Courts from the installed v63 data without editing the game."""
import csv
import os
import copy
import json
import pathlib
import shutil

ROOT = pathlib.Path(__file__).resolve().parents[1]
GAME = pathlib.Path(os.environ.get('POKER_QUEST_DIR', r'E:\SteamLibrary\steamapps\common\Poker Quest'))
from release_paths import OUT, MOD

def table(name):
    with (GAME / 'csv' / (name + '.csv')).open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.reader(f))
    return rows[0], rows[1:]

MH, MR = table('MONSTERS')
RH, RR = table('WORLD_REGIONS')
MONSTERS = {r[0]: dict(zip(MH, r)) for r in MR}
REGIONS = {r[1]: dict(zip(RH, r)) for r in RR if r[1] in ['plains', 'swamp', 'desert', 'mountains', 'sea']}
QH, QR = table('QUERIES')
Q = {r[3]: r for r in QR if len(r) > 3}

def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    staging = path.with_suffix(path.suffix + '.tmp')
    with staging.open('w', encoding='ascii', newline='') as f:
        csv.writer(f, lineterminator='\n').writerows(rows)
    staging.replace(path)

def skill(source, slot):
    prefix = 'eq' + str(slot)
    return {k[len(prefix):]: v for k, v in MONSTERS[source].items() if k.startswith(prefix)}

def set_skill(monster, slot, fields):
    prefix = 'eq' + str(slot)
    for k in MH:
        if k.startswith(prefix):
            monster[k] = ''
    for suffix, value in fields.items():
        key = prefix + suffix
        if key in MH:
            monster[key] = str(value)

def clear_passives(monster):
    for k in MH:
        if k.startswith('Modifier ') or (len(k) > 1 and k[0] == 'm' and k[1].isdigit()):
            monster[k] = ''

def base(source, index, name, tip, region):
    x = copy.deepcopy(MONSTERS[source])
    x.update({'': name, 'ID': str(9700 + index), 'isEnabled': '1', 'isEndgame': '0',
              'guaranteedRuns': '', 'guaranteedMinColumns': '', 'displayName': name,
              'displayNamePossessive': name + "'s", 'isBoss': '1', 'Location': 'none',
              'isVisibleOnMap': '1', 'Spawn Weight': '1', 'specialTooltip': tip,
              'claimVictoryText': 'VICTORY! ' + name + ' has fallen. The road ahead is open.'})
    return {'data': x, 'source': source, 'region': region, 'tip': tip}

from boss_design_v14 import VERSION, create_bosses
bosses = create_bosses(MONSTERS, base, skill, set_skill, clear_passives)

def update_chances(x):
    visible = int(x['Visible Cards']); total = visible + int(x['Hidden Cards'])
    for i in range(1, 4):
        prefix = 'eq' + str(i)
        q = x[prefix + 'query']
        if not q: continue
        total_key = prefix + ('chance' if i == 2 else 'TotalChance')
        if q in Q:
            row = Q[q]
            x[prefix + 'VisibleChance'] = row[5 + visible]
            x[total_key] = row[5 + total]
        else:
            x[prefix + 'VisibleChance'] = '#N/A'; x[total_key] = '#N/A'

for b in bosses: update_chances(b['data'])

MOD.mkdir(parents=True, exist_ok=True)
write_csv(MOD / 'add' / 'MONSTERS.csv', [[b['data'].get(k, '') for k in MH] for b in bosses])

# Native combat-local event binding; never changes global ordinary battles.
WH, WR = table('WORLD_MODIFIERS')
stance = {k:'' for k in WH}
stance.update(id='9792',internalName='BC Thorn Stance',isEnabled='0',
              displayName='Thorn Stance (retired)',
              Description='Retired in 1.4.0. Thorn Reprisal uses a bounded native attack skill.')
assert all(k in WH for k in ('event1','effect1','e1p1','e1p2','event2','effect2','e2p1','e2p2'))
write_csv(MOD / 'add' / 'WORLD_MODIFIERS.csv', [[stance.get(k,'') for k in WH]])

# The native generator keeps the selected region object. Independent IDs allow
# guardian variants to reuse the ORIGINAL internal name and every asset path.
# Name-based lookups still find the first (original) row, whose ordinary pool is
# identical. No image copies, executable hooks, custom names or new biomes.
region_variants = []
for b in bosses:
    variant = copy.deepcopy(REGIONS[b['region']])
    variant['ID'] = str(9800 + int(b['data']['ID']) - 9700)
    variant['boss'] = b['data']['']
    region_variants.append(variant)
# All eligible rows get weight=1 at runtime. Four swamp candidates require
# four desert candidates to preserve World 2's original 50/50 biome selection.
# Retain an additional original Sandwyrm slot instead of inventing a guardian.
extra_desert = copy.deepcopy(REGIONS['desert'])
extra_desert['ID'] = '9890'
region_variants.append(extra_desert)
write_csv(MOD / 'add' / 'WORLD_REGIONS.csv',
          [[variant.get(k, '') for k in RH] for variant in region_variants])

# Restore the original tomb pools. Regional guardians must not leak into
# early catacomb encounters through the unrestricted chooseFromPool entry.
tomb_rows = []
for name in ['catacombs_medium', 'catacombs_hard']:
    original = next(r for r in RR if r[1] == name)
    tomb_rows.append(['SEARCH', name] + original)
write_csv(MOD / 'replace' / 'WORLD_REGIONS.csv', tomb_rows)

info = {
    'name': 'Boss Courts', 'version': VERSION, 'gameVersion': '63', 'gameBuild': '2021',
    'bosses': [{'name': b['data'][''], 'id': b['data']['ID'], 'asset': b['data']['asset'],
                'region': b['region'], 'source': b['source'], 'strategy': b['tip'],
                'chineseName': b['cn'], 'mechanics': b['mechanics'], 'counter': b['counter'],
                'origin': b['origin'], 'hpMultiplier': b['hpMultiplier']} for b in bosses],
    'worldGuardianCount': 5 + len(bosses), 'catacombsPoolSize': 5,
    'newBossesInCatacombs': False,
    'newRegions': 0, 'regionVariantRecords': len(region_variants),
    'newRegionNames': 0, 'bundledGameImages': 0, 'launcherRequired': False,
    'bossSelection': 'native CSV region variants with unique IDs and original names/assets',
    'regionVariants': [{'id':v['ID'],'region':v['name'],'boss':v['boss']} for v in region_variants],
    'biomeProbabilities': {'world1':{'plains':1},'world2':{'swamp':0.5,'desert':0.5},
                          'world3':{'mountains':0.5,'sea':0.5}},
    'runtimeStatus': 'pending',
}
(OUT / 'build-info.json').write_text(json.dumps(info, ensure_ascii=False, indent=2), encoding='utf-8')
print('Built', len(bosses), 'bosses;', len(region_variants),
      'same-name region variants; original assets; no launcher required at', MOD)
