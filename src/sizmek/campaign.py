'''
Created on 30 Jul 2015

@author: bernie.kim
'''

from utils.soap import Soap
from datetime import datetime, timedelta

class Campaign:
    '''
    classdocs
    '''


    def __init__(self, _id, accId, advId, start, end, actualStart, timeZoneId):
        '''
        Constructor
        '''
        self.id = _id
        self.accId = accId
        self.advId = advId
        self.start = start
        self.end = end
        self.actualStart = actualStart
        self.timeZoneId = timeZoneId
        self.addedDate = datetime.now().date()
    
    def __repr__(self):
        return "acc id: %s|adv id: %s|id: %s|start: %s|end: %s" % (self.accId, self.advId, self.id, self.start.date(), self.end.date())
    
    def __str__(self):
        return "acc id: %s|adv id: %s|id: %s|start: %s|end: %s" % (self.accId, self.advId, self.id, self.start.date(), self.end.date())
    
    def __len__(self):
        return 1
    
    @staticmethod
    def GetItemRes(wurl, auth, pageIndex, pageSize, filterRecent=True, _id=None, showExtInfo=True):
        client = Soap.SetupClient(wurl, auth, toAddToken=True, toImportMsgSrc=True, toImportArrSrc=False)
        # update paging info
        paging = client.factory.create('ns1:ListPaging')
        paging['PageIndex'] = pageIndex
        paging['PageSize'] = pageSize
        # update filter
        if filterRecent:
            # update filter array - isRecent = True
            objFilter = client.factory.create('ns0:CampaignRecentFilter')
            objFilter['IsRecent'] = filterRecent
        else:
            if _id is not None:
                # update campaign id
                objFilter = client.factory.create('ns0:CampaignIDFilter')
                objFilter['CampaignID'] = _id
            else:
                return (0, 'Campaign id is missing')
        filterArray = client.factory.create('ns0:ArrayOfCampaignServiceFilter')
        filterArray.CampaignServiceFilter = [objFilter]
        # get campaign response
        response = client.service.GetCampaigns(filterArray, paging, showExtInfo)        
        return response
    
    @staticmethod
    def GetItem(response):
        objList = []
        for r in response[1]['Campaigns']['CampaignInfo']:
            dt = r['CampaignExtendedInfo']['StartDate']
            start = datetime(dt['Year'], dt['Month'], dt['Day'], dt['Hour'], dt['Minute'], dt['Second'])
            timeZone = dt['TimeZoneID']
            dt = r['CampaignExtendedInfo']['EndDate']
            end = datetime(dt['Year'], dt['Month'], dt['Day'], dt['Hour'], dt['Minute'], dt['Second'])
            dt = r['CampaignExtendedInfo']['ActualStartDate']
            actualStart = datetime(dt['Year'], dt['Month'], dt['Day'], dt['Hour'], dt['Minute'], dt['Second']) if dt is not None else None
            obj = Campaign(r['ID'], r['AgencyID'], r['AdvertiserID'], start, end, actualStart, timeZone)
            objList.append(obj)
        return objList
    
    @staticmethod
    def GetItemPgn(wurl, auth, pageIndex, pageSize, filterRecent=True, _id=None, showExtInfo=True):
        objList = []
        cond = True
        while cond:
            response = Campaign.GetItemRes(wurl, auth, pageIndex, pageSize, filterRecent, _id, showExtInfo)
            objList = objList + Campaign.GetItem(response)
            Soap.ShowProgress(response[1]['TotalCount'], len(objList), pageIndex, pageSize)
            if len(objList) < response[1]['TotalCount']:
                pageIndex += 1
            else:
                cond = False
        return objList
    
    @staticmethod
    def GetFilter(objList, breakDate):
        filteredList = [obj for obj in objList if obj.startDate.date() <= breakDate and obj.endDate.date() >= breakDate + timedelta(days=-1)]
        print "%s campaigns from %s to %s" % (len(filteredList), breakDate, breakDate + timedelta(days=-1))
        return filteredList
