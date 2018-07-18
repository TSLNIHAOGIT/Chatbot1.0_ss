import sys,os
sys.path.append('../Lib/')
from LOG import Logger

class Test:
    def __init__(self):
        self.log = Logger(self.__class__.__name__,level='INFO').logger
#         self.log.('init')
    def test1(self):
        self.log.info('test')
        
        
if __name__ == '__main__':
    t = Test()
    t.log.info("sss")
    t.test1()