REM THIS CREATES ALL RELEASE FILES CRUNCHED WITH EXOMIZER

cls
@echo off
set startadr=9000

For /f "tokens=1-4 delims=/:." %%a in ("%TIME%") do (
    SET HH24=%%a
    SET MI=%%b
)
echo %date% %HH24%:%MI%>timedate.clk


REM ---------------------------------------------------------------------
REM                           BUILD NORMAL VERSIONS
REM --------- %~1 --------- %~2 ------------ %~3 ---------- %~4 ---------
call:build64 "-D defset=1" "-D DEF_SIDFX=0" "-D DEF_REU=0" "normal"          
call:build64 "-D defset=2" "-D DEF_SIDFX=0" "-D DEF_REU=0" "1541u2cmd"       
call:build64 "-D defset=3" "-D DEF_SIDFX=0" "-D DEF_REU=0" "iec-cmd-ide64"   
call:build64 "-D defset=4" "-D DEF_SIDFX=0" "-D DEF_REU=0" "sd2iec"          
call:build64 "-D defset=5" "-D DEF_SIDFX=0" "-D DEF_REU=0" "1541u-netdrive"  
call:build64 "-D defset=6" "-D DEF_SIDFX=0" "-D DEF_REU=0" "chameleon-normal"
call:build64 "-D defset=7" "-D DEF_SIDFX=0" "-D DEF_REU=0" "chameleon-sd2iec"
mkdir "build\normal"
move /Y *.prg "build\normal"
move /Y *.o64 "build\normal"
move /Y *.log "build\normal"

REM ---------------------------------------------------------------------
REM                           BUILD REU VERSIONS
REM --------- %~1 --------- %~2 ------------ %~3 ---------- %~4 ---------
call:build64 "-D defset=1" "-D DEF_SIDFX=0" "-D DEF_REU=1" "reu-normal"          
call:build64 "-D defset=2" "-D DEF_SIDFX=0" "-D DEF_REU=1" "reu-1541u2cmd"       
call:build64 "-D defset=3" "-D DEF_SIDFX=0" "-D DEF_REU=1" "reu-iec-cmd-ide64"   
call:build64 "-D defset=4" "-D DEF_SIDFX=0" "-D DEF_REU=1" "reu-sd2iec"          
call:build64 "-D defset=5" "-D DEF_SIDFX=0" "-D DEF_REU=1" "reu-1541u-netdrive"  
mkdir "build\normal reu"
move /Y *.prg "build\normal reu"
move /Y *.o64 "build\normal reu"
move /Y *.log "build\normal reu"

REM ---------------------------------------------------------------------
REM                           BUILD SIDFX VERSIONS
REM --------- %~1 --------- %~2 ------------ %~3 ---------- %~4 ---------
call:build64 "-D defset=1" "-D DEF_SIDFX=1" "-D DEF_REU=0" "sfx-normal"          
call:build64 "-D defset=2" "-D DEF_SIDFX=1" "-D DEF_REU=0" "sfx-1541u2cmd"       
call:build64 "-D defset=3" "-D DEF_SIDFX=1" "-D DEF_REU=0" "sfx-iec-cmd-ide64"   
call:build64 "-D defset=4" "-D DEF_SIDFX=1" "-D DEF_REU=0" "sfx-sd2iec"          
call:build64 "-D defset=5" "-D DEF_SIDFX=1" "-D DEF_REU=0" "sfx-1541u-netdrive"  
mkdir "build\sidfx"
move /Y *.prg "build\sidfx"
move /Y *.o64 "build\sidfx"
move /Y *.log "build\sidfx"


REM ---------------------------------------------------------------------
REM                           BUILD SIDFX REU VERSIONS
REM --------- %~1 --------- %~2 ------------ %~3 ---------- %~4 ---------
call:build64 "-D defset=1" "-D DEF_SIDFX=1" "-D DEF_REU=1" "sfx-reu-normal"          
call:build64 "-D defset=2" "-D DEF_SIDFX=1" "-D DEF_REU=1" "sfx-reu-1541u2cmd"       
call:build64 "-D defset=3" "-D DEF_SIDFX=1" "-D DEF_REU=1" "sfx-reu-iec-cmd-ide64"   
call:build64 "-D defset=4" "-D DEF_SIDFX=1" "-D DEF_REU=1" "sfx-reu-sd2iec"          
call:build64 "-D defset=5" "-D DEF_SIDFX=1" "-D DEF_REU=1" "sfx-reu-1541u-netdrive"  
mkdir "build\sidfx reu"
move /Y *.prg "build\sidfx reu"
move /Y *.o64 "build\sidfx reu"
move /Y *.log "build\sidfx reu"

goto end

REM ---------------------------------------------------------------------
REM             Function compiles with 64tass and crunches with Exomizer
REM ---------------------------------------------------------------------
REM 64tass -D defset=1 -D DEF_SIDFX=0 -D DEF_REU=0 --m6502 -a sidplay64.tas -o sidplay64-normal.o64
REM
:build64
64tass %~1 %~2 %~3 --m6502 -l _sp64labels-%~4.log -L _sp64list-%~4.log -a sidplay64.tas -o sidplay64-%~4.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
rem pucrunch -x$%startadr% sidplay64-%~4.o64 sidplay64-%~4.prg
exomizer sfx $%startadr% -n sidplay64-%~4.o64 -o sidplay64-%~4.prg
goto:eof

:end

echo -
echo --
echo Sidplay64 builds completed successfully!
echo --
echo -