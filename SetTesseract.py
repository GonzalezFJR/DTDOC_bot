import os, cv2
import pytesseract
import numpy as np
from Functions import *

class ImgReader:
  def __init__(self, path=None):
    self.SetPath(path)

  def SetPath(self, path=None):
    if path is None: path = os.popen("which tesseract").read().replace('\n', '').replace(' ', '')
    self.path = path
    pytesseract.pytesseract.tesseract_cmd = self.path

  def GetTxtFromImage(self, image):
    ''' Use tessetact to get text from an image '''
    return pytesseract.image_to_string(cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY), lang ='eng').replace('\n', '')

  def LoadImgStatusAndCommentsLHC(self, pngname):
    ''' Process LHC page1 image and returns text values '''
    img = cv2.imread(pngname)
    img_LHCstatus = img[40:90, :]
    img_comments  = img[585:-30, 10:510]
    LHCstatus = self.GetTxtFromImage(img_LHCstatus)
    LHCcomments = self.GetTxtFromImage(img_comments)
    return LHCstatus, LHCcomments
  
  def LoadInfoCMS(self, pngname):
    ''' Process CMS page1 image and returns text values '''
    img = cv2.imread(pngname)
    fill         = self.GetTxtFromImage(img[35:70, 540:630]).replace('\t', '').replace('\n', '').replace(' ', '')
    run          = self.GetTxtFromImage(img[35:70, 850:940]).replace('\t', '').replace('\n', '').replace(' ', '')
    lumi_del     = self.GetTxtFromImage(img[400:428, 250:440]).replace(' ', '')
    lumi_rec     = self.GetTxtFromImage(img[426:460, 274:439]).replace(' ', '')
    trigger_mode = self.GetTxtFromImage(img[400:428, 700:-5])
    rate_L1      = self.GetTxtFromImage(img[452:488, 760:-5])
    rate_HLT     = self.GetTxtFromImage(img[480:514, 760:-5])
    dt_daq       = self.GetTxtFromImage(img[700:725, 580:720])
    dt_dcs       = self.GetTxtFromImage(img[700:725, 700:800])
    fill = GetNumberString(fill)
    run  = GetNumberString(run)
    if not fill.isdigit(): fill = None
    if not  run.isdigit(): run  = None
    lumi_del = GetLumiString(lumi_del)
    lumi_rec = GetLumiString(lumi_rec)
    rate_L1  = GetRateString(rate_L1)
    rate_HLT = GetRateString(rate_HLT)
    dt_daq   = GetDAQstatus(dt_daq)
    dt_dcs   = GetDTstatus(dt_dcs)
    return fill, run, lumi_del, lumi_rec, trigger_mode, rate_L1, rate_HLT, dt_daq, dt_dcs
  
  
 
