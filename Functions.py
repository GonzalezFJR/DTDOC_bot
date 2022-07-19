import os, sys
from datetime import datetime
import time

### Web pages
pathToLHCpage1 = 'https://vistar-capture.s3.cern.ch/lhc1.png'
pathToCMSpage1 = 'https://vistar-capture.s3.cern.ch/cms.png'
pngnameLHC = "lhc1.png"
pngnameCMS = "cms.png"

def DownloadLHCpage1():
  command = "wget -q " + pathToLHCpage1 + " > /dev/null"
  os.system(command)

def DownloadCMSpage1():
  command = "wget -q " + pathToCMSpage1 + " > /dev/null"
  os.system(command)

def DownloadPages():
  if os.path.isfile(pngnameCMS): os.system('rm %s'%pngnameCMS)
  if os.path.isfile(pngnameLHC): os.system('rm %s'%pngnameLHC)
  DownloadLHCpage1()
  DownloadCMSpage1()


def GetTimeNow():
  return datetime.now()

def GetTimestamp():
  return GetTimeNow().strftime("%d-%b-%Y (%H:%M:%S.%f)")

def GetNumberString(num):
  s = ''
  for c in num:
    if (not c.isdigit()) and (c!= '.'): continue
    else: s+=c
  return s

def GetLumiString(lumi):
  l = ''
  lumi = lumi.replace(' ', '')
  for c in lumi:
    if c.isdigit(): l += c
    else: break
  if   'ub' in lumi: l += ' /ub'
  elif 'nb' in lumi: l += ' /nb'
  elif 'pb' in lumi: l += ' /pb'
  elif 'fb' in lumi: l += ' /fb'
  return l

def GetRateString(rate):
  r = ''
  rate = rate.replace(' ', '')
  for c in rate:
    if c.isdigit(): r+=c
    else: break
  if   'khz' in rate.lower(): r += ' kHz'
  elif  'hz' in rate.lower(): r += ' Hz'
  return r

def GetDTstatus(s):
  if  'NOT' in s:  s = 'NOT ON'
  elif 'ON' in s: s = 'ON'
  return s

def GetDAQstatus(s):
  return s

def GetHelp():
  ''' Returns help for telegram users '''
  msg  = "Here you have a list of commands...\n"
  msg += " > cms - Get the CMS page1 pic\n"
  msg += " > lhc - Get the LHC page1 pic\n"
  msg += " > run [run number] - Get info of the current or given run\n"
  msg += " > fill [run number] - Get info of the current or given fill\n"
  return msg

