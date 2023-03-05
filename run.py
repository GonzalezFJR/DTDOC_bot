from TelegramDTDOC import *

nSecSleep = 4
TDT = TelegramDTDOC("HERE YOUR TELEGRAM BOT KEY")

while True:
    
  # All kind of automatic notifications here!
  DownloadCMSpage1()
  DownloadDAQpage()
  TakeCMSpage1bits()
  TakeDAQpagebits()
  status, update = IsCMSpage1Updated()
  if update:
    TDT.UpdateCMSstatus(status)

  print(' >> ', GetTimestamp())
  time.sleep(nSecSleep)
