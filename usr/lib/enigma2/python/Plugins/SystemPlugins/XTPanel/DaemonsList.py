from enigma import *
from Plugins.Plugin import PluginDescriptor
from Screens.Screen import Screen
from Components.ActionMap import ActionMap
from Components.MenuList import MenuList
from Components.GUIComponent import GUIComponent
from Components.HTMLComponent import HTMLComponent
from Tools.Directories import fileExists, crawlDirectory
from Components.MultiContent import MultiContentEntryText, MultiContentEntryPixmapAlphaTest
from Components.Button import Button
from Extra.ExtrasList import ExtrasList, SimpleEntry
from Extra.ExtraActionBox import ExtraActionBox
import os
import sys
from __init__ import _, loadPluginSkin
from Components.Ipkg import IpkgComponent
from Screens.Ipkg import Ipkg
from Screens.MessageBox import MessageBox
from time import sleep

def DaemonEntry(name, picture, description, started, installed):
    res = [(name,
      picture,
      description,
      started)]
    picture = picture[8:]
    picture = '/usr/lib/enigma2/python/Plugins/SystemPlugins/XTPanel/pictures/' + picture
    if started:
        picture2 = '/usr/share/enigma2/skin_default/icons/lock_on.png'
    else:
        picture2 = '/usr/share/enigma2/skin_default/icons/lock_off.png'
    if not installed:
        picture2 = '/usr/share/enigma2/skin_default/icons/lock_error.png'
    if fileExists(picture):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(5, 0), size=(48, 48), png=loadPNG(picture)))
    res.append(MultiContentEntryText(pos=(65, 10), size=(135, 38), font=0, text=name))
    res.append(MultiContentEntryText(pos=(210, 10), size=(280, 38), font=0, text=description))
    if fileExists(picture2):
        res.append(MultiContentEntryPixmapAlphaTest(pos=(500, 10), size=(24, 24), png=loadPNG(picture2)))
    return res


