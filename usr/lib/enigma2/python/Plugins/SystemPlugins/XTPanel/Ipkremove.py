from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import NumberActionMap
from Components.Input import Input
from Components.Pixmap import Pixmap
from Components.FileList import FileList
from Screens.ChoiceBox import ChoiceBox
from Plugins.Plugin import PluginDescriptor

import os

import gettext

def _(txt):
	t = gettext.dgettext("XTPanel", txt)
	if t == txt:
		print "[XTPanel] fallback to default translation for", txt
		t = gettext.gettext(txt)
	return t
###############################
# Coded by PCD, February 2008 #
###############################

class Ipkremove(Screen):
	skin = """
		<screen position="100,100" size="550,400" title="Ipkremove" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="190,250" scrollbarMode="showOnDemand" />
			<widget name="pixmap" position="200,0" size="190,250" />
		</screen>"""
	def __init__(self, session, args = None):
		self.skin = Ipkremove.skin
		Screen.__init__(self, session)

		self["list"] = FileList("/", matchingPattern = "^.*\.(png|avi|mp3|mpeg|ts)")
		self["pixmap"] = Pixmap()
		
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
		title = _("Ipkremove")
                self.setTitle(title)
		self.onShown.append(self.openTest)

	def openTest(self):
#		self.session.openWithCallback(self.callback, MessageBox, _("Test-Messagebox?"))
#                self.session.openWithCallback(test, ChoiceBox, title="Select playlist item?", list=[(_("yes"), "yes"), (_("no"), "no"), (_("perhaps"), "perhaps"), (_("ask me tomorrow"), "ask me tomorrow"), (_("leave me alone with this!"), "yes")])
#		self.session.open(InputBox)

           try:
	       	myfile = open("/etc/ipklist_installed", "r+")
                icount = 0
                data = []
                ebuf = []

                for line in myfile:
                       data.append(icount)
                       data[icount] = (_(line), "")
#                        if icount>0:
                       ebuf.append(data[icount])
                       icount = icount + 1
                myfile.close()

                ipkres = self.session.openWithCallback(self.test2, ChoiceBox, title=(_("Please select ipkg to remove")), list=ebuf)
                self.close()
           except:
                self.close()      
                
                
        def test2(self, returnValue):
                if returnValue is None:
                       return
                else: 
                       print "returnValue", returnValue
                       nos = len
                
                       emuname = ""

                       ipkname = returnValue[0]
 	               print "ipkname =", ipkname
 	        
# 	               os.mkdir(/etc/currentEmu)
 
                       cmd = "opkg remove " + ipkname[:-1] + " >/tmp/ipk.log"
                       print cmd
                       os.system(cmd)
		       cmd = "touch /etc/tmpfile"
                       os.system(cmd)
 ###############################
        	       myfile = open("/etc/ipklist_installed", "r")
         	       f= open("/etc/tmpfile", "w")
                       icount = 0
                       for line in myfile:
                              if (line != ipkname):
                                     print "myfile line=", line
                                     f.write(line)
#                             icount = icount + 1
                       f.close()
                       f= open("/etc/tmpfile", "r+")       
                       f2 = f.readlines()
                       print "/etc/tmpfile", f2
                       f.close()
                       f= open("/etc/ipklist_installed", "r+")
                       f2 = f.readlines()
                       print "/etc/ipklist_installed", f2
                       f.close()
                        
                       cmd = "rm /etc/ipklist_installed"        
                       os.system(cmd)
                       cmd = "mv /etc/tmpfile /etc/ipklist_installed"
                       os.system(cmd)
                
                       f= open("/etc/ipklist_installed", "r+")
                       f2 = f.readlines()
                       print "/etc/ipklist_installed 2", f2
                       f.close()
                       return		

	def callback(self, answer):
		print "answer:", answer
                return
	
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


























































































