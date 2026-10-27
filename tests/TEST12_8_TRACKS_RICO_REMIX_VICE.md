# TEST12 — GRG RICO REMIX: 8 SONGS ON GLENN UI

Experimental extension based **strictly on frozen TEST11 VICE PASS**.
MASTER: `MASTER-SIDPLAY-GRG-RICO-REMIX`, snapshot `milestone/TEST11_VICE_PASS_KRILL_0100_27OCT2026`.

**What changed:** `src/mix10_glenn_symbiont.tas` maps the fixed
Krill song ring from three to eight SID, in the exact first-eight order
of the existing 19-SID Glenn directory. Still uses native Glenn's UI,
timer and playlist cursor; still starts disk prefetch when original CIA TOD
passes 01:00. No user-definable end timestamps yet.

The eight tunes (and staged bank filenames):

1. MINIMERCADO.SID → initial loaded with Glenn, restart via MIX_A2
2. CHACABEZA.SID → MIX_B
3. COMEME (1).SID → MIX_C
4. DATASETTE.SID → MIX_D
5. DROGACUMBIA.SID → MIX_E
6. ESPACIAL.SID → MIX_F
7. CARA.SID → MIX_G
8. MATRACA3.SID → MIX_H

At H returns to A. TEST11 cycle A/B/C remains untouched on its frozen branch.

**Technical scope:** all eight are PSID v2 with explicit payload load
address $1000, INIT $1000, PLAY $1003, binary body at most 19*256 bytes.
Zero-pad staged payload to exactly 4864 bytes; each MIX_x PRG has load
address $5000 plus 4864 bytes of data (4866 bytes total).
All 19 original PSID directory files retained byte-for-byte.
GLENN compiled natively with 64tass/PuCrunch from TEST12 branch.

**Build:** https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40454195397 (PASS).
**D64:** `TEST12_8_SIDS.d64`, SHA256
`76398dcdbe79e57d94080e4004863b909802873f0115094121ad19db54a56405`
174848 bytes, 32 PRG entries, four disk directory sectors,
all file chains validated and re-read, 103 free data sectors.
All previous 3 staged PRGs, BOOT, SYMBIONT, Krill installer, resident
and 19 original PSID files are byte-for-byte unchanged.

**VICE not yet validated.** This is a wider test of 8, not yet
a generalized dynamic directory playlist. For future iterations,
support the entire directory with load/init/play/size-aware staging.
A separate later enhancement under discussion is a saved playlist
configuration with explicit end time for each SID.
