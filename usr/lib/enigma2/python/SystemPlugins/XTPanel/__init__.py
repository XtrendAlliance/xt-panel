from Components.Language import language
from Components.config import config
from Tools.Directories import resolveFilename, SCOPE_PLUGINS, SCOPE_LANGUAGE
import os, gettext
from skin import loadSkin
PluginLanguageDomain = 'XTPanel'
PluginLanguagePath = 'SystemPlugins/XTPanel/locale'

def loadSkinReal(skinPath):
    if os.path.exists(skinPath):
        print '[XTPanel] Loading skin ', skinPath
        loadSkin(skinPath)


def loadPluginSkin(pluginPath):
    loadSkinReal(pluginPath + '/' + config.skin.primary_skin.value)
    loadSkinReal(pluginPath + '/skin.xml')


def localeInit():
    lang = language.getLanguage()[:2]
    os.environ['LANGUAGE'] = lang
    print '[XTPanel] set language to ', lang
    gettext.bindtextdomain(PluginLanguageDomain, resolveFilename(SCOPE_PLUGINS, PluginLanguagePath))


def _(txt):
    t = gettext.dgettext(PluginLanguageDomain, txt)
    if t == txt:
        print '[XTPanel] fallback to default translation for', txt
        t = gettext.gettext(txt)
    return t


localeInit()
language.addCallback(localeInit)