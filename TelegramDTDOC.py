import telepot
from Functions import *
from TelegramIDs import TelegramIDs


class TelegramDTDOC:
  '''
    Class to interact with the telegram bot and provide DT info
  '''

  def __init__(self, bot_address):
    self.SetupBot(bot_address)
    self.TID = TelegramIDs()

  def handle(self, msg):
    chat_id = msg['chat']['id']
    command = msg['text'].lower()
    print ('[BOT] Got command: %s, id = %s' %(command, chat_id))
  
    # Commands
    if command.lower() in ['add', 'addme', 'add me']:
      name = self.bot.getChat(chat_id)['first_name']
      if str(chat_id) in self.TID.GetIdList():
        self.bot.sendMessage(chat_id, 'Hi %s. You are already in the list!'%name)
      else:
        self.bot.sendMessage(chat_id, "Ok, added to the bot.")
        self.TID.AddId(chat_id, name)
        self.bot.sendMessage(chat_id, "Welcome, %s."%name)
      self.bot.sendMessage(chat_id, GetHelp())
    elif command.lower() in ["notifications on", "notificationson"]:
      self.TID.ActivateNotif(chat_id, True)
      self.bot.sendMessage(chat_id, "Ok, activating notifications.")
    elif command.lower() in ["notifications off", "notificationsoff"]:
      self.TID.ActivateNotif(chat_id, False)
      self.bot.sendMessage(chat_id, "Ok, deactivating notifications.")
    elif command == '/start' or command == 'start':
      name = self.bot.getChat(chat_id)['first_name']
      msg  = 'Hi %s, welcome to the DTDOC bot!! Please, write "add me" if you would like to receive automatic notifications. Write "help" to get a list of commands.'%name
      msg2 = 'If you want to activate/deactivate notifications, write "notifications on/off. Enjoy!'
      self.bot.sendMessage(chat_id, msg)
      self.bot.sendMessage(chat_id, msg2)
      print('%s started!'%name)
    elif command.lower() == 'test':
      self.bot.sendMessage(chat_id, "Testing... ok!")

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
    self.SendTelegramAll("DAQ status changed!")
    self.SendTelegramPhotoAll("daq.png")
    os.system("mv run.png run_ref.png")
    os.system("mv dt_daq.png dt_daq_ref.png")

  def UpdateCMSstatusNoRun(self):
    self.SendTelegramAll("Run ended! We are not taking data at the moment, I will notify you when we start again.")
    os.system("mv run.png run_ref.png")
    os.system("mv dt_daq.png dt_daq_ref.png")
  
  def UpdateFill(self):
    self.SendTelegramAll("Fill changed!")
    self.SendTelegramPhotoAll("fill.png")
    os.system("mv fill.png fill_ref.png")

  def UpdateCMScomments(self):
    self.SendTelegramAll("New page1 report: ")
    self.SendTelegramPhotoAll("comments.png")
    os.system("mv comments.png comments_ref.png")