import dde_client as ddec
import os

class IDEConnect():

    def __init__(self):
        pass
    
    def connect(self):
        pass
    
    def poll(self):
        pass
    
class CoDeSysConnect(IDEConnect):
    ''' Codesys Connector class '''
    
    mainPath = 'c:\\Bachmann\\M1sw\\mplc3'
    mainEx = 'M-PLC'

    def __init__(self, prgFile):
        ''' Setup main '''
        self._prgFile = prgFile
        super().__init__()

    def runTest(self, fileList):
        
        path = os.getcwd()
        with open('runTest.cmd', 'w', encoding='cp1252', newline='\r\n') as f:
            f.write('query off ok\n')
            f.write('project import ')
            files = ''
            for file in fileList:
                files += path + '\\' + file + ' ' 

            f.write(files + '\n')
            f.write('online login\n')
            f.write('online run\n')
        
        retVal = os.system(self.mainPath + '\\' + self.mainEx + ' /cmd ' + path + '\\runtest.cmd ' + self._prgFile )

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
    
    