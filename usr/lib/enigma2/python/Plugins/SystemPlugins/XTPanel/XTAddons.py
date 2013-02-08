from Screens.Screen import Screen
from Components.ActionMap import ActionMap,NumberActionMap
from Components.ChoiceList import ChoiceEntryComponent, ChoiceList
from Components.Pixmap import Pixmap
from Tools.Directories import SCOPE_SKIN
import os, socket, string, codecs
from enigma import *
from Screens.MessageBox import MessageBox
from Components.Label import Label
from Downloads import Downloads
from Downloads import Getipklist
from Ipkinstall import Ipkinstall 
from Ipkremove import Ipkremove
from Memory import Memory
from skins import *
from Screens.PluginBrowser import PluginBrowser, PluginDownloadBrowser
from Screens.Standby import TryQuitMainloop

from Components.Button import Button
from Components.config import config

import gettext

def _(txt):
	t = gettext.dgettext("XTPanel", txt)
	if t == txt:
		print "[XTPanel] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t


class Addons(Screen):

	def __init__(self, session, title = "", list = []):
                Screen.__init__(self, session)
                dskin = config.skin.primary_skin.value
                if dskin == "Lava/skin.xml": 
                      # self.skin = ItemList.skin
                       self.skinName = "Downloads"

                else:
                       self.skin = Extramenu.skin 
                      #self.skinName = "Downloads-default"                              
		self["title"] = Label(_("XTA team plugins"))
		self["text"] = Label(_("Please select"))                             
  		self.session = session
		
		self["helptext"] = Label(_("Move right/left to choose active Cam"))
		
		self.__keys = [ "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "blue", "yellow", "green", "red" ]

		self.keymap = {}
		
		self.list = []
		pos = 0
		for x in list:
			strpos = str(self.__keys[pos])
			self.list.append(ChoiceEntryComponent(key = strpos, text = x))
			if self.__keys[pos] != "":
				self.keymap[self.__keys[pos]] = list[pos]
			pos += 1
		self["list"] = ChoiceList(self.list)		
	
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.go,
			"back": self.cancel,
			"1": self.keyNumberGlobal,
			"2": self.keyNumberGlobal,
			"3": self.keyNumberGlobal,
			"4": self.keyNumberGlobal,
			"5": self.keyNumberGlobal,
			"6": self.keyNumberGlobal,
			"7": self.keyNumberGlobal,
			"8": self.keyNumberGlobal,
			"9": self.keyNumberGlobal,
			"0": self.keyNumberGlobal,
			"red": self.close,
			"green": self.go,
			"yellow": self.keyYellow,
			"blue": self.readme,
			"up": self.up,
			"down": self.down,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		self["key_blue"] = Button(_(" "))
                self.setTitle(title)
                self["pixmap"] = Pixmap()
#                self.onShown.append(self.openTest)

        def openTest(self):
                self["pixmap"].instance.setPixmapFromFile("/usr/share/enigma2/CTmenu/addon.png")
	
        def readme(self):
                return
	
	
	def up(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveUp)
				if self["list"].l.getCurrentSelection()[0][0] != "--" or self["list"].l.getCurrentSelectionIndex() == 0:
					break

	def down(self):
		if len(self["list"].list) > 0:
			while 1:
				self["list"].instance.moveSelection(self["list"].instance.moveDown)
				if self["list"].l.getCurrentSelection()[0][0] != "--" or self["list"].l.getCurrentSelectionIndex() == len(self["list"].list) - 1:
					break

	# runs a number shortcut
	def keyNumberGlobal(self, number):
		self.goKey(str(number))

	# runs the current selected entry
	def go(self):
		cursel = self["list"].l.getCurrentSelection()
		if cursel:
			self.goEntry(cursel[0])
		else:
			self.cancel()

	# runs a specific entry
	def goEntry(self, entry):
		keys = [ "blue", "yellow", "green", "red", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0" ]
                if entry[1] == 0:
                        self.session.open(Memory)
                elif entry[1] == 1:
                        self.session.open(Downloads)                        
 		elif entry[1] == 2:
			self.session.open(Ipkinstall)
		elif entry[1] == 3:
			self.session.open(TryQuitMainloop,retvalue=3)
		elif entry[1] == 4:
			self.session.open(Ipkremove)
		elif entry[1] == 5:
			self.close()			
			
	
	# lookups a key in the keymap, then runs it
	def goKey(self, key):
		if self.keymap.has_key(key):
			entry = self.keymap[key]
			self.goEntry(entry)

	# runs a color shortcut
	def keyRed(self):
		self.goKey("red")

	def keyGreen(self):
		self.goKey("green")

	def keyYellow(self):
		self.goKey("yellow")

	def keyBlue(self):
		self.goKey("blue")

	def cancel(self):
		self.close(None)
				





