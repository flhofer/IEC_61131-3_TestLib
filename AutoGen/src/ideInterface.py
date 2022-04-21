import dde_client as ddec
import os
import subprocess
import colorama

class IDEConnect():

    _stick= ['|', '/', '-', '\\']
    
    def __init__(self):
        colorama.init()
        self._pollLines = 0
        self._pollPos = 0
        pass
    
    def connect(self):
        pass
    
    def poll(self):
        pass
    
class CoDeSysConnect(IDEConnect):
    ''' Codesys Connector class '''
    
    #TODO: settings?
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
        
        self._ideProc = subprocess.Popen([self.mainPath + '\\' + self.mainEx, '/cmd', path + '\\runtest.cmd', self._prgFile] )

    def connect(self):
        ''' Connect to IDE and announce symbols '''

        #TODO: handling of DDE Timeout
        self._client = ddec.DDEClient(self.mainEx, os.path.abspath(self._prgFile))
        
        self._symbols = []

        for i in range(1, 63, 1):
            try:
                self._symbols.append('.testLogP^[' + str(i) + ']')
            except:
                #TODO: handling of callback exception
                pass
                                 
        for i in self._symbols:
            self._client.advise(i)
        
    def poll(self):
        ''' Poll the symbols in list '''
        for _ in range(0, self._pollLines):
            print ('\033[A', end = '' )
        self._pollLines = 0
        for i, item in enumerate(self._symbols):
            try:
                currentVal = self._client.request(item)
                if len(currentVal) <= 6:
                    self._pollLines = i
                    break
                print (currentVal)
            except:
                self._pollLines = i
                break
        print(self._stick[self._pollPos] + ' .. update every second\r', end='')
        self._pollPos = (self._pollPos + 1) % 4
    
    def waitIde(self):
        ''' wait for the IDE to be closed '''
        
        print('Waiting for the IDE to stop. (please close it, if not already done so)')
        self._ideProc.wait()
        