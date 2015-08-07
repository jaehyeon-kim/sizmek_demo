'''
Created on 31 Jul 2015

@author: bernie.kim
'''

from utils.soap import Soap
from datetime import datetime

class Advertiser:
    '''
    classdocs
    '''


    def __init__(self, pid, name, vertical, useConv):
        '''
        Constructor
        '''
        self.id = pid
        self.name = name
        self.vertical = vertical
        self.useConv = useConv
        self.addedDate = datetime.now().date()
        
    def __repr__(self):
        return "id: %s|name: %s|use conv: %s" % (self.id, self.name, self.useConv)
    
    def __str__(self):
        return "id: %s|name: %s|use conv: %s" % (self.id, self.name, self.useConv)
    
    def __len__(self):
        return 1
    
    @staticmethod
    def GetItemRes(wurl, auth, pageIndex, pageSize, showExtInfo=True):
        client = Soap.SetupClient(wurl, auth, toAddToken=True, toImportMsgSrc=True, toImportArrSrc=False)
        # update paging info
        paging = client.factory.create('ns1:ListPaging')
        paging['PageIndex'] = pageIndex
        paging['PageSize'] = pageSize
        # update filter array - empty
        filterArrary = client.factory.create('ns0:ArrayOfAdvertiserServiceFilter')
        # get response
        response = client.service.GetAdvertisers(filterArrary, paging, showExtInfo)
        return response
    
    @staticmethod
    def GetItem(response):
        objList = []
        for r in response[1]['Advertisers']['AdvertiserInfo']:
            obj = Advertiser(r['ID'], r['AdvertiserName'], r['Vertical'], r['AdvertiserExtendedInfo']['UsesConversionTags'])
            objList.append(obj)
        return objList
    
    @staticmethod
    def GetItemPgn(wurl, auth, pageIndex, pageSize, showExtInfo=True):
        objList = []
        cond = True
        while cond:
            response = Advertiser.GetItemRes(wurl, auth, pageIndex, pageSize, showExtInfo)
            objList = objList + Advertiser.GetItem(response)
            Soap.ShowProgress(response[1]['TotalCount'], len(objList), pageIndex, pageSize)
            if len(objList) < response[1]['TotalCount']:
                pageIndex += 1
            else:
                cond = False
        return objList
            
    @staticmethod
    def GetFilter(objList):
        filteredList = [obj for obj in objList if obj.useConv == True]
        print "%s out of %s advertiser where useConv equals True" % (len(filteredList), len(objList))
        return filteredList

class ConvTag(object):
    '''
    classdocs
    '''


    def __init__(self, pid, name, advId, url, ptype, status, hasConv):
        '''
        Constructor
        '''
        
        self.id = pid
        self.name = name
        self.advId = advId
        self.url = url
        self.type = ptype
        self.status = status
        self.hasConv = hasConv
        self.addedDate = datetime.now().date()

    def __repr__(self):
        return "adv id: %s|id: %s|name: %s|status: %s|has conv: %s" % (self.advId, self.id, self.name, self.status, self.hasConv)
    
    def __str__(self):
        return "adv id: %s|id: %s|name: %s|status: %s|has conv: %s" % (self.advId, self.id, self.name, self.status, self.hasConv)
    
    def __len__(self):
        return 1
    
    @staticmethod
    def GetItemRes(wurl, auth, advId, pageIndex, pageSize, showExtInfo=True):
        client = Soap.SetupClient(wurl, auth, toAddToken=True, toImportMsgSrc=True, toImportArrSrc=True)
        # update paging info
        paging = client.factory.create('ns1:ListPaging')
        paging['PageIndex'] = pageIndex
        paging['PageSize'] = pageSize
        # update filter array - empty
        filterArrary = client.factory.create('ns0:ArrayOfConversionTagsFilter')
        # get response
        response = client.service.GetConversionTags(advId, filterArrary, paging, showExtInfo)
        return response
    
    @staticmethod
    def GetItem(response):
        objList = []
        for r in response[1]['ConversionTags']['ConversionTagInfo']:
            obj = ConvTag(r['ID'], r['ReportingName'], r['AdvertiserID'], r['AdvertiserPageURL'],
                          r['Type'], r['ConversionTagStatus'], r['ConversionTagExtendedInfo']['HasConversions'])
            objList.append(obj)        
        return objList
    
    @staticmethod
    def GetItemPgn(wurl, auth, advId, pageIndex, pageSize, showExtInfo=True):
        objList = []
        cond = True
        while cond:
            response = ConvTag.GetItemRes(wurl, auth, advId, pageIndex, pageSize, showExtInfo)
            objList = objList + ConvTag.GetItem(response)
            Soap.ShowProgress(response[1]['TotalCount'], len(objList), pageIndex, pageSize)
            if len(objList) < response[1]['TotalCount']:
                pageIndex += 1
            else:
                cond = False
        return objList
    
    @staticmethod
    def GetFilter(objList):
        filteredList = [obj for obj in objList if obj.hasConv == True]
        print "%s out of %s conversion tags where hasConv equals True" % (len(filteredList), len(objList))
        return filteredList
