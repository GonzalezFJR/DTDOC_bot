from TelegramDTDOC import *

nSecSleep = 10
TDT = TelegramDTDOC("YOUR_BOT_ADDRESS")
nUpdateRun = 0
nUpdateComments = 0
nUpdateFill = 0
while True:
    
  # All kind of automatic notifications here!
  try:
    DownloadCMSpage1()
    DownloadDAQpage()
    TakeCMSpage1bits() # Fill and comments
    TakeDAQpagebits()  # Run and DT DAQ status
    status = IsCMSpage1Updated()
    if status['run'] and status['daq']: nUpdateRun      += 1
    if status['comments']             : nUpdateComments += 1
    if status['fill']                 : nUpdateFill     += 1
  except:
    pass

  if nUpdateRun >= 5:
    nUpdateRun = 0
    TDT.UpdateCMSstatusRun(status)

  if nUpdateComments >= 5:
    nUpdateComments = 0
    TDT.UpdateCMScomments()

  if nUpdateFill >= 5:
    nUpdateFill = 0
    TDT.UpdateFill() 

  print(' >> ', GetTimestamp(), '[run = %d, comments = %d, fill = %d]'%(nUpdateRun, nUpdateComments, nUpdateFill))
  time.sleep(nSecSleep)
