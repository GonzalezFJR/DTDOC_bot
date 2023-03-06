import os, sys
from datetime import datetime
import time
import cv2
import numpy as np
from urllib.request import urlopen

### Web pages
pathToLHCpage1 = 'https://vistar-capture.s3.cern.ch/lhc1.png'
pathToCMSpage1 = 'https://vistar-capture.s3.cern.ch/cms.png'
pathToDAQpage = 'http://cmsonline.cern.ch/daqStatusSCX/aDAQmon/DAQstatusGre.jpg'
pathToEventDisplay = 'https://cmsonline.cern.ch/evtdisp/3DTower.png'
pathToLHCpowering = 'https://lhcpoweringtests.web.cern.ch/lhcpoweringtests/PTplanning.png'
pngnameLHC = "lhc1.png"
pngnameCMS = "cms.png"
pngnameDAQ = "DAQstatusGre.jpg"

def SaveFromWeb(url, name):
  ''' Save a file from a web page '''
  img_arr = np.asarray(bytearray(urlopen(url).read()), dtype=np.uint8)
  img = cv2.imdecode(img_arr, cv2.IMREAD_UNCHANGED)
  cv2.imwrite(name, img)

def DownloadLHCpage1():
  if os.path.isfile(pngnameLHC): os.system('rm %s'%pngnameLHC)
  SaveFromWeb(pathToLHCpage1, pngnameLHC)
  
def DownloadCMSpage1():
  if os.path.isfile(pngnameCMS): os.system('rm %s'%pngnameCMS)
  SaveFromWeb(pathToCMSpage1, pngnameCMS)

def DownloadDAQpage():
  if os.path.isfile(pngnameDAQ): os.system('rm %s'%pngnameDAQ)
  SaveFromWeb(pathToDAQpage, pngnameDAQ)

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
  msg += " > notifications on/off - Activate or deactivate notifications\n"
  return msg





# For notifications
##############################################################

def TakeCMSpage1bits():
  if not os.path.isfile(pngnameCMS): DownloadCMSpage1()
  img = cv2.imread(pngnameCMS) 
  fill = img[35:70, 540:630]
  comments = img[549:737, 5:513]
  #run = img[35:70, 850:1200]
  #dt_daq = img[700:725, 580:720]
  #dt_dcs = img[700:725, 700:800]
  # If exists, move images to old
  if os.path.isfile('fill.png'): os.system('mv fill.png fill_prev.png')
  if os.path.isfile('comments.png'): os.system('mv comments.png comments_prev.png')
  # Save the images to new ones
  time.sleep(0.1)
  cv2.imwrite('fill.png', fill)
  cv2.imwrite('comments.png', comments)

def TakeDAQpagebits():
  if not os.path.isfile(pngnameDAQ): DownloadDAQpage()
  img = cv2.imread(pngnameDAQ) 
  run = img[30:70, 690:763]
  dt_daq = img[360:375, 620:800]
  daq = img[6:520, 610:925]
  # If exists, move images to old
  if os.path.isfile('dt_daq.png'): os.system('mv dt_daq.png dt_daq_prev.png')
  if os.path.isfile('daq.png'): os.system('mv daq.png daq_prev.png')
  if os.path.isfile('run.png'): os.system('mv run.png run_prev.png')
  # Save the images to new ones
  time.sleep(0.1)
  cv2.imwrite('dt_daq.png', dt_daq)
  cv2.imwrite('daq.png', daq)
  cv2.imwrite('run.png', run)

def IsBlankImage(fname):
  ''' Check if the image is blank (no run number) '''
  if not os.path.isfile(fname): return True
  img = cv2.imread(fname)
  img = cv2.addWeighted(img, 1.5, np.zeros(img.shape, img.dtype), 0, 0)
  img = img[0:img.shape[0]-5, 0:img.shape[1]]
  img = img.astype(np.float32)
  mse = img.std()/len(img)
  if mse < 0.1: 
    return True
  return False

def DoesImageChange(fname, fname_ref, fname_prev):
  if not os.path.isfile(fname): return False
  if not os.path.isfile(fname_ref): 
    os.system('mv %s %s'%(fname, fname_ref))
    return False
  if not os.path.isfile(fname_prev):
    os.system('mv %s %s'%(fname, fname_prev))
    return False
  img      = cv2.imread(fname)
  img_prev = cv2.imread(fname_prev)
  img_ref  = cv2.imread(fname_ref)
  diff_prev = cv2.absdiff(img, img_prev)
  diff_ref  = cv2.absdiff(img, img_ref)
  mse_prev = cv2.mean(diff_prev)[0]
  mse_ref  = cv2.mean(diff_ref)[0]
  if mse_prev == 0.0 and mse_ref > 0.0:
    print('There is a change in image %s (mse ref = %f, mse prev = %f)'%(fname, mse_ref, mse_prev))
    return True
  return False

def IsCMSpage1Updated():
  status = {'fill':False, 'run':False, 'norun':False, 'daq':False, 'dcs':False, 'comments':False}
  if IsBlankImage('run.png'):
    status['norun'] = True
  if DoesImageChange('fill.png', 'fill_ref.png', 'fill_prev.png'): 
    print('Fill has changed!')
    status['fill'] = True
  if DoesImageChange('run.png', 'run_ref.png', 'run_prev.png'):
    print('Run has changed!')
    status['run'] = True
  if DoesImageChange('dt_daq.png', 'dt_daq_ref.png', 'dt_daq_prev.png'):
    print('DT DAQ status has changed!')
    status['daq'] = True
  if DoesImageChange('comments.png', 'comments_ref.png', 'comments_prev.png'):
    print('New message from page1!')
    status['comments'] = True
  return status