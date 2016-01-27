SIDPLAY64 V1.10
---------------------------------------------------------------
Welcome to the last version of Sidplay64 (SP64).
Finally we have also found space for BASIC sid files support.
Read more about that in its own section below.
This program alsom comes with our new length injector tool.
With modified sids you can listen to your favourite sids
from start till end before it loads the next or random sid file.

Don't panic! - This program will handle both modified and normal sids.


About the program:
---------------------------------------------------------------
This is a program that can playback .SID files found in the 
HVSC collection (http://hvsc.c64.org/) on a real Commodore 64/128.
Make sure you have the most recent HVSC version for your sid files.
It was designed for both PAL and NTSC computers, and will play all sid 
songs at correct system speed.


Versions of the program:
---------------------------------------------------------------
You will find different versions of SP64 in this package, most of them
will work on all devices.  But I suggest you use the correct version for 
for your device, since they might contain special commands:

sidplay64-reu-1541u2cmd.prg      - 1541 Ultimate II version with REU.
sidplay64-reu-sd2iec.prg         - SD2IEC version with REU. 
sidplay64-reu-1541u-netdrive.prg - 1541 Ultimate & Netdrive with REU.
sidplay64-reu-iec-cmd-ide64.prg  - CMD drives, IDE64 devices & other IEC devices, with REU.
sidplay64-reu-normal.prg         - REU version for 1541, 1571, 1581 and clones of these.

sidplay64-1541u2cmd              - 1541 Ultimate II version.
sidplay64-normal.prg             - Standard version for 1541, 1571, 1581 and clones.
sidplay64-1541u-netdrive.prg     - 1541 Ultimate & Netdrive.
sidplay64-iec-cmd-ide64.prg      - CMD drives, IDE64 devices & other IEC devices.
sidplay64-sd2iec.prg             - SD2IEC.

(The 1541U2 software iec mode has been disabled for this build.)


How to use:
---------------------------------------------------------------
When you first start SP64 you will see the drive selector screen.
You can use F1/F2 to select device number 6-30. Press return when done.
If you for any reason want to force the device number you can press CBM+Return.
Both Netdrive and 1541u (in iec mode) returns: "@? :31,syntax error,00,00" when
SP64 tries to read the error channel. The two mentioned devices doesn't return a 
proper device message when sending "UI".
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

Then you have a new option to disable song lengths for modded/injected sids.
The sids we are talking about here are modified sids done with our little
program called sp64injector.exe. 
You can read more about that program further below. 
If you select Y, any information about song lengths in the sids will be ignored.

Last question : Controlling the program with Joystick Port #1 or Keyboard ?
Selecting Joystick allows you to control the program from your favourite
sofa or armchair. Just sit back and relax.
See further below for Joystick controls.

Now the mains screen shows up and you have the option to select skin colours
with the keys 0-9. Or press any other key to make SP64 load the directory.

If you don't like to answer these questions next time, simply press
return 6 times to get the default values.


KEYBOARD COMMANDS:
---------------------------------------------------------------
When a fresh directory is loaded you can only use some of these keys.

CRSR UP/DOWN   :Select sid tune
RETURN         :Load a sid tune / open directory / open disk image file
INSTDEL        :Go back a directory level (Only for the versions that supports directory browsing)
SPACE          :Load/Reload directory
F1             :Restart song
F7             :Pause/Continue song
+ / -          :Select songs  (if any)
, / .          :Set timer for when NEXT or RANDOM tune is going to be loaded.
M              :Mode select: Manual, Next or Random
CRSR LEFT      :jump 15 lines upwards.
CRSR RIGHT     :jump 15 lines downwards.  (In the non-REU version this jumps all the way down.)
RESTORE        :Force exit from the sid playing - reloads directory.
RUNSTOP+RESTORE:Force exit from the sid playing - returns to fileselector with all keys available.
<-(LEFT ARROW) :Fast forward (when song is playing)
CBM KEY        :Exit an RSID or PSID with $0000 as play address.
S              :Screen on/off. (Reduce video chip noise).
X              :Load Next or Random sid
CLRHOME        :Keep pressed to load more filenames when reading directory holding more than 164 files.
                This only works for the NON-REU version of sd2iec, *iec, cmd drives, IDE64, Netdrive and 1541Ultimate.

When the sid is playing/present in memory you can use all keys.


JOYSTICK CONTROLS:
---------------------------------------------------------------
When in joystick mode, these keys and stick commands applies:

FIRE BUTTON   :Load SID
SPACEBAR:     :Load Directory
COMMODORE KEY :Fast Forwards

(While loading in a directory you can hold joystick to the RIGHT to load more filenames 
from a directory with more than 164 files.) 


JOYSTICK CONTROL WITHOUT FIREBUTTON PRESSED:


                 CURSOR UP
                    |
                    |
PREVIOUS SONG   ---- ---- NEXT SONG
                    |
                    |
                CURSOR DOWN


JOYSTICK CONTROL WITH FIREBUTTON PRESSED:

Important: First move and hold the stick in the desired direction, 
           then press fire, then release fire button.


                JUMP UPWARDS
                    |
PREVIOUS DIRECTORY  |   RESTART SONG
                  \ | /
                   \|/
TIMER DECREASE  ----*---- TIMER INCREASE (NEXT/RANDOM)
                   /|\
                  / | \
         SET MODE   |   PAUSE/CONTINUE SONG
                    |
                JUMP DOWNWARDS


LOADING DIRECTORY:
---------------------------------------------------------------
When you press SPACEBAR the current directory will be loaded from your
SD card, Hard Drive or Diskette. 
Pressing RETURN on ".." allows you to go back a directory level.
Pressing the INSTDEL key will do the same thing.
When you switch a directory level, the new directory will be loaded automatically.
Directory names will have a "DIR" extension on the right side of the directory name.

In the non-REU version you can move the cursor up and down while loading directory,
for instance holdign the CRSR right key allows you to see the new filenames enter c64 memory.

In the non-REU version for iec,cmd and ide64 devices you have the option to hold 
the CLR HOME key to load more filenames.  The limit is 164 filenames in this program, 
so loading the complete DRAX dir is now possible. 
But with this new key feature it is possible.
(In joystick mode you can hold joystick to the right to load more filesnames.)

In the REU versions you have the possibilty to have up to 65535 filenames in memory.
In the REU versions you will also see the filesize in kb for each sid on the right side of
the screen (Unfortunately this is not possible for 1541uII yet).


LOADING A SID FILE:
---------------------------------------------------------------
SP64 determines if the file is a sid by scanning the sid header of the file. That means the .sid
extension in the filename doesn't need to be present on the disk.
If the file is a wrong format it will exit back to limited cursor control with a red border.
If the file is a RSID you will see the border changes to Grey when the music starts playing, and you 
will also notice that none of the keys works. Pressing/Holding the CBM key should exit back to SP64 in most cases.
If the file is a PSID you will see your skin default border color and you can use all keys to control the program.
There's One exception though, some PSIDs also has $0000 as play address and will behave like a RSID.

Panic Load:
Some sids will use more memory than SP64 can handle. And in those cases, if the sid header has 
information to do so, the sid will be loaded and started with no possible return.
In many cases loading such files need a cartridge or device that can load under IO memory d000-e000.
Action Replay/Retro Replay can do this. The 1541UII version also allows to load under IO memory.


About RSIDs:
---------------------------------------------------------------
RSIDs run using its own interrupt handler. The play call address is always set to $0000.
And you will see the letters "RSID" in the the top left corner.
The border turns grey when an RSID is playing. (Unless the rsid itself changes the border colours)

To exit an RSID:
Press the CBM key.
If that doesn't work try pressing Sacebar, Run/Stop, Ctrl, Shift, then the CBM key.
If that still doesn't work, try hitting RunStop + Restore to trigger a reset of the program.
If that doesn't work. You have to reset and reload the program.

If you successfully exited and RSID the normal way (CBM key) you can select sub tunes with +/- and
you can start and stop the song with F1 and F7.


Loading a BASIC sid file:
---------------------------------------------------------------
Loading and running a BASIC sid file will turn your border to grey (unless the sid itself changes colours).
It is possible to return back to SP64 by pressing CBM key, but only after the song has stopped and finished.
If the song loops forever you have to hold the RunStop button and tap RESTORE, the music should stop and 
the border color should return to default, and you can use F1, + and - to restart or select subtunes for this sid.

Many BASIC sids will write text and colors to screen, so don't worry if you see weird colors on the screen.


MODE SELECT:
---------------------------------------------------------------
Next to the Timer on screen you will see the letters M N R appear when you press
the M key. This sets the Mode for the timer.
M = Manual selection - The timer is not used.
N = Play Next - The next song in the list is played when the Clock reach the Timer value.
R = Random Play - A random song is played when the Clock reach the Timer value.


RUNSTOP+RESTORE and RESTORE:
---------------------------------------------------------------
Should only be used on Rsid's or Psid's that has it's own interrupt handler (play call is $0000)
or a sid that is made with a BASIC start (init call is $0000). 
These sids normally turn the border to dark grey.

Normally you can exit these sids by pressing the CBM key, but if that doesnt work you can try
holding RUN STOP and tapping RESTORE.

RESTORE alone does the same thing as pressing SPACEBAR (loads directory and turn off most keys).


SP64INJECTOR.EXE:
---------------------------------------------------------------
With this tool you can inject default song lengths into your sids.
Place the sids you want to modify into a dir together with this tool.
You also need a copy of the file \HVSC\C64Music\DOCUMENTS\Songlengths.txt
to be present in the dir.
Once all files are present, go to the dos shell and from the command line call:

sp64injector.exe

Use the -s flag if you want to include sub directories:

sp64injector.exe -s

This way you can also inject song lengths into the whole hvsc collection.
BUT I suggest you keep a untouched backup of your hvsc collection, we don't 
know what your pc/mac based sidplayers will think about modified sids.

Use the -v flag (verbose mode) to see more details.

sp64injector.exe -v -s

The injector will give error messages on sid files that is impossible to modify.
Those sids will be 2sids or 3sids files.

SP64 has a new option to make use of the data you have injected into these sids.
And with it you can make a playlist of sids with exact playing time for each sid.

Only use these modified sids with SP64.
Modified sids will play fine on all older versions of SP64, but the 
injected song lengths will only be used by v1.00 and upwards.


REU - The Ram Expansion Unit.
---------------------------------------------------------------
This device is now supported in all versions.
It allows you to have several thousand sid files in your directory.

The 1541U2 has support for up to 16 mb reu. 

If you are looking for real hardware, then you will find that
Commodore manufactured 3 reu versions, with memory sizes of 128kb, 256kb and 512kb.
Creative Micro Design (CMD) produced 512kb and 2mb versions, named 1750 XXL.
Chip Level Designs' (CLD) Superclone 1750 has 512kb of memory.

A 512kb re will give you access to 4096 filenames per directory. 
The 256kb one will have space for 2048 filenames per directory.

A little note about IEC builds:
The REU versions does not support dir sorting to the top. 
If you want your directories to appear at the top you have to 
create directories first, and then you add the files last.
(This should happen automatically if you copy and paste the HVSC dir?)


1541 Ultimate II Command Interface:
---------------------------------------------------------------
This version only works with 1541u2 firmware update 2.6d or higher.
Recommended version is 2.6k
It comes with REU support. You need to enable the REU support.
It uses the Command Interface. You need to enable that as well.

Currently there are two bugs in the latest 1541u2 firmware (v2.6k):

1. When USB drive is connected you first need to enter the USB directory with 
   the U2 Browser or it will show up as a File in SP64 instead of directory.
2. You can only go up to the Root of the U2 drive once and choose the SD Card or 
   USB directory, after that you cannot go completely up to the Root again.

3. This is perhaps not a bug, but worth a note:
   When you have a huge 1541u2 directory each file will take longer to load.



1541U (In IEC mode/Standalone mode):
---------------------------------------------------------------
You can browse dirs and open .d64 images.
You can load sids from filesystem or from within .d64 images.


Netdrive + The Final Replay 0.8:
---------------------------------------------------------------
Select 6 or 7 as your device number in the setup screen.
You can browse dirs.
You need to prepare the files you want to use with Netdrive:
1) To be able to load files from your PC filesystem you need to convert 
   the .sid extension to .prg ( ren *.sid *.prg )
