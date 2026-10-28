; TEST42 -- SD2IEC feasibility probe. TWO ORIGINAL PSID files, no Krill.
; Does IEC KERNAL CHRIN work while a $1003 SID IRQ plays?
; Disc directory: 00player.prg (this), 01.sid and 02.sid (original PSID bytes).
; Palette: BLUE=first SID, YELLOW=streaming second by IEC, GREEN=staged,
; LIGHT GREEN=second SID playing, RED=load failed.
; After 2 seconds in GREEN, automatically transition to SID 2.
; Reproduction cadence: PAL ~50Hz. VICE and SD2IEC physical PASS not claimed.
; Source music: original, unchanged PSID v2 $1000/$1000/$1003. Only sizes differ.
;
; BASiC 10 SYS2061
* = $0801
.word $080b
.word 10
.byte $9e
.text "2061"
.byte 0
.word 0

* = $080d
start:
        lda #0
        sta music_on
        lda #$37
        sta $01                     ; KERNAL ROM+I/O for real IEC access
        lda #6
        sta $d020
        lda #<name1
        sta fnameptr
        lda #>name1
        sta fnameptr+1
        lda #<$080f
        sta destination
        ; Set actual music load destination $1000
        lda #<$1000
        sta destination
        lda #>$1000
        sta destination+1
        lda #<2063                 ; 009_005_apyd.sid original body
        sta remains
        lda #>2063
        sta remains+1
        jsr load_psid_bytes
        bcc song1_loaded
        jmp io_fail

song1_loaded:
        jsr init_music
        sei
        lda #<music_irq
        sta $0314
        lda #>music_irq
        sta $0315
        lda #1
        sta music_on
        cli
        lda #6
        sta $d020

        lda #<name2
        sta fnameptr
        lda #>name2
        sta fnameptr+1
        lda #<$5000
        sta destination
        lda #>$5000
        sta destination+1
        lda #<2226                 ; 016_012_chic.sid original body
        sta remains
        lda #>2226
        sta remains+1
        lda #7
        sta $d020
        jsr load_psid_bytes
        bcc song2_staged
        jmp io_fail

song2_staged:
        lda #5
        sta $d020
        lda #0
        sta frames_lo
        sta frames_hi
wait_2sec:
        lda frames_hi
        bne transition
        lda frames_lo
        cmp #100
        bcc wait_2sec

transition:
        sei
        lda #0
        sta music_on
        ; ONLY the required 2226 bytes, no fixed 8KB blanking.
        ; IRQ remains off during overwrite of executing first SID.
        lda $fb
        sta saved_fb
        lda $fc
        sta saved_fc
        lda $fd
        sta saved_fd
        lda $fe
        sta saved_fe
        lda #0
        sta $fb
        sta $fd
        lda #$50
        sta $fc
        lda #$10
        sta $fe
        lda #<2226
        sta remains
        lda #>2226
        sta remains+1
        ldy #0
copy_loop:
        lda ($fb),y
        sta ($fd),y
        inc $fb
        bne copy_src_ok
        inc $fc
copy_src_ok:
        inc $fd
        bne copy_dst_ok
        inc $fe
copy_dst_ok:
        lda remains
        bne copy_dec
        dec remains+1
copy_dec:
        dec remains
        lda remains
        ora remains+1
        bne copy_loop

        lda saved_fb
        sta $fb
        lda saved_fc
        sta $fc
        lda saved_fd
        sta $fd
        lda saved_fe
        sta $fe

        ; Fresh tune INIT at original address; no SID bytes patched.
        jsr init_music
        lda #1
        sta music_on
        cli
        lda #13
        sta $d020
play_forever:
        jmp play_forever

io_fail:
        lda #2
        sta $d020
        ; If first tune started, it continues playing (no fake PASS).
fail_forever:
        jmp fail_forever

; Read exact original PSID header + load word (126 bytes), then body.
; No 1541 drive code uploaded, no Krill. KERNAL CHRIN with IRQ enabled.
; Inputs: fnameptr, destination, remains.
load_psid_bytes:
        lda #6
        ldx fnameptr
        ldy fnameptr+1
        jsr $ffbd                    ; SETNAM
        lda #2
        ldx #8
        ldy #0
        jsr $ffba                    ; SETLFS 2,8,0
        jsr $ffc0                    ; OPEN
        bcc open_ok
        sec
        rts
open_ok:
        ldx #2
        jsr $ffc6                    ; CHKIN
        bcc input_ok
        lda #2
        jsr $ffc3                    ; CLOSE
        sec
        rts
input_ok:
        lda #126
        sta bytes_skip
skip_psid_header:
        jsr $ffcf                    ; CHRIN, unchanged PSID data
        dec bytes_skip
        bne skip_psid_header
        lda destination
        sta store_byte+1
        lda destination+1
        sta store_byte+2
read_music:
        jsr $ffcf                    ; CHRIN, interrupts remain ON
store_byte:
        sta $5000
        inc store_byte+1
        bne no_store_carry
        inc store_byte+2
no_store_carry:
        lda remains
        bne dec_remaining
        dec remains+1
dec_remaining:
        dec remains
        lda remains
        ora remains+1
        bne read_music
        jsr $ffcc                    ; CLRCHN
        lda #2
        jsr $ffc3                    ; CLOSE
        clc
        rts

; Separate music ZP state from KERNAL/IEC ZP while streaming.
; Swap bytes $02..$FF. DO NOT replace $00/$01 memory mapping.
init_music:
        ldx #$fd
save_kernal_for_init:
        lda $02,x
        sta kernal_zp,x
        dex
        bpl save_kernal_for_init
        lda #0                     ; subtune index 0
        tax
        tay
        jsr $1000
        ldx #$fd
capture_music_init:
        lda $02,x
        sta music_zp,x
        lda kernal_zp,x
        sta $02,x
        dex
        bpl capture_music_init
        rts

; Hook the KERNAL IRQ RAM vector. No ROM bank switching during CHRIN.
music_irq:
        pha
        txa
        pha
        tya
        pha
        inc frames_lo
        bne frame_ok
        inc frames_hi
frame_ok:
        lda music_on
        beq end_music_irq
        ldx #$fd
swap_to_music:
        lda $02,x
        sta kernal_zp,x
        lda music_zp,x
        sta $02,x
        dex
        bpl swap_to_music
        jsr $1003
        ldx #$fd
restore_kernal:
        lda $02,x
        sta music_zp,x
        lda kernal_zp,x
        sta $02,x
        dex
        bpl restore_kernal
end_music_irq:
        pla
        tay
        pla
        tax
        pla
        jmp $ea31                   ; normal KERNAL IRQ tail + RTI

name1:       .text "01.sid"
name2:       .text "02.sid"
fnameptr:    .word 0
destination: .word 0
remains:     .word 0
bytes_skip:  .byte 0
music_on:    .byte 0
frames_lo:   .byte 0
frames_hi:   .byte 0
saved_fb:    .byte 0
saved_fc:    .byte 0
saved_fd:    .byte 0
saved_fe:    .byte 0
music_zp:    .fill 254,0
kernal_zp:   .fill 254,0
.cerror *>$1000, "TEST42 probe overlaps original SID load base $1000"
