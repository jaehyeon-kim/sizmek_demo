'''
Created on 31 Jul 2015

@author: bernie.kim
'''

from suds.client import Client
from suds.sax.element import Element
from suds.xsd.doctor import Import, ImportDoctor

class Soap:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
    @staticmethod
    def SetupClient(wurl, auth, toAddToken = True, toImportMsgSrc = True, toImportArrSrc = False):
        if toImportMsgSrc:
            # update WSDL (xsd)
            msgImport = Import('http://api.eyeblaster.com/message')
            if toImportArrSrc:
                arrImport = Import('http://schemas.microsoft.com/2003/10/Serialization/Arrays')
                doctor = ImportDoctor(msgImport, arrImport)
            else:            
                doctor = ImportDoctor(msgImport)
            client = Client(wurl, doctor = doctor, faults = False)
        else:
            client = Client(wurl, faults = False)
        
        if toAddToken:
            # update token into SOAP header
            header = ('ns1', 'http://api.eyeblaster.com/message')
            element = Element('UserSecurityToken', ns=header).setText(auth.token)
            client.set_options(soapheaders=element)
        return client
    
    @staticmethod
    def ShowProgress(total, current, pageIndex, pageSize):
        print "Total No: %s, Current No: %s, page index: %s, page size: %s" % (total, current, pageIndex, pageSize)

    