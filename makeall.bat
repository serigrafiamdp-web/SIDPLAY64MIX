rem THIS batch file compiles all files and quickly packs them with pucrcunch
cls
@echo off
set startadr=9000

For /f "tokens=1-4 delims=/:." %%a in ("%TIME%") do (
    SET HH24=%%a
    SET MI=%%b
)
echo %date% %HH24%:%MI%>timedate.log

64tass.exe --m6502 -l _s64labels-normal.log -L _s64list-normal.log -D defset=1 -a sidplay64.tas -o sidplay64-normal.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-normal.o64 sidplay64-normal.prg

64tass.exe --m6502 -l _s64labels-1541u2cmd.log -L _s64list-1541u2cmd.log -D defset=2 -a sidplay64.tas -o sidplay64-1541u2cmd.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-1541u2cmd.o64 sidplay64-1541u2cmd.prg

64tass.exe --m6502 -l _s64labels-iec-cmd-ide64.log -L _s64list-iec-cmd-ide64.log -D defset=3 -a sidplay64.tas -o sidplay64-iec-cmd-ide64.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-iec-cmd-ide64.o64 sidplay64-iec-cmd-ide64.prg

64tass.exe --m6502 -l _s64labels-sd2iec.log -L _s64list-sd2iec.log -D defset=4 -a sidplay64.tas -o sidplay64-sd2iec.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-sd2iec.o64 sidplay64-sd2iec.prg

64tass.exe --m6502 -l _s64labels-1541u-netdrive.log -L _s64list-1541u-netdrive.log -D defset=5 -a sidplay64.tas -o sidplay64-1541u-netdrive.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-1541u-netdrive.o64 sidplay64-1541u-netdrive.prg

c1541.exe < c1541.mak
