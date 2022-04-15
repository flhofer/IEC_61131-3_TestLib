import dde_client as ddec
import time


class IDEConnect():

    def __init__(self):
        pass
    
    def connect(self):
        pass
    
    def poll(self):
        pass
    
class CoDeSysConnect(IDEConnect):
    ''' Codesys Connector class '''
    
    mainEx = 'M-PLC'

    def __init__(self, prgFile='Sample1.pro'):
        ''' Setup main '''
        self._prgFile = prgFile
        super.__init__()
        
    def connect(self):
        ''' Connect to IDE and announce symbols '''
        self._client = ddec.DDEClient(self.mainEx, self._prgFile)
        
        self._symbols = ['.testLogP^[0]']
        for i in self._symbols:
            self._client.advise(i)
        
    def pollDDE(self):
        ''' Poll the symbols in list '''
        for item in self._symbols:
            currentVal = self._client.request(item).split()
            print (currentVal[0])

        return currentVal
    
    