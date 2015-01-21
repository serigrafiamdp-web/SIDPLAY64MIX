SIDPLAY64 V0.8 (c) GRG/SHAPE 2013
----------------------------------
Welcome to this latest version of Sidplay64 (SP64).

About the program:
------------------
This is a program that can playback .SID files found in the 
HVSC collection (http://hvsc.c64.org/) on a real Commodore 64/128.
Make sure you have the most recent HVSC version for your sid files.
It was designed for both PAL and NTSC computers, and will play all sid 
songs at correct system speed.

How to use:
-----------
You will find 5 different versions of SP64 in this package:

Sidplay64_08.prg                 -  Standard version - will work on all disk drives and devices.
sidplay64_08_1541u2.prg          -  Only for 1541u2
Sidplay64_08_1541u_netdrive.prg  -  Only for 1541u or netdrive.
sidplay64_08_iec_cmd_ide64.prg   -  Only for iec, cmd or ide64 devices.
sidplay64_08_sd2iec.prg          -  Only for Sd2iec.


When you first start SP64 you will see the drive selector screen.
You can use F1/F2 to select device number 6-30. Press return when done.
If you for any reason want to force the device number you can press CBM+Return.
Both netdrive and 1541u (in iec mode) returns: "@? :31,syntax error,00,00" when
SP64 tries to read the error channel. The same goes for 1541u2 in software iec mode.
The three mentioned devices doesn't return a proper device message when sending "UI".
Just press return to start the program when you see this message.

Then you have the option to configure a second sid chip.
(If you use the same address for sid 1 and sid 2 - both at $d400 in stereo - you should answer 
no to this question.)
You will need a second sid chip installed in your computer for this to work.
Valid bank addresses for the second sid chip:
$D400,$D420,$D440,$D460,$D480,$D4A0,$D4C0,$D4E0,$D500,$D520... up to $DFE0
Default is $d420. Press return to continue.

Next up is to select if you wish to ignore loading sids using $0000 as play address.
Both RSIDs and PSIDs can have this play address and they will stop
the random Shuffle play and the play next routine in your playlist.
Selecting Y here will avoid loading these "troublesome" sids.

Now the mains screen shows up and you have the option to select skin colors
with the keys 1-9. Or press any other key to make SP64 load the directory.

When a fresh directory is loaded you can only use some of these keys:

Cursor keys   :Select sid tune
Return        :Load a sid tune / open directory / open disk image file
Instdel       :Go back a directory level (Only for the versions that supports directory browsing)
Space         :Load/Reload directory
F1            :Restart song
F7            :Pause/Continue song
+ / -         :Select songs  (if any)
< / >         :Set shuffle time
R             :Randomly load sid tune (when shuffle time has been reached)
N             :Load next sid tune (when shuffle time has been reached)
M             :Manually select sid tune
ClrHome       :Top of directory
Shift+ClrHome :Bottom of directory
Restore       :Restart program (inits values and variables and loads directory.)
<-(left arrow):Fast forward (when song is playing)
CBM key       :Exit an RSID or PSID with $0000 as play address.

When the sid is playing/present in memory you can use all keys.

SP64 determines if the file is a sid by scanning the sid header of the file. That means the .sid
extension in the filename doesn't need to be present on the disk.
If the file is a wrong format it will exit with a red border (and reload dir incase the disk was swapped).
If the file is a RSID you will see the border changes to Grey when the music starts playing, and you 
will also notice that none of the keys works. Pressing CBM will exit back to SP64.
If the file is a PSID you will see a black border and you can use all keys to control the program.
There's One exception though, some PSIDs also has $0000 as play address and will behave like a RSID.



About RSIDs:
-------------
RSIDs runs with its own interrupt handler. The play call address is always set to $0000.
And you will see the letters "RSID" in the the top left corner.
The border turns grey when an RSID is playing. (Unless the rsid itself changes the border colors)

To exit an RSID:
Press the CBM key.
If that doesn't work try pressing spacebar, runstop, ctrl, shift, then the CBM key.
If that still doesn't work, try hitting Restore or Runstop/Restore to trigger a reset of the program.
If that doesn't work. You have to reset and reload the program.

If you sucessfully exited and RSID the normal way (CBM key) you can select subtunes with +/- and
you can start and stop the song with F1 and F7.

1541U2 using Software IEC:
-----------------------------------
Rename all *.sid files to *.prg
Put all files into root folder.
Filenames must not be larger than 16 letters (include the ".prg" ).


1541U (In IEC mode/Standalone mode):
------------------------------------
You can browse dirs and open .d64 images.
You can load sids from filesystem or from within .d64 images.


Netdrive + The Final Replay 0.8:
--------------------------------
You can browse dirs.
You need to prepare the files you want to use with netdrive:
1) To be able to load files from your PC filesystem you need to convert 
   the .sid extension to .prg ( ren *.sid *.prg )
