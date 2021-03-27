import time
import xbmc
import xbmcvfs
import xbmcaddon
from resources.lib.epgprocess import *
import os


__addon__   = xbmcaddon.Addon()

class settings():
  def __getattr__(self, name):
    temp = __addon__.getSetting(name)
    if temp.lower() == 'true':
      return True
    elif temp.lower() == 'false':
      return False
    elif temp.isdigit():
      return int(temp)
    else:
      return temp

  def __setattr__(self, name, value):
    __addon__.setSetting(name, str(value))

  def open(self):
    __addon__.openSettings()


def refresh_cfg(epg, epg_cfg):
    epgURL = epg_cfg.epgURL
    epgOffset = int(epg_cfg.epgOffset)
    filterEPG = epg_cfg.filterEPG
    wrkdir = epg_cfg.wrkdir
    if len(wrkdir) == 0:
        if sys.version_info[0] == 2:
            wrkdir = xbmc.translatePath(__addon__.getAddonInfo('profile')).decode('utf-8')
        else:
            wrkdir = xbmcvfs.translatePath(__addon__.getAddonInfo('profile'))
    filterlist = epg_cfg.filterlist
    epgDownloadHrs = epg_cfg.epgDownloadHrs

    filtertv = []
    if filterEPG and os.path.exists(filterlist):
        with open(filterlist, 'r') as flt:
            filtertv = flt.read().split()
    epg.configure(wrkdir, epgURL, epgOffset, filtertv, epgDownloadHrs)


if __name__ == '__main__':
    monitor = xbmc.Monitor()
    epg_cfg = settings()
    wrkdir = epg_cfg.wrkdir

    epg = voyo_epg(wrkdir)
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(3):
            # Abort was requested while waiting. We should exit
            break

        refresh_cfg(epg, epg_cfg)

        if not epg.processing:
            epg.run()
            #epg.start()
            #epg.join()

