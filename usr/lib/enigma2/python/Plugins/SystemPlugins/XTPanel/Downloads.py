from Plugins.Plugin import PluginDescriptor
from Components.Sources.List import List
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from enigma import eTimer, quitMainloop, RT_HALIGN_LEFT, RT_VALIGN_CENTER, eListboxPythonMultiContent, eListbox, gFont, getDesktop, ePicLoad
from Tools.LoadPixmap import LoadPixmap
from enigma import getDesktop

import urllib
from urllib2 import urlopen
from Components.MenuList import MenuList
from Components.Label import Label
from Tools.Directories import fileExists, resolveFilename, SCOPE_SKIN_IMAGE, SCOPE_LANGUAGE, SCOPE_PLUGINS


from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Components.ActionMap import NumberActionMap
from Components.Input import Input
from Components.Pixmap import Pixmap
from Components.FileList import FileList
from Screens.ChoiceBox import ChoiceBox
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import ActionMap
from Screens.InputBox import InputBox
from Ipkinstall import Ipkinstall

from twisted.web.client import getPage, downloadPage
import os
from Components.Button import Button

from Components.Task import Task, Job, job_manager as JobManager, Condition
from Screens.TaskView import JobView

##################################################
# Coded by pcd@www.dreamforum.nu, September 2009 #
##################################################


class RSList(MenuList):
	def __init__(self, list):
		MenuList.__init__(self, list, False, eListboxPythonMultiContent)
		self.l.setItemHeight(30)
		self.l.setFont(0, gFont("Regular", 20))

##############################################################################

