from TelegramDTDOC import *

nSecSleep = 10
TDT = TelegramDTDOC("YOUR_BOT_ID HERE")
nUpdateRun = 0
nUpdateComments = 0
nUpdateFill = 0
nNoRun = 0
while True:
    
  # All kind of automatic notifications here!
  try:
    DownloadCMSpage1()
    DownloadDAQpage()
    TakeCMSpage1bits() # Fill and comments
    TakeDAQpagebits()  # Run and DT DAQ status
    status = IsCMSpage1Updated() 
    nUpdateRun      = 0 if not status['run'     ] else (nUpdateRun+1)
    nUpdateComments = 0 if not status['comments'] else (nUpdateComments+1)
    nUpdateFill     = 0 if not status['fill'    ] else (nUpdateFill+1)
    nNoRun          = 0 if not status['norun'   ] else (nNoRun+1)
  except:
    print('is there something wrong with the internet connexion?')
    pass

  if nUpdateRun >= 5:
    nUpdateRun = 0
    if nNoRun >= 3:
      TDT.UpdateCMSstatusNoRun()
    else: 
      TDT.UpdateCMSstatusRun()

  if nUpdateComments >= 5:
    nUpdateComments = 0
    TDT.UpdateCMScomments()

  if nUpdateFill >= 5:
    nUpdateFill = 0
    TDT.UpdateFill() 

  print(' >> ', GetTimestamp(), '[run = %d, comments = %d, fill = %d]'%(nUpdateRun, nUpdateComments, nUpdateFill))
  time.sleep(nSecSleep)
