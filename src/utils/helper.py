'''
Created on 31 Jul 2015

@author: bernie.kim
'''

import csv

class Helper:
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @staticmethod
    def PrintObjects(objs):
        if len(objs) is 1:
            print objs            
        else:
            for obj in objs:
                print obj
        print "No of objs: %s" % len(objs)
        
    @staticmethod
    def WriteCsv(objs, path, mode='wb'):
        if len(objs) is 1:
            dic = {k:v for k,v in objs.__dict__.items() if not (k.startswith('__') and (k.endswith('__')))}
            names = dic.keys()
            with open(path, mode) as fout:
                cout = csv.DictWriter(fout, names)
                cout.writeheader()
                cout.writerow(dic)
        else:
            dics = []
            for obj in objs:
                dic = {k:v for k,v in obj.__dict__.items() if not (k.startswith('__') and (k.endswith('__')))}
                dics.append(dic.copy())
            names = dics[0].keys()
            with open(path,mode) as fout:
                cout = csv.DictWriter(fout, names)
                cout.writeheader()
                cout.writerows(dics) 