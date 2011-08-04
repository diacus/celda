'''
Created on 08/06/2011

@author: diacus
'''

import logging
from lib.common import Messages

class ProxyLogger:
    '''
    classdocs
    '''

    __state = {
    	'_messages' = {
    		Messages.SAVE_STREAM = "Saving stream %s for user %s with group %s"
    	}
    }


    def __init__(self):
        '''
        Constructor
        '''

		self.__dict__ = self.__state
        
