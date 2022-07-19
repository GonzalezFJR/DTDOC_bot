import os, json

class TelegramIDs:
  def __init__(self, path='.telegram_id.json'):
    self.SetPath(path)
    self.LoadFile()

  def SetPath(self, path):
    self.path = path
    if not os.path.isfile(self.path):
      print('Creating IDs json file: ', self.path)
      os.system('echo "{}" > %s'%self.path)

  def LoadFile(self):
    with open(self.path, 'r') as f:
      idd = json.load(f)
      self.id = idd
      self.id_list = list(idd.keys())

  def AddId(self, new_id, name=None):
    self.id[new_id] = {'name':name}
    self.id_list = list(self.id.keys())
    print("New ID added: ", new_id + ' ' if name is None else ' with name %s'%name)
    self.UpdateFile()

  def UpdateFile(self):
    with open(self.path, 'w') as f:
      json.dump(self.id, f)

  def AddField(self, idn, field, value=True):
    if not idn in id_list:
      print('ERROR: id %s not found...'%str(idn))
      return
    self.id[idn][field] = value
    self.UpdateFile()

  def GetIdList(self, permdict=[]):
    if isinstance(permdict, str) and ',' in permdict: permdict = permdict.replace(' ', '').split(',')
    elif isinstance(permdict, str): permdict = [permdict]
    l = []
    for i in self.id_list:
      add = True
      for p in permdict:
        if not p in self.id[i]: add = False
        if not self.id[i]: add = False
      if add: l.append(i)
    return l
      