2) Filenames can have a maximum of 16 letters ( not counting the ".prg" file extension)
3) directory names must not exceed 16 letters.
Once these things are done you can enter the following line to start Netdrive:
netdrive -r c:/tmp/sids/
(Note the "/" slash must be correct or you will suffer countless hours of agony and pain...)


SD2IEC:
-------
You can browse directories, and you can open
the the following disk images : .d64, .d71, .d81 and .dnp

IEC(UIEC/IEC-ATA/IEC2ATA)/CMD FD/CMD HD/CMD RAMLINK/IDE64(+PClink):
-------------------------------------------------------------------
You can browse directories.


UNO2IEC (The Arduino Project):
------------------------------
Doesn't work with SP64 at the moment.
Possibly a bug in the IEC implementation on the device ?


DTV:
----
Random shuffle and play next mode doesn't work on DTV.
Reason: the DTV doesn't have a TOD clock registers.


WinVice:
--------
Use the REU SD2IEC version with WinVice to browse the Windows file system and the
complete HVSC directory.


Unsupported sid files:
----------------------
* Sid files with PSID in the filename.
* Sid files using the old v1 sid headers will not work.


Bugs:
-----
Many sid files are badly ripped and will crash or cause strange bugs on SP64.
Reasons are many:

* The sid header has no free relocation pages set. (SP64 will print "no memory")
* The free relocation pages offered by the sid header is wrong and crashes SP64.
* The sid will overwrite other music data when selecting sub tunes. (sidplay on pc load the file back from a buffer.)
* The sid load to area at d000-e000.  That wont work on a stock c64 without a fastload cartridge. Or a custom software loader.
* The sid overwrite NMI and IRQ vectors (fffa-ffff)
* The sid use wrong zeropage $01 and they might set CLI or SEI in the play call.
* The sid contains routines that change graphic mode, memory banks, colour ram etc.

