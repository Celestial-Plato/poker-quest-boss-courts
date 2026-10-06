"""Update Boss Courts data and apply the shipped loader without launching the game."""
from pathlib import Path
import contextlib
import csv
import datetime
import io
import json
import os
import runpy
import shutil
import hashlib
import ctypes as c
from ctypes import wintypes as w

ROOT=Path(__file__).resolve().parent
OUT=ROOT
SOURCE=OUT/'content'/'BossCourts'
GAME=Path(r'E:\SteamLibrary\steamapps\common\Poker Quest')
PROFILE=Path(os.environ['APPDATA'])/'Playsaurus'/'PokerQuest'
DEST=PROFILE/'mods'/'BossCourts'
assert DEST.is_dir(), 'Expected existing BossCourts installation'
assert (PROFILE/'mods'/'mods.txt').read_text().splitlines()==['BossCourts'], 'Unexpected enabled mods; inspect before applying'
class ProcessEntry(c.Structure):
    _fields_=[('size',w.DWORD),('usage',w.DWORD),('pid',w.DWORD),('heap',c.c_size_t),
              ('module',w.DWORD),('threads',w.DWORD),('parent',w.DWORD),('priority',w.LONG),
              ('flags',w.DWORD),('name',w.WCHAR*260)]
kernel=c.WinDLL('kernel32',use_last_error=True)
kernel.CreateToolhelp32Snapshot.restype=w.HANDLE
kernel.Process32FirstW.argtypes=[w.HANDLE,c.POINTER(ProcessEntry)]
kernel.Process32NextW.argtypes=[w.HANDLE,c.POINTER(ProcessEntry)]
kernel.CloseHandle.argtypes=[w.HANDLE]
snapshot=kernel.CreateToolhelp32Snapshot(2,0)
assert snapshot!=c.c_void_p(-1).value, 'Could not check whether the game is running'
entry=ProcessEntry();entry.size=c.sizeof(entry)
try:
    available=kernel.Process32FirstW(snapshot,c.byref(entry))
    while available:
        assert entry.name.lower()!='pokerquest.exe', 'Close Poker Quest before updating'
        available=kernel.Process32NextW(snapshot,c.byref(entry))
finally:kernel.CloseHandle(snapshot)
backup=ROOT/'backups'/('before-update-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
files=('add/MONSTERS.csv','add/WORLD_REGIONS.csv','add/WORLD_MODIFIERS.csv','replace/WORLD_REGIONS.csv',
       'README.en.md','README.zh-CN.md','TESTING.zh-CN.md','CHANGELOG.zh-CN.md',
       'DESIGN.zh-CN.md','metadata.json')
assert all((SOURCE/rel).is_file() for rel in files), 'Incomplete update package'
save_hashes={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PROFILE.glob('*.sol')}
for rel in files:
    target=DEST/rel
    assert target.resolve().is_relative_to(DEST.resolve())
    if target.exists():
        (backup/rel).parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(target,backup/rel)
for name in ('MONSTERS','WORLD_REGIONS','WORLD_MODIFIERS'):
    path=PROFILE/'modded_csvs'/'csv'/(name+'.csv')
    if path.exists():
        (backup/'applied').mkdir(parents=True,exist_ok=True)
        shutil.copy2(path,backup/'applied'/path.name)
for rel in files:
    (DEST/rel).parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(SOURCE/rel,DEST/rel)

original_rmtree=shutil.rmtree
allowed_delete=[PROFILE/'modded_csvs'/'csv',PROFILE/'modded_imgs',PROFILE/'backup_csvs'/'csv']
def checked_rmtree(path,*args,**kwargs):
    resolved=Path(path).resolve()
    assert any(resolved==x.resolve() for x in allowed_delete), 'Unexpected deletion target: '+str(resolved)
    return original_rmtree(path,*args,**kwargs)
original_startfile=os.startfile
previous_cwd=Path.cwd()
log=io.StringIO()
try:
    shutil.rmtree=checked_rmtree
    os.startfile=lambda path: None
    os.chdir(GAME)
    with contextlib.redirect_stdout(log):
        runpy.run_path(str(GAME/'modLoader.py'),run_name='__main__')
finally:
    shutil.rmtree=original_rmtree
    os.startfile=original_startfile
    os.chdir(previous_cwd)
(ROOT/'installed-loader.log').write_text(log.getvalue(),encoding='utf-8')
with (PROFILE/'modded_csvs'/'csv'/'MONSTERS.csv').open(encoding='utf-8-sig',newline='') as f:
    applied=list(csv.DictReader(f))
info=json.loads((OUT/'build-info.json').read_text(encoding='utf-8'))
for boss in info['bosses']:
    row=next(r for r in applied if r['ID']==boss['id'])
    assert row['']==row['displayName']==boss['name']
def regions(path):
    with path.open(encoding='utf-8-sig',newline='') as f:
        return {r['name']:r for r in csv.DictReader(f)}
original_regions=regions(GAME/'csv'/'WORLD_REGIONS.csv')
applied_regions=regions(PROFILE/'modded_csvs'/'csv'/'WORLD_REGIONS.csv')
for pool in ('catacombs_medium','catacombs_hard'):
    assert applied_regions[pool]==original_regions[pool], 'Tomb pool differs from the original game: '+pool
assert not any(name.startswith('bc_') for name in applied_regions), 'Legacy region names remain enabled'
for name,row in applied_regions.items():
    if row['minWorld'] in ('1','2','3'):
        for tile in ('top','top_left','top_right','bottom','bottom_left','bottom_right',
                     'center','center_left','center_right'):
            assert (GAME/'mapTiles'/name/(tile+'.png')).is_file(), 'Missing native terrain: '+name+'/'+tile
assert save_hashes=={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in PROFILE.glob('*.sol')}, 'Save files changed'
print(json.dumps({'synced':[{b['id']:b['name']} for b in info['bosses']],
                  'version':info['version'],'catacombsRestored':True,
                  'legacyRegionNamesRemoved':True,'nativeTerrainPathsVerified':True,
                  'backup':str(backup),'restartRequired':True,'newRunRequired':True,'savesModified':False},indent=2))
