### emustarter.py 3.0

Emulators of retro computers have a lot of options. But when you want to play a game, you just want to tell the emulator: "I want to use this system, and I want to play this game". You don't want to go through a lot of configuration work, before starting playing.
`emustarter.py` let's you do this: It lets you select one of several systems, then the game you want to play, and ideally it handles the rest of the configuration and just starts the game. 

Supported systems and emulators are:

- Sinclair ZX Spectrum  (fuse)
- Atari 800 XL          (atari800)
- Amiga (500 and 1200)  (fs-uae)
- Mame                  (mame)

Of course, these emulators have to be already installed correctly on your system, otherwise, `emustarter.py` wouldn't work.
And to make it work (it does for me!), it also needs a bit of, well, configuration.
There is a configuration file called `emustarter.dat`, that should be in the same directory as `emustarter.py`. In the file `emustarter.dat` you have to specify the emulator directories, and then you have to write the list of games and game-files, you want to use with `emustarter.py`. There are examples of the required data format in the file `emustarter.dat` provided here. That file has to be edited according to the circumstances on your system. The entries of the game lines in `emustarter.dat` are separated by commata.
If `emustarter.dat` is edited correctly, it can be read by `emustarter.py`. Then, all the needed information can be found, and games can be started as described.

The following background-information is probably needed to be able to edit `emustarter.dat` correctly:

- ZX Spectrum emulation with `fuse`: A configuration file `~/.fuserc` is also read by the emulator.

- Atari 800 XL emulation with `atari800`: A configuration file `~/.atari800.cfg` is also read by the emulator. This file can be created in the graphical user interface of `atari800`. This file especially also contains the locations of the Atari ROM files (`atarixl.rom` and such). That's why these locations don't need to be specified again in `emustarter.dat`. For convenience, I also upload the file `atari800.cfg` from my system here.
- Most Atari 8-bit games run with the ROM of the [Atari 800 XL](https://upload.wikimedia.org/wikipedia/commons/b/bf/Atari-800XL.jpg) (`atarixl.rom`). Some older games need the ROM of the older [Atari 800](https://upload.wikimedia.org/wikipedia/commons/3/35/Atari_800.jpg) (`atariosb.rom`) though. To make `emustarter.py` aware of this, there has to be a third entry in the game lines in `emustarter.dat`: `0` is for the (ordinary) XL-ROM, `1` is for the Atari 800-ROM. `emustarter.py` will probably fail with an error, if this third entry is missing.

- Amiga emulation with FS-UAE: After the game name, the name of the FS-UAE configuration has to be given as the second entry of the game lines in `emustarter.dat`. These configurations have to be created for each game with the program `fs-uae-launcher`, that comes with FS-UAE. 
`fs-uae-launcher` writes these configuration files into a directory `../FS-UAE/Configurations`. They have the file-suffix `.fs-uae`. By default the directory should be created by `fs-uae-launcher` in `/home/user/Documents/FS-UAE/Configurations` (or `Dokumente` instead of `Documents` for German users). The location of this `Configurations`-directory has to be specified in the upper part of `emustarter.dat` at `AMIGA_CONFIGURATIONS_PATH=...`. (The location of the `FS-UAE`-directory can be changed by writing a different location into the file `/home/user/.config/fs-uae/base-dir`, just in case you wonder.)
When running an Amiga program with `fs-uae`, it is possible to save a snapshot of the Amiga's memory-state using the menu that appears when pressing `F12`. By default, `emustarter.py` starts `fs-uae` with loading the snapshot in the first slot directly (thanks to Frode Solheim for making this possible in `fs-uae`!). As a result, Amiga programs are started instantaneously, without any Amiga disk loading times (provided, that the memory state was saved, after the program was loaded once from the virtual disk). This is a very cool feature, that isn't possible on a real Amiga.
So, this is the default. If you don't want to load a snapshot, put a "0" (after a comma) in the game line as a third entry. Or for example a "2", if you want to load the second snapshot instead.

- Mame emulation: If you don't have a directory for `MAME_SAMPLES_PATH`, just create an empty directoriy "samples" in the directory of the game files, and specify it in the mentioned variable in `emustarter.dat`.

By default, `emustarter.py` presents you lists to select the system and the game. But if you already know the numbers, you can call `emustarter.py` with them as command-line options.
For example `emustarter.py 3 2` starts the second game on the Amiga.
Other command line options to `emustarter.py` are:

- `-vol 10`: Sets the sound volume to a value of 10. What `10` means in this context, depends on the emulator.
- `-nofs`: Don't use fullscreen mode.
- `-nostart`: Don't start. Just print the line to execute, then exit.

License: GNU GPL 3.
