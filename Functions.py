import os, sys
from datetime import datetime
import time
import cv2

### Web pages
pathToLHCpage1 = 'https://vistar-capture.s3.cern.ch/lhc1.png'
pathToCMSpage1 = 'https://vistar-capture.s3.cern.ch/cms.png'
pathToDAQpage = 'http://cmsonline.cern.ch/daqStatusSCX/aDAQmon/DAQstatusGre.jpg'
pathToEventDisplay = 'https://cmsonline.cern.ch/evtdisp/3DTower.png'
pathToLHCpowering = 'https://lhcpoweringtests.web.cern.ch/lhcpoweringtests/PTplanning.png'
pngnameLHC = "lhc1.png"
pngnameCMS = "cms.png"
pngnameDAQ = "DAQstatusGre.jpg"

def DownloadLHCpage1():
  if os.path.isfile(pngnameLHC): os.system('rm %s'%pngnameLHC)
  command = "wget -q " + pathToLHCpage1 + " > /dev/null"
  os.system(command)

def DownloadCMSpage1():
  if os.path.isfile(pngnameCMS): os.system('rm %s'%pngnameCMS)
  command = "wget -q " + pathToCMSpage1 + " > /dev/null"
  os.system(command)

def DownloadDAQpage():
  if os.path.isfile(pngnameDAQ): os.system('rm %s'%pngnameDAQ)
  command = "wget -q " + pathToDAQpage + " > /dev/null"
  os.system(command)

def DownloadPages():
  DownloadLHCpage1()
  DownloadCMSpage1()
  DownloadDAQpage()

def GetTimeNow():
  return datetime.now()

def GetTimestamp():
  return GetTimeNow().strftime("%d-%b-%Y (%H:%M:%S.%f)")

def GetHelp():
  ''' Returns help for telegram users '''
  msg  = "Here you have a list of commands...\n"
  msg += " > cms - Get the CMS page1 pic\n"
  msg += " > lhc - Get the LHC page1 pic\n"
  msg += " > daq - Get the DAQ status pic\n"
  #msg += " > status - Get the status the LHC\n"
  #msg += " > run [run number] - Get info of the current or given run\n"
  #msg += " > fill [run number] - Get info of the current or given fill\n"
  return msg





# For notifications
##############################################################

def TakeCMSpage1bits():
  if not os.path.isfile(pngnameCMS): DownloadCMSpage1()
  img = cv2.imread(pngnameCMS) 
  fill = img[35:70, 540:630]
  #run = img[35:70, 850:1200]
  #dt_daq = img[700:725, 580:720]
  #dt_dcs = img[700:725, 700:800]
  # If exists, move images to old
  if os.path.isfile('fill.png'): os.system('mv fill.png fill_old.png')
  # Save the images to new ones
  time.sleep(0.1)
  cv2.imwrite('fill.png', fill)

def TakeDAQpagebits():
  if not os.path.isfile(pngnameDAQ): DownloadDAQpage()
  img = cv2.imread(pngnameDAQ) 
  run = img[0:70, 680:850]
  dt_daq = img[360:375, 620:800]
  daq = img[160:520, 620:920]
  # If exists, move images to old
  if os.path.isfile('dt_daq.png'): os.system('mv dt_daq.png dt_daq_old.png')
  if os.path.isfile('daq.png'): os.system('mv daq.png daq_old.png')
  if os.path.isfile('run.png'): os.system('mv run.png run_old.png')
  # Save the images to new ones
  time.sleep(0.1)
  cv2.imwrite('dt_daq.png', dt_daq)
  cv2.imwrite('daq.png', daq)
  cv2.imwrite('run.png', run)

def DoesImageChange(fname, fname_old):
  if os.path.isfile(fname_old) and os.path.isfile(fname):
    img = cv2.imread(fname)
    img_old = cv2.imread(fname_old)
    diff = cv2.absdiff(img, img_old)
    mse = cv2.mean(diff)[0]
    if mse > 5:
      print('There is a change in image %s (mse = %f)'%(fname, mse))
      return True
  return False

def IsCMSpage1Updated():
  status = {'fill':False, 'run':False, 'daq':False, 'dcs':False}
  update = False
  if DoesImageChange('fill.png', 'fill_old.png'): 
    print('Fill has changed!')
    status['fill'] = 'fill.png'
    update = True
  if DoesImageChange('run.png', 'run_old.png'): 
    print('Run has changed!')
    status['run'] = 'run.png'
    update = True
  if DoesImageChange('dt_daq.png', 'dt_daq_old.png'):
    print('DT DAQ status has changed!')
    status['daq'] = 'dt_daq.png'
    update = True
  return status, update
