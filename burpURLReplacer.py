'''
Created on 2017-03-06
https://support.portswigger.net/customer/portal/questions/16700529-automatically-modifying-request-parameters

BurpUrlReplacer
@author: @tandhy
@version: 0.1
@summary: a Burp Suite extension to modify Request's URL, including parameter and its values.
          to check the modified request, chain the second instance of Burp as upstream proxy  from the first instance

@todo: use array for parameter_to_replace
@todo: replace strings
@todo: create UI
@todo: dynamic addition 

'''
from burp import IBurpExtender
from burp import IHttpListener
 
from java.net import URL
 
import re
import unicodedata
from datetime import datetime
from java.io import PrintWriter

class BurpExtender(IBurpExtender, IHttpListener):
    # definitions
    EXTENSION_NAME = "burpURLReplacer"
    AUTHOR = "@tandhy"
    HOST_NAME = 'localhost'
    PARAMETER_TO_REPLACE = 'sessionId'
    NEW_PARAMETER = ''
    # to replace an existing string
    VALUE_TO_REPLACE = 'xxx'
    # the new value
    NEW_VALUE = 'aaa'

    def registerExtenderCallbacks(self, callbacks):
        # keep a reference to our callbacks object
        self._callbacks = callbacks

        # obtain an extension helpers object
        self._helpers = callbacks.getHelpers()

        # define stdout writer
        self._stdout = PrintWriter(callbacks.getStdout(), True)

        print(self.EXTENSION_NAME + ' by ' + self.AUTHOR)
        print('================================')
        print('This extension will modify parameters and the values in Requests\' URL.')
        print('For help or any information see the github page.')

        # set the extension name
        callbacks.setExtensionName( self.EXTENSION_NAME )

        # register as an HTTP Listener
        callbacks.registerHttpListener( self )
        return
 
    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo ):
        # only process requests
        if messageIsRequest:

            # only process request if the request's host matches HOST_NAME
            if ( BurpExtender.HOST_NAME in self._helpers.analyzeRequest( messageInfo ).getUrl().toString() ): 

                # get the HTTP service for the request
                requestInfo = self._helpers.analyzeRequest( messageInfo )
                
                #needs to be a string before parsing it with urlparse
                completeURL = requestInfo.getUrl().toString()
                #print completeURL
                
                newParameters = []

                # get the parameters
                params = requestInfo.getParameters()
                for _params in params:
                    if ( _params.getName() == BurpExtender.PARAMETER_TO_REPLACE ):
                        print _params.getName(), _params.getValue(), _params.getType()
                        # create a new parameter and assign it with the NEW_VALUE
                        newParameter = self._helpers.buildParameter( BurpExtender.PARAMETER_TO_REPLACE , BurpExtender.NEW_VALUE , _params.getType() )
                        newParameters.append( newParameter )
                
                #bodyBytes = messageInfo.getRequest()[requestInfo.getBodyOffset():]
                #bodyStr = self._helpers.bytesToString(bodyBytes)

                # update the current request with the new parameter
                for _newParameters in newParameters:
                    #print _newParameters
                    messageInfo.setRequest( self._helpers.updateParameter( messageInfo.getRequest() , _newParameters ) )

                # uncomment the following to check the updated parameters
                #for param in self._helpers.analyzeRequest(messageInfo).getParameters():
                    #print param.getName(), " is now ", param.getValue()
            
        return

'''class UrlData():

    def __init__( self , url , domain , netloc , directories , params , filename , fileExt , baseURL , completeURL , path , responseData , logger ):
        self._url = url
        self._domain = domain
        self._netloc = netloc
        self._directories = directories
        self._params = params
        self._fileExt = fileExt
        self._baseURL = baseURL
        self._completeURL = completeURL
        self._responseData = responseData
        self._logger = logger
        self._path = path
        self._filename = filename

        self._logger.debug("UrlData object created")
        return

    def getPath(self):
        return self._path

    def getFilename(self):
        return self._filename

    def getResponseHeaders(self):
        if not self._url:
            return self._domain

    def getResponseData(self):
        return self._responseData

    def getBaseUrl(self):
        return self._baseURL

    def getCompleteURL(self):
        return self._completeURL

    def getUrl(self):
        return self._url

    def getDomain(self):
        return self._domain

    def getNetloc(self):
        return self._netloc

    def getDirectories(self):
        return self._directories

    def getLastDirectory(self):
        if len(self._directories) > 0:
            return self._directories[len(self._directories)-1]
        else:
            return ""

    def getParams(self):
        return self._params

    def getFileExt(self):
        return self._fileExt
'--------------------------------------------------------------------'
'''