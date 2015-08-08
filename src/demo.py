from utils.helper import Helper
from sizmek.authentication import Auth
from sizmek.advertiser import Advertiser, ConvTag
from sizmek.campaign import Campaign
import logging

logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.client').setLevel(logging.DEBUG)

## WSDL urls
authWSDL = 'https://platform.mediamind.com/Eyeblaster.MediaMind.API/V2/AuthenticationService.svc?wsdl'
advertiserWSDL = 'https://platform.mediamind.com/Eyeblaster.MediaMind.API/V2/AdvertiserService.svc?wsdl'
campaignWSDL = 'https://platform.mediamind.com/Eyeblaster.MediaMind.API/V2/CampaignService.svc?wsdl'

## credentials
username = 'user-name'
password = 'password'
appkey = 'application-key'

## path to export API responses
path = 'C:\\projects\\workspace\\sizmek_report\\src\\csvs\\'

## authentication
auth = Auth(username, password, appkey, authWSDL)

## get advertisers
advRes = Advertiser.GetItemRes(advertiserWSDL, auth, pageIndex=0, pageSize=50, showExtInfo=True)
advList = Advertiser.GetItem(advRes)
Helper.PrintObjects(advList)

# advListPgn = Advertiser.GetItemPgn(advertiserWSDL, auth, pageIndex=0, pageSize=50, showExtInfo=True)
# Helper.PrintObjects(advListPgn)

## get campaigns
# recent filter
camRes = Campaign.GetItemRes(campaignWSDL, auth, pageIndex=0, pageSize=50, filterRecent=True, _id=None, showExtInfo=True)
camList = Campaign.GetItem(camRes)
Helper.PrintObjects(camList)

# camListPgn = Campaign.GetItemPgn(campaignWSDL, auth, pageIndex=0, pageSize=50, filterRecent=True, _id=None, showExtInfo=True)
# Helper.PrintObjects(camListPgn)
# 
# Helper.WriteCsv(camList, path + 'camList.csv', 'wb')
# 
# filteredList = Campaign.GetFilter(camListPgn, datetime.now().date())
# Helper.PrintObjects(filteredList)
# 
# Helper.WriteCsv(camListPgn, path + 'camListPgn.csv', 'wb')