def RSListEntry(download, state):
	res = [(download)]
	res.append(MultiContentEntryText(pos=(10, 0), size=(370, 25), font=0, text=download))
        if state == 0:
              res.append(MultiContentEntryPixmapAlphaTest(pos=(600, 0), size=(50,30), png=LoadPixmap(cached=True, desktop=getDesktop(0), path=resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/buttons/green.png"))))
        else:
              res.append(MultiContentEntryPixmapAlphaTest(pos=(600, 0), size=(50,30), png=LoadPixmap(cached=True, desktop=getDesktop(0), path=resolveFilename(SCOPE_SKIN_IMAGE, "skin_default/buttons/red.png"))))

	print "res =", res
        return res

##############################################################################







class Downloads(Screen):

    skin = """
		<screen position="center,center" size="520,400" title=" " >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,40" size="500,350" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<!--eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" /-->
			<widget name="info" position="80,80" zPosition="4" size="350,300" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="left" valign="center" />
		</screen>"""

     

    def __init__(self, session):
		self.skin = Downloads.skin
		Screen.__init__(self, session)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
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
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		title = "Download Categories"
		self["title"] = Button(title)		
                self.icount = 0
                self.errcount = 0
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                       xurl = "http://www.et-view-support.com/addons/XTA-team/" + "list.txt"
                       print "xurl =", xurl
                       getPage(xurl).addCallback(self.gotPage).addErrback(self.getfeedError)

    def gotPage(self, html):
#	        try:
        	       print "html = ", html 
                       self.data = []
                       icount = 0
                       self.data = html.splitlines()

                       print "self.data =", self.data
		       self["info"].setText("")
                       self["list"].setList(self.data)

#                except Exception, error:
#			print "[TDw]: Could not download HTTP Page\n" + str(error)

    def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error

    def okClicked(self):
	  if self.errcount == 1:
                self.close()
          else:      
                sel = self["list"].getSelectionIndex()
                addon = self.data[sel]
                self.session.open(Getipklist, addon)
                
    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)

class Getipklist(Screen):


    skin = """
		<screen position="center,center" size="800,400" title=" " >
			<widget name="text" position="100,20" size="200,30" font="Regular;20" halign="left" />
                        <!--widget name="list" position="10,150" size="500,350" scrollbarMode="showOnDemand" /-->
                        <widget name="list" position="50,80" size="730,300" scrollbarMode="showOnDemand" />

                        <!--eLabel text="Already installed" position="100,20" size="200,30" font="Regular;20" halign="left" /-->
                        <ePixmap name="red"    position="270,20"   zPosition="4" size="50,30" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />

			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="100,230" zPosition="4" size="300,25" font="Regular;18" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
		</screen>"""



    def __init__(self, session, addon):
		self.skin = Getipklist.skin
		Screen.__init__(self, session)

        	self.list = []
                self["text"] = Label()
                self["text"].setText(_("Already installed"))
                
                self["list"] = List(self.list)
                self["list"] = RSList([])

		self["info"] = Label()
                self["actions"] = NumberActionMap(["WizardActions", "InputActions", "ColorActions", "DirectionActions"], 
		{
			"ok": self.okClicked,
			"back": self.close,
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
			"green": self.okClicked,
		}, -1)
	        self["key_red"] = Button(_("Cancel"))
		self["key_green"] = Button(_("Select"))
		title = addon + " List"
		self["title"] = Button(title)
                self.addon = addon
                self.icount = 0
                self.names = []
                self.onLayoutFinish.append(self.openTest)
                
    def openTest(self):
                self["info"].setText("Downloading list...")
                testno = 1
                
                xurl = "http://www.et-view-support.com/addons/XTA-team/" + self.addon + "/list.txt"
                print "xurl =", xurl
                getPage(xurl).addCallback(self.gotPage).addErrback(self.getfeedError)

    def gotPage(self, html):
#	        try:
        	       print "html = ", html 
                       self.data = []
                       icount = 0
                       self.data = html.splitlines()

#                       print "self.data =", self.data
                       list = []
                       for line in self.data:
                               ipkname = self.data[icount] 
                               
                               print "gotPage icount, ipk name =", icount, ipkname 
                               ipos = ipkname.find("_")
                               remname = ipkname[:ipos]
                               state = self.getstate(remname)
                               print "gotPage state, remname = ", state, remname
                            #   state = 0 not installed 1 installed
                               list.append(RSListEntry(remname, state))
                               
                               icount = icount+1

		       self["list"].setList(list)
		       print 'self["list"] A =', self["list"] 
                       
                       self["info"].setText("")
                       
    def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error
                

    def getstate(self, remname):
            try:
	       	myfile = open("/etc/ipklist_installed", "r+")
                icount = 0
                data = []
                ebuf = []

                for line in myfile:
                       data.append(icount)
                       data[icount] = line[:-1]
                       print "getstate data[icount], remname = ", data[icount], remname
                       if data[icount] == remname:
                               state = 1
                               return state
                       icount = icount + 1
                myfile.close()

#                ipkres = self.session.openWithCallback(self.test2, ChoiceBox, title="Please select ipkg to remove", list=ebuf)
                state = 0
                return state
            except:
                state = 0
                return state     
    

    def okClicked(self):
	        sel = self["list"].getSelectionIndex()
                ipk = self.data[sel]
                addon = self.addon
                self.session.open(Getipk, ipk, addon)
                
    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)		

class Getipk(Screen):
    skin = """
		<screen position="center,center" size="800,500" title="Play Options" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,20" size="750,350" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="50,50" zPosition="4" size="500,400" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="left" valign="top" />
		        <ePixmap name="red"    position="0,450"   zPosition="2" size="140,40" pixmap="skin_default/buttons/red.png" transparent="1" alphatest="on" />
	                <ePixmap name="green"  position="140,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/green.png" transparent="1" alphatest="on" />
	                <ePixmap name="yellow" position="280,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/yellow.png" transparent="1" alphatest="on" /> 
	                <!--ePixmap name="blue"   position="420,450" zPosition="2" size="140,40" pixmap="skin_default/buttons/blue.png" transparent="1" alphatest="on" /--> 

	                <widget name="key_red" position="0,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
	                <widget name="key_green" position="140,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /> 
	                <widget name="key_yellow" position="280,450" size="140,40" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" />
	                <!--widget name="key_blue" position="420,450" size="140,50" valign="center" halign="center" zPosition="4"  foregroundColor="#ffffff" font="Regular;20" transparent="1" shadowColor="#25062748" shadowOffset="-2,-2" /-->
                </screen>"""
 
    def __init__(self, session, ipk, addon):
		Screen.__init__(self, session)
                self.skin = Getipk.skin
                title = "Addon Install"
                self.setTitle(title)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["key_red"] = Button(_("Exit"))
		self["key_green"] = Button(_("Download"))
		self["key_yellow"] = Button(_("Install"))
#		self["key_blue"] = Button(_("Stop Download"))
                self["setupActions"] = ActionMap(["SetupActions", "ColorActions", "TimerEditActions"],
		{
			"red": self.close,
			"green": self.okClicked,
			"yellow": self.install,
#			"blue": self.stopdl,
			"cancel": self.cancel,
			"ok": self.close,
		}, -2)

                print "Getipk : ipk =", ipk
                self.icount = 0
                self.ipk = ipk
                self.addon = addon
                 
                self.onLayoutFinish.append(self.openTest)
#                self["info"].setText("Must do (1) Download  (2) Play. \n\nVideo selected :-  " + self.name)
                txt = "You have selected\n\n" + ipk + "\n\n\nPlease press Download"
                self["info"].setText(txt)

                self.srefOld = self.session.nav.getCurrentlyPlayingServiceReference()
                self.onLayoutFinish.append(self.openTest)

    def openTest(self):
                xurl1 = "http://www.et-view-support.com/addons/XTA-team/" + self.addon + "/"        
                print "xurl1 =", xurl1
                xurl2 = xurl1 + self.ipk
                print "xurl2 =", xurl2
                xdest = "/tmp/" + self.ipk
                print "xdest =", xdest
                self.svfile = xdest
                self.cmd = 'wget -O "' + xdest + '" "' + xurl2 + '"'
                    

    def okClicked(self):
                print "self.cmd = ", self.cmd
                JobManager.AddJob(downloadJob(self, self.cmd, self.svfile, 'Title 1')) 
                txt = "Please press Install" 
                self["info"].setText(txt)
                self.LastJobView()

 
    def LastJobView(self):
		currentjob = None
		for job in JobManager.getPendingJobs():
			currentjob = job

		if currentjob is not None:
			self.session.open(JobView, currentjob)
 
    def install(self):
                       cmd = "opkg install --force-overwrite /tmp/" + self.ipk + ">/tmp/ipk.log"
                       print "cmd =", cmd
                       os.system(cmd)
                       self.viewLog()

    def viewLog(self):
          self["info"].setText("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n       Press Exit to continue...")
#          self["info"].setText(" ")
          if os.path.isfile("/tmp/ipk.log")is not True :
                cmd = "touch /tmp/ipk.log"
                os.system(cmd)
	  else:     	
                myfile = file(r"/tmp/ipk.log")
                icount = 0
                data = []
                for line in myfile.readlines():
                      data.append(icount)
                      print line
                      num = len(line)
                      data[icount] = (line[:-1])
                      print data[icount]
      
                      icount = icount + 1
                self["list"].setList(data)
                self.endinstall()

    def endinstall(self):
                path="/tmp"
                tmplist = []
                ipkname = 0  
                tmplist=os.listdir(path)
                print "files in /tmp", tmplist
                icount = 0
                for name in tmplist:
                       nipk = tmplist[icount]
                       if (nipk[-3:]=="ipk"):
                              ipkname = nipk
                       icount = icount+1       

                if ipkname != 0:               
                       print "endinstall ipk name =", ipkname 
                       ipos = ipkname.find("_")
                       remname = ipkname[:ipos]
                       print "endinstall remname =", remname
                       f=open('/etc/ipklist_installed', 'a')
                       f1= remname + "\n"
                       f.write(f1)
                       cmd = "rm /tmp/*.ipk"
                       os.system(cmd)                 
                        
                               
    
    def cancel(self):
                self.close()

    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()

    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)
		
		

