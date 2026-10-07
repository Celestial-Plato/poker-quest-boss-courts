# Boss Courts 1.4.0

## Upgrading an existing Workshop installation

The native Mod Manager can retain an old local copy after Steam downloads an update. Resubscribing or toggling the mod may still load the old data. A first-time installation without a local copy does not need this cleanup.

1. Close the game. In Mod Manager, open Boss Courts **Details → Delete Mod** and confirm. This removes the local mod copy, not saves. Keep your Workshop subscription.
2. Close and reopen Mod Manager so it imports Boss Courts from Steam's updated download.
3. Enable Boss Courts again. If using Travel Run, keep Travel Run enabled. Enable only one copy of Boss Courts.
4. Click **Run Game** to apply and launch, then start a new run.

In 1.4.0, Ashwing's World 1 periodic Enflame is 5; the left/right ability images are Flare / Firestorm. The middle fire image is unchanged. The manager's Game Version column shows game compatibility, not the mod version.


Adds 13 regional bosses using existing Poker Quest artwork. Original guardians and final Jokers remain; new bosses are excluded from normal encounters and catacombs.

Subscribe, enable and apply in the game's Mod Manager, restart and start a NEW RUN. Disable Random Bosses. Enable only one copy of Boss Courts.
Use the normal game executable. No custom launcher, executable patch or bundled game images are required.
Upgrading changes the region selection table, so old runs may recalculate their regions and bosses; begin a new run.

The CSV adds guardian variants with unique IDs and unchanged native region names. All other region fields remain original. World count, biome names, normal enemies, towns, music and map generation rules remain. Swamp/Desert and Mountains/Sea each retain 50/50 biome selection. Great Sandwyrm has two of the four desert slots; the other two contain Three Kings and Obsidian Smith. Other regional candidates have equal slots.

Version 1.4.0 recalibrates all 13 bosses with 26 native hero HP profiles, wounded entry and three assumed damage bands. These are sensitivity models, not measured class DPS or win rates. Old Thorn uses one native attack on each even boss turn: 10% of its own missing life, capped at MBD*0.11 (base World 2 cap: 8); normal Block applies. This is a scheduled reprisal, not immediate per-hit reflection. Full combat balance testing remains pending. Native startup, data loading and regional boss generation passed in an isolated profile. Full map rendering and thirteen complete combats still require gameplay testing. Please report bugs and balance issues in the Workshop comments, including boss, hero, difficulty and equipment.

Art belongs to Playsaurus. Some portraits are already used in the base game; others are dormant or portrait-only resources. Workshop images use the approved nine-boss cover and English-name portrait gallery.
