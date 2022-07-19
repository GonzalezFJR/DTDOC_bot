from Functions import *

### Get info from LHC and CMS
#################################################################################
class RunInfo:
  ''' Class to store info about fills and runs '''
  def __init__(self):
    self.fill = 0
    self.run = 0
    self.status = ''
    self.comments = ''
    self.DTstatus = 0
    self.DTrun = 0
    self.isON = False
    self.dic = {}

  def Get(self, name):
    if name == 'fill': return self.fill
    if name == 'run': return self.run
    if name == 'status': return self.status
    if name == 'comments': return self.comments
    if name == 'DTstatus': return self.DTstatus
    if name == 'DTrun': return self.DTrun
    if name == 'isON': return self.isON
    print("[Get error] not found: ", name)
    return None

  def Set(self, name, val):
    if name == 'fill': self.fill = val
    if name == 'run': self.run = val
    if name == 'status': self.status = val
    if name == 'comments': self.comments = val
    if name == 'DTstatus': self.DTstatus = val
    if name == 'DTrun': self.DTrun = val
    if name == 'isON': self.ON = val

  def AddFill(self, fill):
    if fill in list(self.dic.keys()): return
    self.dic[fill] = {}
  
  def AddRun(self, run, fill=None):
    if fill==None: fill = self.fill
    if run in list(self.dic[fill].keys()): return
    self.dic[fill][run] = {}

  def SetProp(self, name, prop, fill=None, run=None):
    if fill is None: fill = self.fill
    if  run is None:  run = self.run
    self.dic[fill][run][name] = prop

  def GetProp(self, name, fill=None, run=None):
    if fill is None: fill = self.fill
    if  run is None:  run = self.run
    return self.dic[fill][run][name]

  def HasProp(self, name, fill=None, run=None):
    if fill is None: fill = self.fill
    if  run is None:  run = self.run
    return (name in self.dic[fill][run].keys())

  def GetDict(self, fill=None, run=None):
    if fill is None: fill = self.fill
    if  run is None:  run = self.run
    return self.dic[fill][run].copy()

  def GetListOfRuns(self, fill=None):
    if fill is None: fill = self.fill
    return list(self.dic[fill].keys())
    
  def GetRunSummary(self, fill=None, run=None):
    d = self.GetDict(fill, run)
    if fill is None: fill = self.Get('fill')
    msg  = ">> Run summary [%s] << \n"%(run)
    msg += " > Fill %s \n > Duration = %s\n"%(fill, (str(d['time_end']-d['time_start'])) if 'time_end' in d.keys() else str(GetTimeNow() - d['time_start']) )
    msg += " > Delivered lumi = %s \n > Recorded lumi = %s\n"%(d['lumi_del'], d['lumi_rec'])
    msg += " > DT status: %s \n > DT DAQ: %s\n"%(d['DTdcs'], d['DTdaq'])
    msg += " > L1 rate: %s \n > HLT rate: %s\n > Trigger mode: %s\n"%(d['L1rate'], d['HLTrate'], d['trigger'])
    return msg
  
  def GetFillSummary(self, fill=None):
    msg = "### FILL SUMMARY [%s] ###\n\n"%(fill)
    if fill is None: fill = self.Get('fill')
    for r in self.GetListOfRuns(fill):
      if r == 0: continue
      msg += self.GetRunSummary(fill, r) + '\n'
    return msg
 
