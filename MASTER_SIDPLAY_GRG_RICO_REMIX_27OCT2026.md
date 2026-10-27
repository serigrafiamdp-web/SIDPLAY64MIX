# MASTER SIDPLAY GRG - RICO REMIX — 27 OCT 2026

Baseline frozen from `test/test11-glenn-krill-prefetch-0100`, commit `0cfcfadbc95518c9fab6b8923303e4c56d9a51a5`.
Original SIDPLAY64 v1.21 UI by Glenn Rune Gallefoss; KrillLoad double-buffer symbiont by Rico Remix.
User tested TEST11 D64 in VICE, reported **éxito**; it stages its next tune at **01:00** of Glenn's TOD counter. Original code and compiled build recorded in GitHub workflow run **40449505236** (success). The prior TEST05/06/07 milestone branches remain unchanged.

**Important limitation:** current Krill symbiont is a deliberately **hardcoded three-song loop** MINIMERCADO -> CHACABEZA -> COMEME -> MINIMERCADO (not the 19-entry directory). This was observed by user after initial PASS and verified in `src/mix10_glenn_symbiont.tas` (`mix10_current`, `mix10_load_b/c`, compare 3, names MIX_B/MIX_C/MIX_A2). It is therefore a **progress master only**, not a general-purpose complete playlist implementation. No generalized non-3-song cycle, per-track timer config, or editable playlist files have passed VICE yet.

**Later design idea, not implemented:** save a user configuration/playlist file with custom SID end time (current approximate timer can be overridden per tune), keeping Glenn's selection workflow and synchronizing Krill prefetch to the selected next tune.

Next experimental branch should copy this master exactly and broaden to 8 compatible SID in chronological directory order, using fixed $1000 INIT and $1003 PLAY, 19-page stage. This requires independent VICE validation. Do not change this branch as a side effect of later tests.

This branch contains the immutable source. Associated approved D64: `TEST11.d64` previously furnished in chat, SHA256 to be independently verified for the saved binary rather than inferred from source.