class DaemonsList(Screen):

    def __init__(self, session, args = 0):
        Screen.__init__(self, session)
        self.running = list()
        self.installed = list()
        self.daemons = list()
        self['menu'] = ExtrasList(list())
        self['menu'].onSelectionChanged.append(self.selectionChanged)
        self['key_green'] = Button('')
        self['key_red'] = Button('')
        self['key_blue'] = Button(_('Exit'))
        self['key_yellow'] = Button('')
        self['actions'] = ActionMap(['OkCancelActions', 'ColorActions'], {'blue': self.quit,
         'yellow': self.yellow,
         'red': self.red,
         'green': self.green,
         'cancel': self.quit}, -2)
        self.onFirstExecBegin.append(self.drawList)
        self.onShown.append(self.setWindowTitle)

    def setWindowTitle(self):
        self.setTitle(_('Daemons'))

    def selectionChanged(self):
        if len(self.daemons) > 0:
            index = self['menu'].getSelectionIndex()
            if self.installed[index]:
                if self.running[index]:
                    self['key_red'].setText(_('Stop'))
                else:
                    self['key_red'].setText(_('Start'))
                if self.daemons[index][6]:
                    self['key_yellow'].setText(_('Configure'))
                else:
                    self['key_yellow'].setText('')
                self['key_green'].setText('')
            else:
                self['key_red'].setText('')
                self['key_yellow'].setText('')
                if self.daemons[index][9]:
                    self['key_green'].setText(_('Install'))
                else:
                    self['key_green'].setText('')

    def drawList(self, ret = None):
        self.session.open(ExtraActionBox, _('Checking daemons status...'), _('Daemons'), self.actionDrawList)

    def actionDrawList(self):
        self.ishowed = True
        if len(self.daemons) == 0:
            self.loadList()
        self.checkInstalled()
        self.checkRunning()
        list = []
        i = 0
        for daemon in self.daemons:
            list.append(DaemonEntry(daemon[0], 'Daemons/%s' % daemon[2], daemon[1], self.running[i], self.installed[i]))
            i += 1

        self['menu'].setList(list)

    def checkRunning(self):
        self.running = list()
        for daemon in self.daemons:
            self.running.append(daemon[3]())

    def checkInstalled(self):
        self.installed = list()
        for daemon in self.daemons:
            self.installed.append(daemon[7]())

    def loadList(self):
        self.daemons = list()
        tdaemons = crawlDirectory('%s/Daemons/' % os.path.dirname(sys.modules[__name__].__file__), '.*\\.ext$')
        tdaemons.sort()
        for daemon in tdaemons:
            if daemon[1][:1] != '.':
                try:
                    src = open(os.path.join(daemon[0], daemon[1]))
                    exec src.read()
                    src.close()
                    self.daemons.append((daemon_name,
                     daemon_description,
                     daemon_icon,
                     daemon_fnc_status,
                     daemon_fnc_start,
                     daemon_fnc_stop,
                     daemon_class_config,
                     daemon_fnc_installed,
                     daemon_fnc_boot,
                     daemon_package))
                except TypeError:
                    print '[CTPanel] Could not parse daemonlist while Directory crawl. Please check .ext Files for errors.'

    def yellow(self):
        index = self['menu'].getSelectionIndex()
        try:
            if self.installed[index]:
                if self.daemons[index][6]:
                    if self.daemons[index][6] == 'XTOpenvpn':
                        from plugin import XTOpenvpn
                        self.session.open(XTOpenvpn)
                    elif self.daemons[index][6] == 'NFSServerSetup':
                        from Plugins.PLi.NFSServer.plugin import NFSServerSetup
                        self.session.open(NFSServerSetup)
                    elif self.daemons[index][6] == 'XTCronMang':
                        from plugin import XTCronMang
                        self.session.open(XTCronMang)
                    elif self.daemons[index][6] == 'XTNTPdConf':
                        self.session.open(MessageBox, _('Please visit the following Website:\nhttp://linux-fuer-alle.de/doc_show.php?docid=7\nto gain further instructions how to configure your STB as NTP-Client/Server.'), MessageBox.TYPE_INFO)
        except IndexError:
            print '[XTPANEL] no Daemon .ext files found.'

    def green(self):
        index = self['menu'].getSelectionIndex()
        if not self.installed[index]:
            if self.daemons[index][9]:
                filename = self.daemons[index][9]
                self.oktext = _('\nAfter pressing OK, please wait!')
                self.cmdList = []
                if not fileExists('/var/lib/opkg/openpli-all') and not fileExists('/var/lib/opkg/openpli-mipsel') and not fileExists('/var/lib/opkg/openpli-3rd-party'):
                    self.ipkg = IpkgComponent()
                    self.ipkg.startCmd(IpkgComponent.CMD_UPDATE)
                    sleep(5)
                self.cmdList.append((IpkgComponent.CMD_INSTALL, {'package': filename}))
                if len(self.cmdList):
                    self.session.openWithCallback(self.runUpgrade, MessageBox, _('Do you want to install the package:\n') + filename + '\n' + self.oktext)

    def red(self):
        if len(self.daemons) > 0:
            index = self['menu'].getSelectionIndex()
            if self.running[index]:
                self.session.openWithCallback(self.drawList, ExtraActionBox, _('Stopping %s...') % self.daemons[index][0], _('Daemons'), self.startstop)
            else:
                self.session.openWithCallback(self.drawList, ExtraActionBox, _('Starting %s...') % self.daemons[index][0], _('Daemons'), self.startstop)

    def startstop(self):
        if len(self.daemons) > 0:
            index = self['menu'].getSelectionIndex()
            if self.installed[index]:
                if self.running[index]:
                    self.daemons[index][5]()
                else:
                    self.daemons[index][4]()
                self.daemons[index][8](self.daemons[index][3]())

    def quit(self):
        self.close()

    def runUpgrade(self, result):
        if result:
            self.session.openWithCallback(self.runUpgradeFinished, Ipkg, cmdList=self.cmdList)

    def runUpgradeFinished(self):
        self.session.openWithCallback(self.UpgradeReboot, MessageBox, _('Installation/Upgrade finished.') + ' ' + _('Do you want to restart Enigma2?'), MessageBox.TYPE_YESNO)

    def UpgradeReboot(self, result):
        if result is None or result is False:
            self.session.open(ExtraActionBox, _('Checking daemons status...'), _('Daemons'), self.actionDrawList)
        if result:
            quitMainloop(3)