2) Filenames can have a maximum of 16 letters ( not counting the ".prg" file extension)
3) directory names must not exceed 16 letters.
Once these things are done you can enter the following line to start netdrive:
netdrive -r c:/tmp/sids/
(Note the "/" slash must be correct or you will suffer countless hours of agony and pain...)


SD2IEC:
-------
You can browse directories, and you can open
the the following disk images : .d64, .d71, .d81 and .dnp


IEC(UIEC/IEC-ATA)/CMD FD/CMD HD/CMD RAMLINK/IDE64(+PClink):
-----------------------------------------------------------
You can browse directories.


DTV:
----
Random shuffle and play next mode doesn't work on DTV.
Reason: the DTV doesn't have the TOD clock registers.


Unsupported sid files:
----------------------
* Sid files with PSID in the filename.
* Sid files with BASIC in the filneame.
* Sid files using the old v1 sid headers will not work.


Bugs:
-----
Some sid files will cause bugs or even a crash. 
Especially RSIDs and PSIDs using $0000 as play address.
Be sure to help the HVSC crew by identifying those sids so that they
can be fixed to work with this program.


Thanks for help & support:
--------------------------
iAN CooG, Tom-Cat, Erhan, Ready, Fredric, Lemming
And to anyone I might have forgotten.

SIDPLAY 64 v.08 (12/12/2013):
-----------------------------
* Updated:   F7 key works as pause/continue.
* Updated:   Random routine is now more random in a increasing way.
* Added:     1541U2 software iec mode support.
* Added:     Configure and clear registers for 2nd sid chip. (for loading 2sid tunes)
* Added:     An option to skip RSIDs and PSIDs using $0000 as play address on startup.
* Added:     Select skin color using keys 1-9 on startup.


SIDPLAY 64 v.07 (25/08/2011):
-----------------------------
* Added:     Real PAL/NTSC detector.
* Added:     "D64" detector for long filenames (1541u + netdrive.)
* Added:     "DIR" sorter for directory displayer.
* Added:     Native dir browser and disk image browser (d64,d71 etc.) for netdrive, 1541u, iec, cmd and ide64.
* Added:     Long filenames support (Vice and Windows file system)
* BugFixed:  RunStop key doesn't stop loading. (Jiffydos will stop
* Updated:   Keyboard scanner - key delays works much better now.
* Added:     Keyboard scanner - "Instdel key" goes back a dir level.
* Added:     Device selector - device #6 up to #30
* Updated:   Alot of things in background code was optimized to save memory.
* Updated:   Timer IRQ updated, more available cpu time, it's now possible to play Jeff's 12 speed song.
* Updated:   TOD Clock + Shuffle modes  moved out of timer irq and into keyboard scanner subroutine.
* BugFixed:  RunStop+Restore will not crash when hardware IRQ interrupt is running (0314-0315).
* Updated:   "Memory Error" detection:
             Fixed a bug where SP64 code was relocated when loading a file with not enough
             relocation pages.

SIDPLAY64 v.06 beta (01/01/2010):
----------------------------------
* Corrected all text output, when loading sid files from PC dir, and when loading files over netdrive.
  No strange signs on screen now. ( ? )
* Fixed to "Work" with Netdrive, but there is a but: all sid files extensions must end with ".prg"
  For instance "shape.sid" will only work if renamed to "shape.prg" or "shape.sid.prg"
  Netdrive only supports files with the .prg extension.
  Filenames must be equal or less than 16 letters (do not count file extension)
* Fixed the bug with Retro Replay.
  According to Countzer0 it is indeed a bug that shouldnt be there.
* Files with not enough relocation pages for siplay64 and with a built in play mode 
  (see sid files with $0000 as play call) will now be loaded and started.
  Examples here are Pollytracker songs which use all memory.
  Other files where relocation pages doesn't leave enough memory will still give you
  the "out of memory error" message.
* Speeded up the keyboard scanner.
  You can select things faster now.
* Added a display number for number of files in dir.

SIDPLAY64 v.05 beta (20/11/2009):
----------------------------------
Added a long overdue IDE64 fix - Thanks to iAN COOG and Soci.

SIDPLAY64 v.04 beta (23/12/2005):
----------------------------------
First version that was released.