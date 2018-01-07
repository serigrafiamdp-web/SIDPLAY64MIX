cls

rem THIS DELETES ALL BUILD and TEMPORARY FILES

del *.prg
del *.o64
del *.log
del test.d64

rem DELETES BUILD DIRECTORY IF IT EXIST

IF EXIST "build" RD /S /Q "build"
