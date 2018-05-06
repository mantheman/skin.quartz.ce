import xbmcaddon
import xbmcgui
import time
import os
import subprocess
import sys
 
#addon       = xbmcaddon.Addon()
#addonname   = addon.getAddonInfo('name')

use_shell = False
appid = "Kodi"

atv2_path = "/User/Library/Preferences/%s/addons/skin.quartz.ce-master/scripts/" % appid
macosx_path = "~/Library/Application Support/%s/addons/skin.quartz.ce-master/scripts/" % appid
linux1_path = "/var/lib/%s/.%s/addons/skin.quartz.ce-master/scripts/" % (appid.lower(), appid.lower())
linux2_path = "~/.%s/addons/skin.quartz.ce-master/scripts/" % appid.lower()
android1_path = "Android/data/org.%s.%s/files/.%s/addons/skin.quartz.ce-master/scripts/" % (appid.lower(), appid.lower(), appid.lower())
android2_path = "/sdcard/%s/skin.quartz.ce-master/scripts/" % android1_path
firetv_path = "/storage/emulated/0/%s/skin.quartz.ce-master/scripts/" % android1_path

if sys.platform == "win32":
	win32_path = "%s\\%s\\addons\\skin.quartz.ce-master\\scripts\\" % (os.environ["appdata"], appid)
	if os.path.exists(win32_path):
		path =  win32_path
		use_shell = True
elif sys.platform == "darwin" and os.path.exists(atv2_path):
		path = atv2_path
elif sys.platform == "darwin" and os.path.exists(os.path.expanduser(macosx_path)):
		path = macosx_path
else: #Linux/Android
	if os.path.exists(os.path.expanduser(linux1_path)):
		path = os.path.expanduser(linux1_path)
	elif os.path.exists(os.path.expanduser(linux2_path)):
		path = os.path.expanduser(linux2_path)
	elif os.path.exists(firetv_path):
		path = firetv_path
	elif os.path.exists(android2_path):
		path = android2_path
	elif os.path.exists(android1_path):
		path = android1_path

path = path + "texturecache.py"

answer = xbmcgui.Dialog().yesno('Texture Cache Maintenance utility', 'This may take awhile to run.', '', 'Sure you want to continue?')               
if not answer: sys.exit(0)
 
dialog = xbmcgui.DialogProgress()
dialog.create('Texture Cache Maintenance utility', ("Initiating"))

p = subprocess.Popen(['python', path, 'c'], 
	bufsize=1, shell=use_shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

while True:
	line = p.stdout.readline()
	if line != b'':
		dialog.update(0, ("processing..."), "", (line))
	else:
		break
	if dialog.iscanceled():
		break

streamdata = p.communicate()[0]
rc = p.returncode		
p.stdout.close()

time.sleep(4)

if (not rc) and dialog.iscanceled(): 
	xbmcgui.Dialog().ok('Luke', "You switched off your targeting computer.", "", "What's wrong?")
elif not rc:
	xbmcgui.Dialog().ok('Success', 'TCM completed processing without any errors.')
else:
	xbmcgui.Dialog().ok('Ooops!', 'TCM was not able to do its thing.', '', 'Please ensure the KODI webserver is running with default settings.')