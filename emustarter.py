#!/usr/bin/python3
# coding: utf-8

"""
    emustarter.py 3.2 - Starts certain classic games with several emulators
                        on Linux. Supported systems and emulators are:

    - Sinclair ZX Spectrum  (fuse)
    - Atari 800 XL          (atari800)
    - Amiga (500 and 1200)  (fs-uae)
    - Mame                  (mame)

    Copyright (C) 2018-2024 Hauke Lubenow

    This program is free software: you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import os, sys
import time

# Look for "dat_emustarter.conf" in the same directory as "emustarter.py".
# Change, if you like:
DATAFILE = os.path.join(os.path.dirname(__file__), "dat_emustarter.conf")

class Main:

    def __init__(self):

        self.data = EmuData()
        self.paths = self.data.data["directories"]
        self.systems = (System(self.paths, self.data, "spectrum", "Sinclair ZX Spectrum", "", "Manic Miner"),
                        System(self.paths, self.data, "atari", "Atari 800 XL", "", "Joust"),
                        System(self.paths, self.data, "amiga", "Amiga 500", "Amiga", "Giana Sisters"),
                        System(self.paths, self.data, "mame", "Mame", "", "Pacman"))
        self.systemnumber = -1
        self.gamenumber   = -1

        # First option on command-line (system choice):

        if len(sys.argv) > 1:
            if sys.argv[1].isdigit() and int(sys.argv[1]) >= 1 and int(sys.argv[1]) <= len(self.systems):
                self.systemnumber = int(sys.argv[1]) - 1

        # Second option on command-line (game choice):
        if len(sys.argv) > 2 and self.systemnumber >= 0:
            if self.systemnumber < len(self.systems):
                self.system = self.systems[self.systemnumber]
                if sys.argv[2].isdigit() and int(sys.argv[2]) >= 1 and int(sys.argv[2]) <= len(self.system.gamedata):
                    self.gamenumber = int(sys.argv[2]) - 1

        if self.systemnumber == -1:
            self.createSystemNames()
            self.systemnumber = self.getChoice("Which system?", self.systemnames, 0, {})

        # self.systemnumber is now >= 0.
        if self.gamenumber == -1:
            if self.systemnumber < len(self.systems):
                self.system = self.systems[self.systemnumber]
                self.system.createGameList()
                defaultgamenumber = self.system.getDefaultGameNumber()
                self.gamenumber = self.getChoice(self.system.fullplatformname + " - Programs", self.system.gamelist, defaultgamenumber, {})

        # self.system is now set to one of self.systems and
        # self.gamenumber is known.

        if len(sys.argv) > 3:
            self.system.createSettings(sys.argv[3:])

        self.system.createGameRunString(self.gamenumber)
        self.system.printSettings(self.gamenumber)

        self.system.start(self.gamenumber)

    def createSystemNames(self):
        self.systemnames = []
        for i in self.systems:
            self.systemnames.append(i.choicelistname)

    def getChoice(self, headline, choices, defaultchoice, interruptions):
        """ Presents the items of a list, to let you choose one of them,
            with a number from 1 to len(choices).
            Returns the number of the item in the list, that is an integer
            in the range of 0 to "len(choices) - 1".
        """
        if len(choices) < 1 or len(choices) > 9999:
            raise ValueError("List-length out of range (1-9999).")
        if defaultchoice < -1 or defaultchoice > len(choices) - 1:
            raise ValueError("Default-choice out of range.")
        os.system("clear")
        x = 0
        print()
        print(headline + ":")
        print()
        n = 10
        sprintfnr = 1
        while len(choices) > n:
            sprintfnr += 1
            n *= 10
        sprintfstr = "%0" + str(sprintfnr) + "d";
        for i in range(len(choices)):
            if i in interruptions.keys():
                if i != 0:
                    print()
                print(interruptions[i] + ":")
            numberstring = sprintfstr % (i + 1)
            print(numberstring + ". " +  choices[i])
        print()
        inputstr = ""
        while x == 0:
            prompt = "Enter your choice"
            if defaultchoice > -1:
                prompt += " (Default: \"" + str(defaultchoice + 1) + ". " + choices[defaultchoice] + "\")"
            prompt += ": "
            inputstr = input(prompt)
            inputstr = str(inputstr)
            if inputstr == "":
                if defaultchoice > -1:
                    inputstr = str(defaultchoice + 1)
                    x = 1
                else:
                    continue
            if inputstr == "q":
                print("Bye.\n")
                sys.exit(0)
            if inputstr.isdigit() and int(inputstr) >= 1 and int(inputstr) <= len(choices):
                x = 1;
        return int(inputstr) - 1


class System:

    def __init__(self, paths, data, platform, fullplatformname, choicelistname, defaultgame):
        self.paths = paths
        self.data = data
        self.platform = platform
        self.fullplatformname = fullplatformname
        self.choicelistname = choicelistname
        if self.choicelistname == "":
             self.choicelistname = self.fullplatformname
        self.defaultgame = defaultgame
        self.gamedata = self.data.data[self.platform]
        self.settings = self.data.getSettings(self.platform)

        self.options = {"fullscreen"   : True,
                        "start"        : True,
                        "soundvolume"  : None}

    def createGameList(self):
        self.gamelist = []
        for i in self.gamedata:
            self.gamelist.append(i[0])

    def getDefaultGameNumber(self):
        for i in range(len(self.gamedata)):
            if self.gamedata[i][0].startswith(self.defaultgame):
                return i
        return -1

    def createSettings(self, clopts):
        o = ((("nofs", "win"), ("fullscreen", False)),
             (("nostart", "dontstart"), ("start", False)))
        for i in range(len(clopts)):
            for u in o:
                for u2 in u[0]:
                    if u2 in clopts[i]:
                        self.options[u[1][0]] = u[1][1]
            if "vol" in clopts[i]:
                if i < len(clopts) - 1 and self.isdigitOrNegative(clopts[i + 1]):
                    self.options["soundvolume"] = int(clopts[i + 1])

        if self.platform == "spectrum":
            if self.options["fullscreen"] is False:
                self.settings["fullscreen"] = "--no-full-screen"
            if self.options["soundvolume"] != None:
                self.settings["soundvolume"] = "--volume-beeper " + str(self.options["soundvolume"])

        if self.platform == "atari":
            if self.options["fullscreen"] is False:
                self.settings["fullscreen"] = "-windowed"
            if self.options["soundvolume"] != None:
                self.settings["soundvolume"] = "-volume " + str(self.options["soundvolume"])

        if self.platform == "amiga":
            if self.options["fullscreen"] is False:
                self.settings["fullscreen"] = "--fullscreen=0"

        if self.platform == "mame":
            if self.options["fullscreen"] is False:
                self.settings["fullscreen"] = "-window"

            if self.options["soundvolume"] is not None:
                # Correct Mame-volume:
                if self.options["soundvolume"] >= 0:
                    if self.options["soundvolume"] > 40:
                        self.options["soundvolume"] = 40
                    self.options["soundvolume"] = self.options["soundvolume"] - 40 # -40 should be silent.
                self.settings["soundvolume"] = "-volume " + str(self.options["soundvolume"])

    def isdigitOrNegative(self, a):
        """ Checks, if a string contains either an integer,
            or a minus-character followed by an integer. """
        if a.isdigit():
            return True
        if len(a) >= 2 and a[0] == "-" and a[1:].isdigit():
            return True
        return False

    def createGameRunString(self, gamenumber):

        self.gamename = self.gamedata[gamenumber][0]

        if self.platform == "spectrum":
            self.startstring = "fuse -g paltv3x --no-aspect-hint --kempston --joystick-1-output 2 "
            gamestring = "--snapshot " + os.path.join(self.paths["SPECTRUM_PROGRAMS_PATH"], self.gamedata[gamenumber][1])

        if self.platform == "atari":
            self.startstring = "atari800 "
            gamestring = os.path.join(self.paths["ATARI_PROGRAMS_PATH"], self.gamedata[gamenumber][1])
            if self.gamedata[gamenumber][2] == 1:
                self.settings["machinetype"] = "-atari"
            if self.gamename == "Atari BASIC":
                self.settings["holdoption"] = "-basic"

        if self.platform == "amiga":
            self.startstring = "fs-uae "
            gamestring = '"' + os.path.join(self.paths["AMIGA_CONFIGURATIONS_PATH"], self.gamedata[gamenumber][1]) + '"'

            # Add " --load_state=1" by default (without third element).
            # Add nothing, if third element exists, and is "0",
            # "--load_state=" + third element, if it exists, and is larger than 0:

            if len(self.gamedata[gamenumber]) < 3:
                gamestring += " --load_state=1"
            elif int(self.gamedata[gamenumber][2]) > 0:
                gamestring += " --load_state=" + self.gamedata[gamenumber][2]

        if self.platform == "mame":
            self.startstring = "mame -rompath " + self.paths["MAME_PROGRAMS_PATH"] + " -samplepath " + self.paths["MAME_SAMPLES_PATH"] + " "
            gamestring = '"' + os.path.join(self.paths["MAME_PROGRAMS_PATH"], self.gamedata[gamenumber][1]) + '"'

        for i in self.settings.keys():
             if self.settings[i]:
                 self.startstring += self.settings[i]
                 self.startstring += " "
        self.startstring += gamestring
        # self.startstring += " &>/dev/null"

    def printSettings(self, gamenumber):
        print()
        print("Settings:")
        print()
        prlist = [["Platform: ", self.fullplatformname],
                  ["Game: ", str(gamenumber + 1) + ". " + self.gamename]]
        if self.platform != "mame":
            a = ["Fullscreen: "]
            if self.options["fullscreen"]:
                a.append("Yes.")
            else:
                a.append("No.")
            prlist.append(a)
        if self.platform == "atari":
            prlist.append(("Hold Option-Key:",  self.settings["holdoption"]))
        if self.platform == "amiga":
            prlist.append(("Sound volume:", "Handled by config-file."))
        else:
            a = ["Sound volume: "]
            if self.options["soundvolume"] is None:
                b = self.settings["soundvolume"]
                if self.platform in ("spectrum", "mame"):
                    b = b.split(" ")[1]
                a.append(b)
            else:
                a.append(str(self.options["soundvolume"]))
            prlist.append(a)
        prlist.append(["System-call:", self.startstring])
        for i in prlist:
            print(self.getFormatted(i))
        print()

    def getFormatted(self, twostrings):
        mylength = 27
        (a, b) = twostrings
        a += (mylength - len(a)) * " "
        b2 = ""
        if a.startswith("System-call"):
            b2 = b
        else:
            for i in range(len(b)):
                if i == 0:
                    b2 += b[i].upper()
                else:
                    b2 += b[i]
        return a + b2

    def start(self, gamenumber):

        if self.platform == "amiga":
            amigaconfigurationfile = os.path.join(self.paths["AMIGA_CONFIGURATIONS_PATH"], self.gamedata[gamenumber][1])
            if not os.path.exists(amigaconfigurationfile):
                print("Error: Amiga configuration file\n\n\"" + amigaconfigurationfile + "\"\n\nnot found. Can't start game. Aborting.\n")
                return

        if self.options["start"]:
            time.sleep(2)
            os.system(self.startstring)

class EmuData:

    def __init__(self):
        self.readData()

    def stripArray(self, a):
        for i in range(len(a)):
            a[i] = a[i].strip()
            a[i] = a[i].strip('"')
        return a

    def readData(self):
        if not os.path.exists(DATAFILE):
            print("\nError: File \"" + DATAFILE + "\" not found.")
            print("Make sure, it is present in the same directory as \"emustarter.py\".\n")
            sys.exit(1)
        fh = open(DATAFILE, "r")
        a  = fh.readlines()
        fh.close()
        lines = {}
        headline = ""
        for i in a:
            i = i.rstrip("\n")
            if i == "" or i.startswith("#"):
                continue
            if "[" in i and "]" in i:
                c = i.split("[")
                c = c[1].split("]")
                headline = c[0]
                lines[headline] = []
                continue
            lines[headline].append(i)
        self.data = {}
        self.data["directories"] = {}
        for i in lines["Directories"]:
            b = i.split("=")
            b = self.stripArray(b)
            self.data["directories"][b[0]] = b[1]
        for i in lines.keys():
            if i.lower() == "directories":
                continue
            self.data[i.lower()] = []
            for u in lines[i]:
                b = u.split(",")
                b = self.stripArray(b)
                self.data[i.lower()].append(b)

    def getSettings(self, platform):

        # Define the default values of the options:

        if platform == "spectrum":
            return {"fullscreen"  : "--full-screen",
                    "soundvolume" : "--volume-beeper 15"}

        if platform == "atari":

            return {"machinetype" : "-xl",
                    "soundvolume" : "-volume 5",
                    "holdoption"  : "-nobasic",
                    "fullscreen"  : "-fullscreen"}

            """     Set in config-file:
                    "osbpath"     : "-osb_rom " + os.path.join(ATARI_ROMS_PATH, "atariosb.rom"),
                    "osxlpath"    : "-xlxe_rom " + os.path.join(ATARI_ROMS_PATH, "atarixl.rom"),
                    "basicpath"   : "-basic_rom" + os.path.join(ATARI_ROMS_PATH, "ataribas.rom"),
            """

        if platform == "amiga":
            return {"fullscreen"  : "--fullscreen=1"}

        if platform == "mame":
            return {"fullscreen"  : "",
                    "soundvolume" : "-volume -15"}


if __name__ == '__main__':
    Main()