Especially RSIDs and PSIDs using $0000 as play address seems to be problematic.
Be sure to help the HVSC crew by identifying those sids so that they
can be fixed to work with this program.


Thanks for help & support:
--------------------------
The 1541U2 cmd routines was developed by my friend Tom-Cat/Nostalgia,
without his help this version would never have seen daylight. 
I shared the sources with him on gitlab and within 2 days we had a working beta.
So kudos to him for his work.
(I should buy one of those myself someday. (Edit: And I did))

The sp64injector.exe was programmed by Tom-Cat.

Also thanks to these people for help, ideas, bug testing:

Tom-Cat, Erhan, Ready, Lemming, Hurminator, iAN CooG, Fredric, Wilfred,
and everyone in Nostalgia and Shape.

And ofcourse to everybody we know.

Also a big thanks to Whiteflame for sharing his 'random' routines on codebase.


Credits:
--------
Programming by: Glenn R. Gallefoss
Additional programming by: Tom-Cat


SIDPLAY 64 v1.10 (xx/xx/2016):
-------------------------------
* Added:     IEC/CMD/IDE64: ClrHome key loads more filenames while reading directory.
* Added:     IEC/CMD/IDE64: Joystick RIGHT loads more filenames while reading directory.
* Behaviour: BASIC sid's that stops on its own can be exited by pressing CBM.
* Added:     Songs with BASIC start support.
* Added:     REU: Remembers previous dir positions when you go back.
* Added:     REU: File size are displayed in kilobytes. (Not for 1541u2)
* Behaviour: Restore : resets variables and reloads dir.
* Behaviour: RunStop+Restore : exit BASIC sid's or sid's using $0000 as play call.
* Fixed:     1541U2: shortened dir read routine.
* Fixed:     One of the color skins used dark grey for border.


