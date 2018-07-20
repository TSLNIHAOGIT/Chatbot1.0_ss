
import logging
import os,sys



class Logger:
    def __init__(self, logger_name, level='INFO', pt=False):
        """
            
        Logger(self.__class__.__name__,level=ENV.NODE_LOG_LEVEL.value).logger
            
        """
        self.logger = logging.getLogger(logger_name)
        self.level= level
        self.logmapping ={'INFO': logging.INFO, 'DEBUG': logging.DEBUG}
        self.logLevel = self.logmapping[self.level.upper()]
        
        self.init_log(pt)
        
    def init_log(self, pt):
        fh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - CLASS:%(name)s- METHOD:%(funcName)s -LINE:%(lineno)d - MSG:%(message)s')
        if pt:
            sh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - P%(process)d - T%(thread)d - %(name)s- %(funcName)s -%(lineno)d- \t%(message)s')
        else:
            sh_formatter = logging.Formatter('%(asctime)s - %(levelname)s - CLASS:%(name)s- METHOD:%(funcName)s -LINE:%(lineno)d - MSG:%(message)s')

        self.logger.setLevel(self.logLevel)
        sh = logging.StreamHandler()
        sh.setFormatter(sh_formatter)
        self.logger.addHandler(sh)
        
        
        
        