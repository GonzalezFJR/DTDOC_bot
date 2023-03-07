import telepot
from Functions import *
from TelegramIDs import TelegramIDs
import json


class TelegramDTDOC:
  '''
    Class to interact with the telegram bot and provide DT info
  '''

  def __init__(self, bot_address):
    self.SetupBot(bot_address)
    self.TID = TelegramIDs()
    self.links = json.load(open('DTLinks.json', 'r'))
    self.linkcommands = [str(x).lower().replace(' ', '') for x in self.links.keys()]
    self.dictkeyslinks = {}
    for k in self.links.keys():
      self.dictkeyslinks[k.lower().replace(' ', '')] = k

  def handle(self, msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower().replace(' ', '')
    print ('[BOT] Got command: %s, id = %s' %(command, chat_id))
  
    # Commands

    if command in self.linkcommands:
      self.bot.sendMessage(chat_id, self.links[self.dictkeyslinks[command]]['link'])

    elif command.lower() in ["notifications on", "notificationson"]:
      self.TID.ActivateNotif(chat_id, True)
      self.bot.sendMessage(chat_id, "Ok, activating notifications.")
    elif command.lower() in ["notifications off", "notificationsoff"]:
      self.TID.ActivateNotif(chat_id, False)
      self.bot.sendMessage(chat_id, "Ok, deactivating notifications.")
    elif command == '/start' or command == 'start':
      name = self.bot.getChat(chat_id)['first_name']
      msg  = 'Hi %s, welcome to the DTDOC bot!! Write "help" to get a list of commands.'%name
      msg2 = 'If you want to activate/deactivate notifications, write "notifications on/off. Enjoy!'
      self.bot.sendMessage(chat_id, msg)
      self.bot.sendMessage(chat_id, msg2)
      print('%s started!'%name)
      if not str(chat_id) in self.TID.GetIdList():
        self.TID.AddId(chat_id, name)
        self.TID.ActivateNotif(chat_id, False)

    elif command.lower() == 'test':
      self.bot.sendMessage(chat_id, "Testing... ok!")
    elif command in ['link', 'links']:
      self.bot.sendMessage(chat_id, "This is a list of the links I know (tell me the name between brackets to get the link):")
      for l in self.links:
        self.bot.sendMessage(chat_id, '[%s]: %s'%(l, self.links[l]['desc']))
    elif command.lower() == 'cms':
      if not os.path.isfile(pngnameCMS):
        DownloadCMSpage1()
      self.bot.sendPhoto(chat_id, open(pngnameCMS,'rb'))
    elif command.lower() == 'lhc':
      if not os.path.isfile('lhc1.png'):
        DownloadLHCpage1()
      self.bot.sendPhoto(chat_id, open(pngnameLHC,'rb'))
    elif command.lower() == 'daq':
      if not os.path.isfile('DAQstatusGre.jpg'):
        DownloadDAQpage()
      self.bot.sendPhoto(chat_id, open(pngnameDAQ,'rb'))

    elif command.lower().startswith('help'):
      self.bot.sendMessage(chat_id, GetHelp())

  def SetupBot(self, bot_address):
    ''' Create the bot that will receive commands '''
    self.bot = telepot.Bot(bot_address)
    self.bot.message_loop(self.handle)
    print('[BOT] I am listening...')

  def SendTelegramAll(self, msg, IDs=None, force=False):
    ''' Send a message to everyone '''
    if IDs is None: IDs = self.TID.GetIdList()
    if isinstance(msg, list):
      for m in msg: self.SendTelegramAll(m, IDs, force)
      return
    print(msg)
    for chat_id in IDs:
      if force or self.TID.CheckNotif(chat_id):
        self.bot.sendMessage(chat_id, msg)

  def SendTelegramPhotoAll(self, imgname, IDs=None, force=False):
    if IDs is None: IDs = self.TID.GetIdList()
    print('Sending pic: ', imgname)
    for chat_id in IDs:
      if force or self.TID.CheckNotif(chat_id):
        self.bot.sendPhoto(chat_id, open(imgname,'rb'))

  def UpdateCMSstatusRun(self):
    self.SendTelegramAll("Starting a new run (DAQ status changed):")
    self.SendTelegramPhotoAll("daq.png")
    os.system("mv run.png run_ref.png")
    os.system("mv dt_daq.png dt_daq_ref.png")

  def UpdateCMSstatusNoRun(self):
    self.SendTelegramAll("Run ended!")
    os.system("mv run.png run_ref.png")
    os.system("mv dt_daq.png dt_daq_ref.png")
  
  def UpdateFill(self):
    self.SendTelegramAll("New fill:")
    self.SendTelegramPhotoAll("fill.png")
    os.system("mv fill.png fill_ref.png")

  def UpdateCMScomments(self):
    self.SendTelegramAll("New page1 report: ")
    self.SendTelegramPhotoAll("comments.png")
    os.system("mv comments.png comments_ref.png")
