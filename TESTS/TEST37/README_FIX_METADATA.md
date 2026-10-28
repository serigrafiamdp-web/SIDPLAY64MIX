# TEST37 — Refresh PSID cover on automatic song changes

## User symptom
- Songs loaded from the FACIL gallery play under TEST35.
- On automatic NEXT, audio changes, but Glenn SIDPLAY64 keeps old song title, artist, date and other PSID metadata.

## Root cause
`mix10_stage_pending` loads the next original PSID through Krill into $5350, then copies the executable body from $53CC to bank $5000. The copy overwrites the header in $5350; TEST35 switches only the music bank, never the header or displayed metadata.

## Fix, scoped to UI metadata
1. `mix37_capture_header` caches bytes 00..7B of the next PSID at reserved $3E00..$3E7B, before copying to the music bank. The bytes 'P','S' are reconstructed from the PSID magic because Krill interpreted them as a PRG load address and placed the remaining bytes at $5350.
2. `mix37_commit_metadata` refreshes Glenn UI **only at the song boundary**, not during prefetch. It uses the same coordinates as `doheaderstuff` for name, author, release, chip model, PAL/NTSC, INIT and PLAY address. It also updates subtune and speed data.
3. Never invoke `doheaderstuff` on NEXT: that code includes relocator and stack jump, not only UI painting.
4. The C64 memory mapping is restored after drawing; the 5-second Krill prefetch, interrupted music handling and files are unchanged.
5. Diagnostic `$3FFE=$71` means header captured, `$3FFF=$72` means refreshed song cover.

## Current test assets
- `SIDPLAY64MIX_TEST37.D64` contains the same original 19 SID sectors as the working master. It is a **regression test** of the cover refresh, not yet a D64 containing the 72 gallery songs.
- Do not label as functional PASS until VICE shows the cover follows each playing SID without audio issues.

## VICE test
1. Load TEST37 in a fresh VICE session.
2. Select SID #1, wait for 5-second prefetch, then automatic transition to SID #2.
3. Verify **both music AND title/author/release** change. Repeat with 2->3 and 19->1 if desired.
4. Monitor after transition: `m $3ff0 $3fff`. Expect `$3FFE=$71`, `$3FFF=$72` after successful precache and metadata commit.
5. Regression: no microcuts, M/N keys keep working.

## Future separate work
The new FACIL library contains 72 records matching the current core LOAD=$1000 INIT=$1000 PLAY=$1003. Support for different LOAD/INIT/PLAY and RSID needs a separate test. Also future tests should track runtime metadata for duration and actual payload end address, rather than assuming static 19-song map.

MASTER TEST35 and original TEST19 are untouched.
