cls
@echo off
set startadr=9000

For /f "tokens=1-4 delims=/:." %%a in ("%TIME%") do (
    SET HH24=%%a
    SET MI=%%b
)
echo %date% %HH24%:%MI%>timedate.log


REM --------- %~1 --------- %~2 ------------ %~3 ---------- %~4 ---------
call:build64 "-D defset=1" "-D DEF_SIDFX=0" "-D DEF_REU=0" "normal"          
call:build64 "-D defset=4" "-D DEF_SIDFX=0" "-D DEF_REU=0" "sd2iec"          
call:build64 "-D defset=2" "-D DEF_SIDFX=0" "-D DEF_REU=0" "1541u2cmd"       
goto:end
call:build64 "-D defset=3" "-D DEF_SIDFX=0" "-D DEF_REU=0" "iec-cmd-ide64"   
call:build64 "-D defset=5" "-D DEF_SIDFX=0" "-D DEF_REU=0" "1541u-netdrive"  
call:build64 "-D defset=6" "-D DEF_SIDFX=0" "-D DEF_REU=0" "chameleon-normal"
call:build64 "-D defset=7" "-D DEF_SIDFX=0" "-D DEF_REU=0" "chameleon-sd2iec"


goto:end


REM ---------------------------------------------------------------------
REM             Compile with 64tass and crunch with pucrunch
REM ---------------------------------------------------------------------
REM 64tass -D defset=1 -D DEF_SIDFX=0 -D DEF_REU=0 --m6502 -a sidplay64.tas -o sidplay64-normal.o64
REM
:build64
64tass %~1 %~2 %~3 --m6502 -l _sp64labels-%~4.log -L _sp64list-%~4.log -a sidplay64.tas -o sidplay64-%~4.o64
if %errorlevel% neq 0 exit /b %errorlevel% 
pucrunch -x$%startadr% sidplay64-%~4.o64 sidplay64-%~4.prg
goto:eof

:end
c1541.exe < c1541.mak
