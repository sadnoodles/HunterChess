# -*- coding: utf-8 -*-
import os
def numberName(dir,start,ext):
    '''dir: dirpath 文件夹
       start: start number 起始数字
       ext: ext 后缀
       return a filepath <type string> named by continual number.
       返回一个以连续数字命名的路径'''
    if ext and ext[0]!='.':
        ext='.'+ext
    while os.path.exists(os.path.join(dir,"%s%s"%(start,ext))):
        start+=1
    return os.path.join(dir,"%s%s"%(start,ext))