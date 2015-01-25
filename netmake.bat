cls
@echo off
set startadr=9000

For /f "tokens=1-4 delims=/:." %%a in ("%TIME%") do (
    SET HH24=%%a
    SET MI=%%b
)
echo %date% %HH24%:%MI%>timedate.log

64tass.exe --m6502 -l _s64labels-sd2iec.log -L _s64list-sd2iec.log -D defset=4 -a sidplay64.tas -o boot.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
rem slh_ult.exe boot.o64 boot.prg %startadr% sys
rem exomizer sfx $%startadr% -n boot.o64 -o boot.prg
pucrunch -x$%startadr% boot.o64 boot.prg

c1541.exe < c1541.mak

codenet -n 192.168.80.64 -w boot.prg
codenet -n 192.168.80.64 -e $080d

rem defset=1 - normal 1541 build
rem defset=2 - 1541u2cmd build
rem defset=3 - iec,ide64,cmd fd,hd,rl,rd build
rem defset=4 - sd2iec build
rem defset=5 - 1541u1, netdrive build
rem defset=6 - 1541u2siec build (can the 1541u2 operate in standalone mode?)