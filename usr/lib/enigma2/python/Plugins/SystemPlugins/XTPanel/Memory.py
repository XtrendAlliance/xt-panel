from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import NumberActionMap
from Components.Input import Input
from Components.Pixmap import Pixmap
from Components.FileList import FileList
from Screens.ChoiceBox import ChoiceBox
from Plugins.Plugin import PluginDescriptor

from Screens.Console import Console
from enigma import eConsoleAppContainer

import gettext

def _(txt):
	t = gettext.dgettext("XTPanel", txt)
	if t == txt:
		print "[XTPanel] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t

############################################################
# Coded by PCD, October 2007, enhanced from Demoplugin Test #
############################################################

class Memory(Screen):
	skin = """
		<screen position="100,100" size="550,400" title=" " >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="190,250" scrollbarMode="showOnDemand" />
		</screen>"""
		
	def __init__(self, session, args = None):
		self.skin = Memory.skin
		Screen.__init__(self, session)

		self["list"] = FileList("/", matchingPattern = "^.*\.(png|avi|mp3|mpeg|ts)")
#		self["pixmap"] = Pixmap()
		
		self["text"] = Input("1234", maxSize=True, type=Input.NUMBER)
				
		self["actions"] = NumberActionMap(["WizardActions", "InputActions"],
		{
			"ok": self.ok,
			"back": self.close,
			"left": self.keyLeft,
			"right": self.keyRight,
			"1": self.keyNumberGlobal,
			"2": self.keyNumberGlobal,
			"3": self.keyNumberGlobal,
			"4": self.keyNumberGlobal,
			"5": self.keyNumberGlobal,
			"6": self.keyNumberGlobal,
			"7": self.keyNumberGlobal,
			"8": self.keyNumberGlobal,
			"9": self.keyNumberGlobal,
			"0": self.keyNumberGlobal
		}, -1)
		title = _("Memory")
                self.setTitle(title)
                self.onShown.append(self.openTest)

	def openTest(self):

                self.session.open(Console,_("Availabe memory"),["" ])
                title = "Availabe memory"
                cmd = "df -h"
                self.session.open(Console,_(title),[cmd])
                self.close()



	def callback(self, answer):
		print "answer:", answer
		self.close()
	
	def keyLeft(self):
		self["text"].left()
	
	def keyRight(self):
		self["text"].right()
	
	def ok(self):
		selection = self["list"].getSelection()
		if selection[1] == True: # isDir
			self["list"].changeDir(selection[0])
		else:
			self["pixmap"].instance.setPixmapFromFile(selection[0])
	
	def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)


