class Getipk2(Screen):

    skin = """
		<screen position="center,center" size="600,470" title="Install status" >
			<!--widget name="text" position="0,0" size="550,25" font="Regular;20" /-->
			<widget name="list" position="10,0" size="630,400" scrollbarMode="showOnDemand" />
			<!--widget name="pixmap" position="200,0" size="190,250" /-->
			<eLabel position="70,100" zPosition="-1" size="100,69" backgroundColor="#222222" />
			<widget name="info" position="100,420" zPosition="4" size="300,35" font="Regular;22" foregroundColor="#ffffff" transparent="1" halign="center" valign="center" />
		</screen>"""

    def __init__(self, session, ipk, addon):
		self.skin = Getipk.skin
		Screen.__init__(self, session)

        	self["list"] = MenuList([])
		self["info"] = Label()
                self["actions"] = ActionMap(["OkCancelActions"], {"ok": self.okClicked, "cancel": self.close}, -1)
                self.icount = 0
                self.ipk = ipk
                self.addon = addon
                 
                self.onLayoutFinish.append(self.openTest)
   
    
    def openTest(self):
                self["info"].setText("Downloading and installing...")
                device = open("/proc/stb/info/model", "r").readline().strip()
                if device == "dm800":
                       xurl1 = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/oe2-dm800hd/" + self.addon + "/"
                else:                
                       xurl1 = "http://www.turk-dreamworld.com/bayraklar/Receiverler/Dreambox/TDW/e2/addons/oe2/" + self.addon + "/"
        
                print "xurl1 =", xurl1
                xurl2 = xurl1 + self.ipk
                print "xurl2 =", xurl2
                xdest = "/tmp/" + self.ipk
                print "xdest =", xdest
                downloadPage(xurl2, xdest).addCallback(self.gotPage)

    def gotPage(self,txt=""):
                       print "in gotPage"
                       self["info"].setText("")
                       cmd = "opkg install --force-overwrite /tmp/" + self.ipk + ">/tmp/ipk.log"
                       print "cmd =", cmd
                       os.system(cmd)
                       self.viewLog()
                       
    def getfeedError(self, error=""):
		error = str(error)
		print "Download error =", error

    def keyLeft(self):
		self["text"].left()
	
    def keyRight(self):
		self["text"].right()
		
    def okClicked(self):
                self.close()		
 
	
    def keyNumberGlobal(self, number):
		print "pressed", number
		self["text"].number(number)		
		


    def viewLog(self):
          self["info"].setText("Press OK to continue...")
          if os.path.isfile("/tmp/ipk.log")is not True :
                cmd = "touch /tmp/ipk.log"
                os.system(cmd)
	  else:     	
                myfile = file(r"/tmp/ipk.log")
                icount = 0
                data = []
                for line in myfile.readlines():
                      data.append(icount)
                      print line
                      num = len(line)
                      data[icount] = (line[:-1])
                      print data[icount]
      
                      icount = icount + 1
                self["list"].setList(data)
                self.endinstall()

    def endinstall(self):
                path="/tmp"
                tmplist = []
                ipkname = 0  
                tmplist=os.listdir(path)
                print "files in /tmp", tmplist
                icount = 0
                for name in tmplist:
                       nipk = tmplist[icount]
                       if (nipk[-3:]=="ipk"):
                              ipkname = nipk
                       icount = icount+1       

                if ipkname != 0:               
                       print "ipk name =", ipkname 
                       ipos = ipkname.find("_")
                       remname = ipkname[:ipos]
                       print "remname =", remname
                       f=open('/etc/ipklist_installed', 'a')
                       f1= remname + "\n"
                       f.write(f1)
                       cmd = "rm /tmp/*.ipk"
                       os.system(cmd)                 
 
