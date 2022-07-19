import os, time
commandCheckLinks = lambda n : "tail %s -n %i"%(pathLogLinks, n)

class CheckLinks:

  ''' 
      This class will check links in a given file (by default log.txt) that has to be updated periodically
      This can be done through a tail command inside a screen session started as:
        ssh user@lxplus.cern.ch | tee log.txt
  '''

  def __init__(self, path='log.txt'):
    self.nLinkErrors = 0
    self.isFile = os.path.isfile(path)
  
  def GetLogLinks(self, n=6):
    out = os.popen( commandCheckLinks(n) ).readlines()
    return out

  def CheckLinksFromFile(self):
    ''' Check if there are link errors '''
    if not self.isFile: return 0
    # XXX Todo: avoid very large log files
    out = self.GetLogLinks()
    ok = True
    for l in out:
      pieces = l.replace('\n', '').replace('\t', ' ')
      while('  ') in pieces: pieces = pieces.replace('  ', ' ')
      pieces = pieces.replace('\x1b[0m', '')
      pieces = pieces.split(' ')[2:]
      for p in pieces:
        if p == '': continue
        if p != "0/0.00E+00": ok = False
    if not ok:
      print('[ERROR with slice test links] Number of errors: ', nErrors)
      self.nErrors += 1
      if self.nErrors >= 10:
        print('\n', out, '\n')
    return self.nErrors

  def GetNerrors(self):
    return self.nErrors

  def ResetNerrors(self):
    self.nErrors = 0

if __name__ == '__main__':
  pass