SIDPLAY 64 v1.00 (13/12/2015):
-------------------------------
* Fixed:     A zeropage buffer bug. Bug is from the v0.9 update.
             Chris Huelsbeck's Hard'n'Heavy played wrong because of this.
* Added:     Panic load for 1541u2 - some of the larger sids can now be loaded
             and executed. No return to SP64 possible.
* Added:     "X" key to skip to next or random sid.
* Fixed:     Optimized 1541u2 loading/dir routines. Gained atleast $10 bytes!
* Fixed:     Optimized some routines using illegal opcodes.
* Added:     Windows program for injecting sids with correct song lengths.
* Added:     Code to handle song lengths for injected sids.
* Added:     Option to disable song length info from injected sids.
* Fixed:     Turn screen off/on value is permanent when loading new sids.
* Fixed:     Replaced the red border skin. We use red border as a error message.
* Fixed:     1541u2: display: Error with song numbers above 10.
* Added:     1541u2: loading dir: display maxfiles while loading dir.
* Added:     1541u2: turn off screen when loading file.
* Behaviour: When you get a red border the dir will NOT be reloaded.
             

SIDPLAY 64 v.09 (xx/02/2015):
-----------------------------
* Added:     1541U2 command interface routines.
* Added:     REU support, possible with 65534 filenames in a directory.
* Added:     A few routines optimized for size.
* Added:     Attract mode.  A scrolling message.
* Updated:   ClrHome (+shift) keys has changed to crsr left and crsr right.
* Added:     Joystick mode for port #1.
* Updated:   Select skin colours with 0-9. New skins.
* Updated:   M now selects Manual, Next, Random.
* Removed:   R and N keys.
* Added:     S Turns screen on/off, this to reduce videochip noise.
* Disabled:  1541U2 software iec mode support.

SIDPLAY 64 v.08 (12/12/2013):
-----------------------------
* Updated:   F7 key works as pause/continue.
* Updated:   Random routine is now more random in a increasing way.
* Added:     1541U2 software iec mode support.
* Added:     Configure and clear registers for 2nd sid chip. (for loading 2sid tunes)
* Added:     An option to skip RSIDs and PSIDs using $0000 as play address on startup.
* Added:     Select skin colour using keys 1-9 on startup.


SIDPLAY 64 v.07 (25/08/2011):
-----------------------------
* Added:     Real PAL/NTSC detector.
* Added:     "D64" detector for long filenames (1541u + Netdrive.)
* Added:     "DIR" sorter for directory displayer.
* Added:     Native dir browser and disk image browser (d64,d71 etc.) for Netdrive, 1541u, iec, cmd and ide64.
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

SIDPLAY 64 v.06 beta (01/01/2010):
----------------------------------
* Corrected all text output, when loading sid files from PC dir, and when loading files over Netdrive.
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

SIDPLAY 64 v.05 beta (20/11/2009):
----------------------------------
Added a long overdue IDE64 fix - Thanks to iAN COOG and Soci.

SIDPLAY 64 v.04 beta (23/12/2005):
----------------------------------
First version that was released.