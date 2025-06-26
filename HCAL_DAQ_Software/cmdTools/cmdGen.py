#!/usr/bin/python


# 生成器类定义

class generator:

    def __init__(self,path='./CMDLib/default.dat'):
        self.path = path
        self.fHandle = open(path,'w+')
        self.log = open('./CMDLib/generatorLog.txt','w+')
        self.bytenum = 0

    def logclose(self):
        self.log.close()

    def fOpen(self):       
        self.fHandle = open(self.path,'w+')
        self.log.write('\n#### file open #### \n')

    def fClose(self):
        self.fHandle.close()
        self.bytenum = 0
        self.log.write('\n#### file close and clear #### \n')

    def fClear(self):
        self.fHandle.seek(0)
        self.fHandle.truncate()
        self.bytenum = 0
        self.log.write('\n#### file clear #### \n')


    def CommandSend(self,cmdWord):
        highByte = cmdWord >> 8
        lowByte = cmdWord & 0xff
        if(self.bytenum>20):
            self.fHandle.write('\n')
            self.log.write('\n')
            self.bytenum = 0
        cmdStr = "0x{:02x} 0x{:02x} ".format(highByte,lowByte)
        self.bytenum += 2
        self.fHandle.write(cmdStr)
        self.log.write(cmdStr)

    def write(self, str):
        self.bytenum = 0
        self.fHandle.write('\n'+str+'\n')
        self.log.write(str)
        

    def delay(self,time): #毫秒为单位
        cmdStr = '\n'+'#Delay'+str(time)+'\n'
        self.bytenum = 0
        self.fHandle.write(cmdStr)
        self.log.write(cmdStr)

class probeMod:
    
    def __init__(self):
        self.chn = 0
        self.chiplen = 992
        self.length = self.chiplen*9
        self.cfgData = ['0']*self.length

    def setChn(self,chn,chipSel): #chipSel != 0 specific chip set; chipSel = 0 all chips set
        if(chipSel == 0):
            for chipId in range(9):
                # 先将所有DAC Probe通道关闭
                self.cfgData[chipId*self.chiplen+6:chipId*self.chiplen+42] = '0'*(42-6)
                # 选通指定通道
                self.cfgData[chipId*self.chiplen+6+chn] = '1'
        else:
            for chipId in range(9):
                # 先将所有DAC Probe通道关闭
                self.cfgData[chipId*self.chiplen+6:chipId*self.chiplen+42] = '0'*(42-6)
            #选择指定芯片的指定通道
            self.cfgData[(chipSel-1)*self.chiplen+6+chn] = '1'
    def closeChn(self):
        for chipId in range(9):
            self.cfgData[chipId*self.chiplen+6:chipId*self.chiplen+42] = '0'*(42-6)

    def formatOutput(self,format = 'byte'):
        cfgStr = ''.join(self.cfgData)
        # 倒序输出
        cfgStrMsbf = cfgStr[::-1] 
        if(format == 'byte'):  # 输出每8bit的数据,由于长度是8的整倍数，没有做补零处理
            cfgByte = [0]*(len(cfgStrMsbf)//8)
            print("Length of cfgByte: "+str(len(cfgByte)))
            print("Length of cfgStrMsbf: "+str(len(cfgStrMsbf)))
            for i in range(0,len(cfgStrMsbf),8):
                cfgByte[i//8] = int(cfgStrMsbf[i:i+8],2)
                #print("i//8: "+str(i//8))
                #print("i: "+str(i))
        return cfgByte
        





