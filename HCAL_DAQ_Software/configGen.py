import sys,os
import numpy as np
import time
from configList import regConfigList,regList,chipIDList,thrList

class fileHandle:
    def __init__(self,path,cfgFileName,dacVoltageList,chipIDList,thrList_3,fixInputDAC): #手动命名配置文件，mod:HT(TDC&Hg),HL(Hg&Lg)
        self.path = path
        self.log = open(path+'/dacGeneratorLog.txt','a')
        self.bytenum = 0
        self.dacVoltageList = dacVoltageList
        self.chipIDList = chipIDList
        self.thrList = thrList_3
        self.cfgFileName = cfgFileName
        self.fWrite = open(self.path + cfgFileName + '.txt','w+') #打开配置文件

    def logClose(self):
        self.log.close()

    def logClear(self):       
        #self.fRead = open(self.path+'dacAdjustNo.'+str(self.num)+'.txt','r')
        self.log.seek(0)
        self.log.truncate()
        self.log.write('\n#### log file clear #### \n')

    def logRecordTime(self):
        year = str(time.localtime().tm_year).zfill(4)
        mon = str(time.localtime().tm_mon).zfill(2)
        day = str(time.localtime().tm_mday).zfill(2)
        hour = str(time.localtime().tm_hour).zfill(2)
        minute = str(time.localtime().tm_min).zfill(2)
        self.log.write('\n#### cfg time is' + year+mon+day+' '+hour+':'+minute  + '#### \n')

    def logWrite(self,record):
        self.log.write(record)
    # def fClose(self):
    #     self.fRead.close()
    #     self.bytenum = 0
    #     self.log.write('\n#### file close #### \n')

    def fClear(self):
        self.fWrite.seek(0) #移动指针到文件头
        self.fWrite.truncate() #删除指针后的所有字符
        self.bytenum = 0
        self.log.write('\n#### file clear #### \n')

    #def dacRead(self,fixInputDAC,num): #得到210个DAC输出的二进制编码
    def dacRead(self,fixInputDAC,num): #得到210个DAC输出的二进制编码
        if(fixInputDAC == 0):
            self.fRead = open(self.path+'dacAdjustFiles/dacAdjustNo.'+str(num)+'.txt','r') #读取已有的dac差异性补偿文件
        else:
            self.fRead = open(self.path+'dacAdjustYZ/Vop0.5_dacAdjustNo.'+str(num)+'.txt','r') #读取已有的dac差异性补偿文件
        line = self.fRead.readline() #这里的fRead是在构造函数中被定义的
        while line: #当line非空继续读取
            if(fixInputDAC == 0):
                if (int((float(line[-9:-5])-4.5)/4*255) == 0):
                    self.dacVoltageList.append('000000001')
                else:
                    self.dacVoltageList.append(str(bin(int((4.5 - float(line[-9:-5]))/4*255)))[2:].zfill(8) + '1')
            #print(str(bin(255 - int((float(line[-9:-5])-0.5)/4*255)))[2:] + '1')
            else:
                locOfTab = line.find('\t')
                self.dacVoltageList.append(str(bin(int(line[locOfTab+1:-1])))[2:].zfill(8)+'1')
            line = self.fRead.readline()
        #for i in range(6): #chip6 的 chn30 - chn35 无用
            #self.dacVoltageList.append('000000000')
        self.fRead.close()

    def outputModSelect(self,outputMod,selectThr): #根据选择的mod决定输出 hg lg 或者 hg TDC
        self.outputMod = outputMod
        if self.outputMod == 'HL': #0 有效
            index = regList.index('Switch_TDC_On')
            regConfigList[index] = '1'
            index = regList.index('Auto_Gain')
            regConfigList[index] = '1'
            index = regList.index('Gain_Select')
            regConfigList[index] = '0'
        elif self.outputMod == 'HT':
            index = regList.index('Switch_TDC_On')
            regConfigList[index] = '0'
            index = regList.index('Auto_Gain')
            regConfigList[index] = '1'
            index = regList.index('Gain_Select')
            regConfigList[index] = '1'
        elif self.outputMod == 'AT':
            index = regList.index('Switch_TDC_On')
            regConfigList[index] = '0'
            index = regList.index('Auto_Gain')
            regConfigList[index] = '0'
            index = regList.index('Gain_Select')
            regConfigList[index] = '0'
            index = regList.index('DAC2_Gain_Sel')
            regConfigList[index] = str(bin(selectThr)[2::].zfill(10))
        else:
            self.log.write('\n#### outputMod should be HL,HT or AT #### \n')
            print('outputMod select error')
            sys.exit(1)
    
    # def thrSet(self,thr):
    #     self.thr = thr
    #     index = regList.index('DAC1_Trigger')
    #     regConfigList[index] = str(bin(self.thr)[2::].zfill(10)) #375 -> 0b0101110111

    def tdcRampSet(self,tdcRamp):
        self.tdcRamp = tdcRamp
        index = regList.index('TDC_Ramp_Slope')
        regConfigList[index] = str(self.tdcRamp)

    def trigDelaySet(self,trigDelay):
        self.trigDelay = trigDelay
        index = regList.index('Trigger_delay')
        regConfigList[index] = str(bin(int(trigDelay)))[2:].zfill(8)
        #print(regConfigList[index])    

    def cfgFileWrite(self,EBUNum,forceEn): #写入配置文件
        #self.cfgFileName = cfgFileName
        #self.fWrite = open(self.path + cfgFileName + '.txt','a')
        dacAllChips = ''.join(self.dacVoltageList) #顺序连接所有的inputdac码值

        dacSingleChip = [] #得到单芯片的inputdac list
        for i in range(9):
            dacSingleChip.append(dacAllChips[i * 324 : i * 324 + 324])
        
        regConfigAll = [] 
        for i in range(9): #生成9个芯片的寄存器值列表
            index = regList.index('Chip_ID')
            regConfigList[index] = chipIDList[i]
            index = regList.index('Input_DAC')
            regConfigList[index] = dacSingleChip[i]
            index = regList.index('DAC1_Trigger')
            if(forceEn==0):
                
                print(bin(thrList[(EBUNum - 1)*9 + i]).zfill(10))
                regConfigList[index] = str(bin(thrList[(EBUNum-1)*9 + i])[2::].zfill(10)) #375 -> 0b0101110111
            else:
                regConfigList[index] = str(bin(1023)[2::].zfill(10)) #375 -> 0b0101110111
            # for member in regConfigList:
            #     print(len(member))
            #print(regConfigList)
            regConfigAll.append(''.join(regConfigList))

        #for member in regConfigAll:
            #print(len(member)) 
        
        
        regConfigAll = ''.join(regConfigAll)
        regConfigAll = regConfigAll[::-1] #逆序
        #print(regConfigAll)
        #regConfigAll = regConfigAll + '0000'
        i = 0
        while i < len(regConfigAll):
            #print(hex(int(regConfigAll[i : i + 8],2)))
            tmpHexData = hex(int(regConfigAll[i : i + 8],2))
            if len(tmpHexData) < 4:
                tmpHexData = list(tmpHexData)
                tmpHexData.insert(2,'0')
                tmpHexData = ''.join(tmpHexData)
            self.fWrite.write(tmpHexData + ' ')
            i = i + 8
        
        self.fWrite.close() #关闭配置文件