class downloadJob(Job):
	def __init__(self, toolbox, cmdline, filename, filetitle):
		Job.__init__(self, _("Downloading"))
		self.toolbox = toolbox
		self.retrycount = 0
		
                downloadTask(self, cmdline, filename, filetitle)

	def retry(self):
		assert self.status == self.FAILED
		self.retrycount += 1
		self.restart()
	
class downloadTask(Task):
	ERROR_CORRUPT_FILE, ERROR_RTMP_ReadPacket, ERROR_SEGFAULT, ERROR_SERVER, ERROR_UNKNOWN = range(5)
	def __init__(self, job, cmdline, filename, filetitle):
		Task.__init__(self, job, filetitle)
#		self.postconditions.append(downloadTaskPostcondition())
		self.setCmdline(cmdline)
		self.filename = filename
		self.toolbox = job.toolbox
		self.error = None
		self.lasterrormsg = None
		
	def processOutput(self, data):
		try:
			if data.endswith('%)'):
				startpos = data.rfind("sec (")+5
				if startpos and startpos != -1:
					self.progress = int(float(data[startpos:-4]))
			elif data.find('%') != -1:
				tmpvalue = data[:data.find("%")]
				tmpvalue = tmpvalue[tmpvalue.rfind(" "):].strip()
				tmpvalue = tmpvalue[tmpvalue.rfind("(")+1:].strip()
				self.progress = int(float(tmpvalue))
			else:
				Task.processOutput(self, data)
		except Exception, errormsg:
			print "Error processOutput: " + str(errormsg)
			Task.processOutput(self, data)

	def processOutputLine(self, line):
			self.error = self.ERROR_SERVER
			
	def afterRun(self):
		pass

class downloadTaskPostcondition(Condition):
	RECOVERABLE = True
	def check(self, task):
		if task.returncode == 0 or task.error is None:
			return True
		else:
			return False

	def getErrorMessage(self, task):
		return {
			task.ERROR_CORRUPT_FILE: _("Video Download Failed!Corrupted Download File:%s" % task.lasterrormsg),
			task.ERROR_RTMP_ReadPacket: _("Video Download Failed!Could not read RTMP-Packet:%s" % task.lasterrormsg),
			task.ERROR_SEGFAULT: _("Video Download Failed!Segmentation fault:%s" % task.lasterrormsg),
#			task.ERROR_SERVER: _("Download Failed!-Server error:%s" % task.lasterrormsg),
			task.ERROR_SERVER: _("Download Failed!-Server error:"),
			task.ERROR_UNKNOWN: _("Download Failed!Unknown Error:%s" % task.lasterrormsg)
		}[task.error]


            
 

def main(session, **kwargs):
        session.open(Downloads)
        
		

def Plugins(**kwargs):
	return PluginDescriptor(name="PluginDownload", description="Download/install plugins ", where = PluginDescriptor.WHERE_PLUGINMENU, fnc=main)



































