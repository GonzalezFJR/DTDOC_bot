import telepot
from Functions import *
from SetTesseract import ImgReader
from RunInfo import RunInfo
from CheckLinks import CheckLinks
from TelegramIDs import TelegramIDs


class TelegramDTDOC:
  '''
    Class to interact with the telegram bot and provide DT info
  '''

  def __init__(self, bot_address):
    self.SetupBot(bot_address)
    self.imgread = ImgReader()
    self.runinfo = RunInfo()
    self.TID = TelegramIDs()

  def handle(self, msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower()
    print ('[BOT] Got command: %s' % command)
  
    if command in ['add', 'addme', 'add me']:
      name = self.bot.getChat(chat_id)['first_name']
      if str(chat_id) in self.TID.GetIdList():
        self.bot.sendMessage(chat_id, 'Hi %s. You are already in the list!'%name)
      else:
        self.bot.sendMessage(chat_id, "Ok, added to the bot. Your ID is: " + str(chat_id))
        self.TID.AddId(chat_id, name)
        self.bot.sendMessage(chat_id, "Welcome, %s."%name)
      self.bot.sendMessage(chat_id, GetHelp())
    elif command == 'test':
      self.bot.sendMessage(chat_id, "Testing... ok!")
    elif command == 'cms':
      self.bot.sendPhoto(chat_id, open("cms.png",'rb'))
    elif command == 'lhc':
      self.bot.sendPhoto(chat_id, open("lhc1.png",'rb'))
    elif command.startswith('run'):
      run_num = command[3:].replace(' ', '')
      if run_num == '': run_num = self.runinfo.Get('run')
      self.bot.sendMessage(chat_id, self.runinfo.GetRunSummary(run=run_num))
    elif command.startswith('fill'):
      fill_num = command[4:].replace(' ', '')
      if fill_num == '': fill_num = self.runinfo.Get('fill')
      self.bot.sendMessage(chat_id, self.runinfo.GetFillSummary(fill_num))
    elif command.startswith('help'):
      self.bot.sendMessage(chat_id, GetHelp())
    elif command == '/start' or command == 'start':
      msg = 'Welcome to the DTDOC bot!! Please, write "add me" if you would like to receive automatic notifications.'
      self.bot.sendMessage(chat_id, msg)
      name = self.bot.getChat(chat_id)['first_name']
      print('%s started!'%name)

  def SetupBot(self, bot_address):
    ''' Create the bot that will receive commands '''
    self.bot = telepot.Bot(bot_address)
    self.bot.message_loop(self.handle)
    print('[BOT] I am listening...')

  def SendTelegramAll(self, msg, IDs=None, send=True):
    ''' Send a message to everyone '''
    if IDs is None: IDs = self.TID.GetIdList()
    if isinstance(msg, list):
      for m in msg: self.SendTelegramAll(m, IDs, send)
      return
    for chat_id in IDs:
      print(msg)
      if send:
        self.bot.sendMessage(chat_id, msg)

  def GetInfoFromLHCandReport(self):
    ''' Gets fill mode and LHC comments and report if changes '''
    status = self.runinfo.Get('status')
    comments = self.runinfo.Get('comments')
    str_LHCstatus, str_comments = self.imgread.LoadImgStatusAndCommentsLHC(pngnameLHC)

    if str_LHCstatus != status:
      self.SendTelegramAll(str_LHCstatus, send=(status!=''))
      status = str_LHCstatus

    if str_comments != comments:
      self.SendTelegramAll(str_comments, send=(comments!=''))
      comments = str_comments

    self.runinfo.Set('status', status);
    self.runinfo.Set('comments', comments)
  
  def GetInfoFromCMSandUpdate(self):
    ''' Get info from CMS and update the runinfo object... and reports if there are changes '''
    fill = self.runinfo.Get('fill')
    run = self.runinfo.Get('run')
    DTstatus = self.runinfo.Get('DTstatus')
    DTrun = self.runinfo.Get('DTrun')
    isON = self.runinfo.Get('isON') 
    filln, runn, lumi_del, lumi_rec, trigger_mode, rate_L1, rate_HLT, dt_daq, dt_dcs = self.imgread.LoadInfoCMS(pngnameCMS)
    if filln is None: filln = fill
    if runn is None: runn = run

    if filln != fill:
      msg = "[INFO] Fill %s is over... \n"%fill
      msg += " >> Starting new FILL << \n"
      msg += "> Fill %s - starting time: %s \n"%(filln, GetTimestamp())
      msg += "> DT status = %s \n> DAQ status = %s"%(dt_dcs, dt_daq)
      self.SendTelegramAll(msg, send=(fill!=0))
      fill = filln
  
    elif runn != run:
      msg  = "[INFO] Run %s is over...\n"%(run)
      self.runinfo.SetProp('time_end', GetTimeNow(), fill, run)
      runsummart = self.runinfo.GetRunSummary(fill, run)
      self.SendTelegramAll(runsummart, send=isON)
      msg += "\n>> Starting new RUN << \n\n"
      msg += "> New run: %s \n> Starting time: %s\n"%(runn, GetTimestamp())
      msg += "> DT status = %s \n> DAQ status = %s"%(dt_dcs, dt_daq)
      self.SendTelegramAll(msg, send=(isON and (run!=0)))
      run = runn
  
    if (dt_dcs != DTstatus or dt_daq != DTrun) and (DTrun != 0 and DTstatus != 0):
      msg  = ">> DT STATUS CHANGE <<\n\n"
      msg += "> Previous DT status = %s\n> Previous DAQ status = %s\n"%(DTstatus, DTrun)
      msg += "> Time: %s\n"%(GetTimestamp())
      msg += "> DT status = %s \n> DAQ status = %s"%(dt_dcs, dt_daq)
      self.SendTelegramAll(msg, send=(DTstatus!='' and DTrun!=''))
      DTstatus = dt_dcs
      DTrun = dt_daq
      isON = (DTstatus == 'ON')
  
    # Update dict
    self.runinfo.AddFill(fill)
    self.runinfo.AddRun(run, fill)
    self.runinfo.SetProp('lumi_del', lumi_del, fill, run)
    self.runinfo.SetProp('lumi_rec', lumi_rec, fill, run)
    self.runinfo.SetProp('L1rate', rate_L1, fill, run)
    self.runinfo.SetProp('HLTrate', rate_HLT, fill, run)
    self.runinfo.SetProp('trigger', trigger_mode, fill, run)
    self.runinfo.SetProp('DTdaq', dt_daq, fill, run)
    self.runinfo.SetProp('DTdcs', dt_dcs, fill, run)
  
    self.runinfo.Set('fill', fill); 
    self.runinfo.Set('run', run); 
    self.runinfo.Set('DTstatus', DTstatus); 
    self.runinfo.Set('DTrun', DTrun); 
    self.runinfo.Set('isON', isON)
    if not self.runinfo.HasProp('time_start', fill, run): 
      self.runinfo.SetProp('time_start', GetTimeNow(), fill, run)

