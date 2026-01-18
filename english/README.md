#### emustarter.py 3.4

Emulators of retro computers have a lot of options. But when you want to play a game, you just want to say: "Computer, I'd like to use this system, and I'd like to play this game!". You don't want to go through a lot of configuration work, before starting playing.
`emustarter.py` let's you select one of several systems and the game you want to play on the Linux console, and ideally handles the rest of the configuration and just starts the game. 

Supported systems and emulators are (these are typical emulators on Linux):

- Sinclair ZX Spectrum  (fuse)
- Atari 800 XL          (atari800)
- Amiga (500 and 1200)  (fs-uae)
- Mame                  (mame)

Of course, these emulators have to be already installed correctly on your system, otherwise, `emustarter.py` won't work.
And to make it work (it does for me!), it also needs a bit of, well, configuration.
There is a configuration file called `dat_emustarter.conf`, that should be in the same directory as `emustarter.py`. In the file `dat_emustarter.conf` you have to specify the emulator directories, and then you have to write the list of games and game-files, you want to use with `emustarter.py`. Please don't edit the headlines in square brackets. There are examples of the required data format in the file `dat_emustarter.conf` provided here. That file has to be edited according to the circumstances on your system. The entries of the game lines in `dat_emustarter.conf` are separated by commata.
If `dat_emustarter.conf` is edited correctly, it can be read by `emustarter.py`. Then, all the needed information can be found, and games can be started as described.

The following background-information is probably needed to be able to edit `dat_emustarter.conf` correctly:

- ZX Spectrum emulation with `fuse`: A configuration file `~/.fuserc` is also read by the emulator.

- Atari 800 XL emulation with `atari800`: A configuration file `~/.atari800.cfg` is also read by the emulator. This file can be created in the graphical user interface of `atari800`. This file especially also contains the locations of the Atari ROM files (`atarixl.rom` and such). That's why these locations don't need to be specified again in `dat_emustarter.conf`. For convenience, I also upload the file `atari800.cfg` from my system here.
- Most Atari 8-bit games run with the ROM of the [Atari 800 XL](https://upload.wikimedia.org/wikipedia/commons/b/bf/Atari-800XL.jpg) (`atarixl.rom`). Some older games need the ROM of the older [Atari 800](https://upload.wikimedia.org/wikipedia/commons/3/35/Atari_800.jpg) (`atariosb.rom`) though. To make `emustarter.py` aware of this, there has to be a third entry in the game lines in `dat_emustarter.conf`: `0` is for the (ordinary) XL-ROM, `1` is for the Atari 800-ROM. `emustarter.py` will probably fail with an error, if this third entry is missing.

- Amiga emulation with FS-UAE: After the game name, the name of the FS-UAE configuration has to be given as the second entry of the game lines in `dat_emustarter.conf`. These configurations have to be created for each game with the program `fs-uae-launcher`, that comes with FS-UAE. 
`fs-uae-launcher` writes these configuration files into a directory `../FS-UAE/Configurations`. They have the file-suffix `.fs-uae`. By default the directory should be created by `fs-uae-launcher` in `/home/user/Documents/FS-UAE/Configurations` (or `Dokumente` instead of `Documents` for German users). The location of this `Configurations`-directory has to be specified in the upper part of `dat_emustarter.conf` at `AMIGA_CONFIGURATIONS_PATH=...`. (The location of the `FS-UAE`-directory can be changed by writing a different location into the file `/home/user/.config/fs-uae/base-dir`, just in case you wonder.)
- When running an Amiga program with `fs-uae`, it is possible to save a snapshot of the Amiga's memory-state using the menu that appears when pressing `F12`. By default, `emustarter.py` starts `fs-uae` with loading the snapshot in the first slot directly (thanks to Frode Solheim for making this possible in `fs-uae`!). As a result, Amiga programs are started instantaneously, without any Amiga disk loading times (provided, that the memory state was saved, after the program was loaded once from the virtual disk). This is a very cool feature, that isn't possible on a real Amiga.
So, this is the default. If you don't want to load such a snapshot, put a "0" (after a comma) in the game line as a third entry. Or for example a "2", if you want to load the snapshot in the second slot instead.

- Mame emulation: If there isn't a directory for `MAME_SAMPLES_PATH`, you can just create an empty directory "samples" in the directory of the game files, and specify it in the mentioned variable in `dat_emustarter.conf`.

By default, `emustarter.py` presents you lists to select the system and the game. But if you already know the numbers, you can call `emustarter.py` with them as command-line options.
For example `emustarter.py 3 2` starts the second game in your Amiga list, `emustarter.py 2 5` starts the fifth game in the Atari list and so on. This makes using `emustarter.py` even faster.
Other command line options to `emustarter.py` are:

- `-vol 10`: Sets the sound volume to a value of `10`. What `10` means in this context, depends on the emulator.
- `-nofs`: Don't use fullscreen mode.
- `-nostart`: Don't start the emulator. Just print the line to execute, then exit.

About the configuration of "atari800":
- On some Linux-systems (probably on those without proprietary drivers for the graphics card), the option `VIDEO_ACCEL=0` should be set in the configuration file. Otherwise the emulation may run extremely slowly, that is, it may not work properly.
- About the configuration of the joystick:
  - For a connected joystick to work, it is not necessary to set the option `Enable keyboard joystick` in the menu `Controller Configuration` of the F1-menu. The joystick should work without this.
  - If pressing the fire-button doesn't have an effect, a certain option has to be set in the F1-menu: In `Controller Configuration / Configure real joysticks / Joystick 1 / Configure Buttons`, for `A` the option `Action / Joy Trigger` has to be set. After that, the configuration should be saved with `Emulator Configuration / Save configuration file` from the F1-menu. After that, the fire-button should work.

The "emustarter"-project's license is the GNU GPL 3.
