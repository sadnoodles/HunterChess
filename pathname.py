# -*- coding: utf-8 -*-
import os
def numberName(dir,start,ext):
    '''dir: dirpath �ļ���
       start: start number ��ʼ����
       ext: ext ��׺
       return a filepath <type string> named by continual number.
       ����һ������������������·��'''
    if ext and ext[0]!='.':
        ext='.'+ext
    while os.path.exists(os.path.join(dir,"%s%s"%(start,ext))):
        start+=1
    return os.path.join(dir,"%s%s"%(start,ext))