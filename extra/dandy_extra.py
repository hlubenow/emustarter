# Extra-code for switching "^"-key off during Atari-game "Dandy".
# Would have to be pasted into "emustarter.py".

class System:

    # ....

    def start(self, gamenumber):

        if self.platform == "amiga":
            amigaconfigurationfile = os.path.join(self.paths["AMIGA_CONFIGURATIONS_PATH"], self.gamedata[gamenumber][1])
            if not os.path.exists(amigaconfigurationfile):
                print("Error: Amiga configuration file\n\n\"" + amigaconfigurationfile + "\"\n\nnot found. Can't start game. Aborting.\n")
                return

        if self.platform == "atari" and self.gamename == "Dandy":
            self.setDandyKey("off")

        if self.options["start"]:
            time.sleep(2)
            os.system(self.startstring)

        if self.platform == "atari" and self.gamename == "Dandy":
            self.setDandyKey("on")

    def setDandyKey(self, on_or_off):
        # In bash: Use "xmodmap -pke" to show settings.
        keyoff = "keycode 49 ="
        keyon  = "keycode 49 = asciicircum degree asciicircum degree notsign notsign notsign"
        print
        execstr = 'xmodmap -e "'
        if on_or_off == "off":
            print("Playing Dandy: Switching ^-key off.")
            execstr += keyoff
        else:
            print("Dandy finished: Switching ^-key on again.")
            execstr += keyon
        execstr += '"'
        os.system(execstr)
