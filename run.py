from TelegramDTDOC import *
from CheckLinks import CheckLinks

nSecSleep = 4
links = CheckLinks()
TDT = TelegramDTDOC("INSERT THE TELEGRAM CHAT ID HERE")

while True:
    
  # Download and process the LHC and CMS page1 images...
  DownloadPages()
  TDT.GetInfoFromLHCandReport()
  TDT.GetInfoFromCMSandUpdate()

  nLinksErr = links.CheckLinksFromFile()
  if nLinksErr >= 10 and nLinksErr <= 12:
    TDT.SendTelegramAll(">>>> ERROR <<<<\n Detected error with links to slice test...")
    #links.ResetNerrors()

  print(' >> ', GetTimestamp())
  time.sleep(nSecSleep)
