SIDPLAY64 version number 1.21

The source files.

This is a native sidplayer for the commodore 64.
It will play songs at correct ntsc or pal speed.
It will work many different devices such as:
REU, 1541u1, 1541u2, sd2iec, iec2ata, 1541/1571/1581, cmd fd/hd/ramlink/ramdrive,
IDE64(+ pclink), Chameleon and more +++


You need 64tass, exomizer 2.x, pucrunch in your path.
You possibly want to have codenet, c1541 in your path.

Make builds uses ms-dos batch 
functions like : ren, del, mkdir, move, goto and some more.

clean.bat will delete all temporary files and directories.

make.bat will create some of the sidplay64 versions in the root dir,
it will also generate a test.d64 image with some sids inside.

makeall.bat will create & pucrunch all versions in a "build" dir.

makerelease.bat will create release files crunched with exomizer in "build" dir.

netmake.bat will transfer a version of sidplay64 via LAN to my RR-net for
testing on real hardware.


Dir/file overview:

sidplay64.tas main source file.
sidplay64.cfg configurations for various devices. Dont touch!
c1541.mak used in combination with c1541.exe to create a test.d64 file.
/bin/ screen files.
/src/ all source files.
/docs/ various documentation.
/pics/ just temporary screenshots.
/sids/ contains various sids for sidplay64 to test.

Generated dirs/files:

timedate.clk time and clock
/build/ contains all release files


Credits:

Programmed by Glenn Rune Gallefoss (2005 up to present day.)

1541u2 code and the injector tool programmed by Tomaz kac.

