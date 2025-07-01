# 用于HCAL原型机的上位机操作软件

import subprocess # 用于命令行执行
#import numpy as np # python 基本计算用数据结构及操作实现包
import sys,os
import tempfile 
from i2c_ustc2b import elink_config#,elink_encoding # elink_config 函数导入
from Driver.setting_ustc_2b import FEC_name_list3,FEC_name_list2,FEC_name_list1,FEC_name_list0,usedElinkList,cmdPath,cfgFileList,cfgPath
from time import sleep, localtime
import time
from cmdTools.cmdGen import generator, probeMod
from configList import regConfigList,regList,chipIDList,HVList,HBUOrderList,thrList, DIFOrderList, HVParaList
from configGen import fileHandle

def felixShellDo(felixCmd,silence=1):
    if(~silence):
        print("FELIX Command:\n"+felixCmd+"\n")
    p = subprocess.Popen([felixCmd], shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]
    if(~silence):
        print("Result INFO:\n"+str(grep_stdout)+"\n")


def FEC_dataInit(GBTList=[1,3]):
    # 可以批量执行 Elink Config GUI窗口的操作
    # 初始化为数据通道
    print('Data Link Configuration Started')
    for GBT in GBTList:
        for i in range(5): #遍历egroup
            for j in range(2): #对应th 和 fh
                if((j==0)&(i==4)): #egroup4 的上行测试通道关闭 
                    elink_config(0,GBT,i,j,0)
                    elink_config(0,GBT,i,j,1)
                    elink_config(0,GBT,i,j,2)
                    elink_config(0,GBT,i,j,3)
                    elink_config(0,GBT,i,j,4)
                    elink_config(0,GBT,i,j,5)
                    elink_config(0,GBT,i,j,6)
                    elink_config(1,GBT,i,j,7)
                    elink_config(1,GBT,i,j,8)
                    elink_config(0,GBT,i,j,9)
                    elink_config(0,GBT,i,j,10)
                    elink_config(0,GBT,i,j,11)
                    elink_config(0,GBT,i,j,12)
                    elink_config(0,GBT,i,j,12)
                    elink_config(0,GBT,i,j,14)
                elif((j==1)&(i==4)): #egroup4的下行通道040设置为4b
                    elink_config(0,GBT,i,j,0)
                    elink_config(0,GBT,i,j,1)
                    elink_config(0,GBT,i,j,2)
                    elink_config(0,GBT,i,j,3)
                    elink_config(1,GBT,i,j,4)
                    elink_config(0,GBT,i,j,5)
                    elink_config(0,GBT,i,j,6)
                    elink_config(1,GBT,i,j,7)
                    elink_config(1,GBT,i,j,8)
                    elink_config(0,GBT,i,j,9)
                    elink_config(0,GBT,i,j,10)
                    elink_config(0,GBT,i,j,11)
                    elink_config(0,GBT,i,j,12)
                    elink_config(0,GBT,i,j,13)
                    elink_config(0,GBT,i,j,14)
                else:
                    elink_config(0,GBT,i,j,0)
                    elink_config(0,GBT,i,j,1)
                    elink_config(0,GBT,i,j,2)
                    elink_config(0,GBT,i,j,3)
                    elink_config(0,GBT,i,j,4)
                    elink_config(0,GBT,i,j,5)
                    elink_config(0,GBT,i,j,6)
                    elink_config(1,GBT,i,j,7)
                    elink_config(1,GBT,i,j,8)
                    elink_config(1,GBT,i,j,9)
                    elink_config(1,GBT,i,j,10)
                    elink_config(1,GBT,i,j,11)
                    elink_config(1,GBT,i,j,12)
                    elink_config(1,GBT,i,j,13)
                    elink_config(1,GBT,i,j,14)
                   # elink_encoding(GBT,i,j,0,1)
                   # elink_encoding(GBT,i,j,1,1)
                   # elink_encoding(GBT,i,j,2,1)
                   # elink_encoding(GBT,i,j,3,1)
                   # elink_encoding(GBT,i,j,4,1)
                   # elink_encoding(GBT,i,j,5,1)
                   # elink_encoding(GBT,i,j,6,1)
                   # elink_encoding(GBT,i,j,7,1)
    print('Elink Configured')
    for elink in usedElinkList:
        cmd = 'fereverse -e '+ usedElinkList[elink] + ' set'
        felixShellDo(cmd)
    
    #反转命令通道和测试通道bit顺序
    if(3 in GBTList):
        cmd = 'fereverse -e 0E6 set'  
        felixShellDo(cmd)
    if(1 in GBTList):
        cmd = 'fereverse -e 040 set'
        felixShellDo(cmd)

def FEC_clockInit(GBTList = [0,2]):
    # 可以批量执行 Elink Config GUI窗口的时钟GBT Link操作
    # 初始化为时钟通道
    print('Clock Link Configuration Started')
    for GBT in GBTList:
        for i in range(5): #遍历egroup
            for j in range(2): #对应th 和 fh
                if((j==1)&(i==4)): #egroup4 的下行EPATH7打开 
                    elink_config(0,GBT,i,j,0)
                    elink_config(0,GBT,i,j,1)
                    elink_config(0,GBT,i,j,2)
                    elink_config(0,GBT,i,j,3)
                    elink_config(0,GBT,i,j,4)
                    elink_config(0,GBT,i,j,5)
                    elink_config(0,GBT,i,j,6)
                    elink_config(0,GBT,i,j,7)
                    elink_config(0,GBT,i,j,8)
                    elink_config(0,GBT,i,j,9)
                    elink_config(0,GBT,i,j,10)
                    elink_config(0,GBT,i,j,11)
                    elink_config(0,GBT,i,j,12)
                    elink_config(0,GBT,i,j,13)
                    elink_config(1,GBT,i,j,14)
                else:
                    elink_config(0,GBT,i,j,0)
                    elink_config(0,GBT,i,j,1)
                    elink_config(0,GBT,i,j,2)
                    elink_config(0,GBT,i,j,3)
                    elink_config(0,GBT,i,j,4)
                    elink_config(0,GBT,i,j,5)
                    elink_config(0,GBT,i,j,6)
                    elink_config(0,GBT,i,j,7)
                    elink_config(0,GBT,i,j,8)
                    elink_config(0,GBT,i,j,9)
                    elink_config(0,GBT,i,j,10)
                    elink_config(0,GBT,i,j,11)
                    elink_config(0,GBT,i,j,12)
                    elink_config(0,GBT,i,j,13)
                    elink_config(0,GBT,i,j,14)
    
    #反转命令通道和测试通道bit顺序
    if(2 in GBTList):
        cmd = 'fereverse -e 0A7 set'  
        felixShellDo(cmd)
    if(0 in GBTList):
        cmd = 'fereverse -e 027 set'
        felixShellDo(cmd)


def tempAcq(elinkNum = 2,cycle = 10,t=1):
    # 默认用3号GBT采数
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    for cycleCnt in range(cycle):
        print("Temperature Acquisition Cycle: {:d}".format(cycleCnt))
        for elink in enList:
            fupCmd = 'fupload -e '+ elink +" " + cmdPath + 'tempAcq.dat'
            felixShellDo(fupCmd)
        #等待t时间
        sleep(t)

    fupCmd = 'fdaq -X -T -t '+str(t)+' ./data/temperature/temp&'
    felixShellDo(fupCmd)

def normalAcq(elinkNum = 2, t=3):
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    for elink in enList:
        fupCmd = 'fupload -e ' + elink + ' ' + cmdPath + 'normalAcq.dat'
        felixShellDo(fupCmd)

    fupCmd = 'fdaq -X -t '+str(t)+' ./data/' +time.strftime("%Y_%m%d",time.localtime())+ '/oneshotAcq/data_&'
    felixShellDo(fupCmd)

    for elink in enList:
        fupCmd = 'fupload -e ' + elink + ' ' + cmdPath + 'stopAcq.dat'
        felixShellDo(fupCmd)

def sp2eConfig(elinkNum = 2, settingId=0):

    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    #fileName = './cfgFiles/'+ cfgFileList[settingId]
    fileName = './cfgFiles/'+ 'chipConfiguration'
    if(not os.path.exists(fileName+'.dat')):

        cfgFileHandle = open(fileName+'.txt')
        cfgDat = cfgFileHandle.read()
        cfgByte = filter(None,cfgDat.split(' '))
        gen = generator(fileName+'.dat')
        gen.CommandSend(0x0601)
        gen.CommandSend(0x0501)

        for byte in cfgByte:
            gen.CommandSend(0x0300+int(byte,16))

        gen.CommandSend(0x0500)
        gen.CommandSend(0x0800)

        gen.fClose()



    for elink in enList:  
        fupCmd = "fupload -e " + elink + " " + fileName+ '.dat'
        felixShellDo(fupCmd)
        sleep(0.5)

def realtimeEnable(elinkNum = 2, enable = 0b100):
    # 控制FPGA是否接收外触发, Valid使能与Eraze使能
    # 由高至低为 Trigger Enable, Valid Enable, Eraze Enable
    # 7为全使能
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum
    tmpFile = open(cmdPath + 'tmpCmd.dat','w+')
    cmdWordH = 0x0c
    cmdWordL = enable
    cmdWord = "0x{:02x} 0x{:02x} ".format(cmdWordH,cmdWordL)
    tmpFile.write(cmdWord)
    tmpFile.close()


    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd)

    

def internalSyncEnable(enable = 1, delay = 100):
    tmpFile = open(cmdPath + 'internalSyncConfig.dat','w+')
    cmdWordH = 0x19
    cmdWordL = (enable<<7) + min(delay,127)
    cmdWord = "0x{:02x} 0x{:02x} ".format(cmdWordH,cmdWordL)
    for i in range(40):
        layerId = "0x{:02x} 0x{:02x} ".format(0xFE,i)
        tmpFile.write(layerId)
        tmpFile.write(cmdWord)
        tmpFile.write("0xEE 0xEE ")
    tmpFile.close()

def elecCalibOpen(enable = 1, delay = 100):
    tmpFile = open(cfgPath + 'elecCalibOpen.dat','w+')
    cmdWordH = 0x19
    cmdWordL = (enable<<7) + min(delay,127)
    cmdWord = "0x{:02x} 0x{:02x} ".format(cmdWordH,cmdWordL)
    for i in range(40):
        layerId = "0x{:02x} 0x{:02x} ".format(0xFE,i)
        tmpFile.write(layerId)
        #tmpFile.write(cmdWord)
        tmpFile.write("0x12 0x55 ")#使能所有enable信号
        tmpFile.write("0xEE 0xEE ")
    tmpFile.close()   

def elecCalibClose(enable = 0, delay = 100):
    tmpFile = open(cfgPath + 'elecCalibClose.dat','w+')
    cmdWordH = 0x19
    cmdWordL = (enable<<7) + min(delay,127)
    cmdWord = "0x{:02x} 0x{:02x} ".format(cmdWordH,cmdWordL)
    for i in range(40):
        layerId = "0x{:02x} 0x{:02x} ".format(0xFE,i)
        tmpFile.write(layerId)
        tmpFile.write(cmdWord)
        tmpFile.write("0x12 0x14 ")#关闭所有enable信号
        tmpFile.write("0xEE 0xEE ")
    tmpFile.close()  

def elecCalib(elinkNum = 2, rg = list(range(50,400,50))+list(range(800,4096,400)),t=1):
    
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    fdaqCmd = "fdaq -X -T -t "+str(t)+" ./data/"+time.strftime("%Y_%m%d",time.localtime())+"/elecCalib/"+time.strftime("%H%M%S",time.localtime())+"/"
    # 写临时命令文件
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0x127f) # enable all chip, and make amplifier active. Accept external trigger

    # 选择Probe寄存器
    gen.CommandSend(0x0600)


    probe = probeMod() # 控制Probe bit数据的生成
    # 最外侧循环为通道选择
    for chn in range(36):
        print("Calibration Channel: " + str(chn))
        gen.CommandSend(0x0501) #将数据通道指向FPGA内部SC/Probe模块
        probe.setChn(chn,0)
        cfgByte = probe.formatOutput()
        for i in range(len(cfgByte)):
            gen.CommandSend(0x0300+cfgByte[i]) #传输数据
        gen.CommandSend(0x0500) #关闭传输通道

        gen.CommandSend(0x0800) #开始向ASIC配置Probe
        
        sleep(0.5) # 暂停50ms，等待读出操作完成
        gen.fClose()
        for elink in enList:
            fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'                
            felixShellDo(fupCmd,infoSlince)
        gen.fOpen()
        sleep(0.5) # 暂停50ms，等到Probe配置完成

        #下面对DAC进行循环
        for dac in rg:
            # dac控制
            # A通道控制
            gen.CommandSend(0x0f00+(dac>>8)) # 小心运算优先级，不同于verilog,下同
            gen.CommandSend(0x0f00+(dac&0xff))
            gen.delay(10)
            # B通道控制
            gen.CommandSend(0x0f00+(0x80|(dac>>8)))
            gen.CommandSend(0x0f00+(dac&0xff))
            gen.delay(10)
            # 开始采集
            gen.CommandSend(0x0100)
            gen.fClose()
            for elink in enList:
                fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'                
                felixShellDo(fupCmd,infoSlince)

            felixShellDo(fdaqCmd+"chn"+str(chn)+"_DAC"+str(dac)+"_&",infoSlince)
            gen.fOpen()

            gen.CommandSend(0x0200)

            gen.fClose()
            for elink in enList:
                fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
                felixShellDo(fupCmd,infoSlince)
            gen.fOpen()

    gen.CommandSend(0x1200)
    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)


def elecSwitchOff(elinkNum = 1,dac = 0): #配置所有芯片的probe
    
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum
    
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0x127f) # enable all chip, and make amplifier active. Accept external trigger

    # 选择Probe寄存器
    gen.CommandSend(0x0600)


    probe = probeMod() # 控制Probe bit数据的生成

    gen.CommandSend(0x0501) #将数据通道指向FPGA内部SC/Probe模块
    probe.closeChn()
    
    cfgByte = probe.formatOutput()
    for i in range(len(cfgByte)):      
        gen.CommandSend(0x0300+cfgByte[i]) #传输数据
    gen.CommandSend(0x0500) #关闭传输通道

    gen.CommandSend(0x0800) #开始向ASIC配置Probe
        
    sleep(0.5)

    
    # dac控制
    # A通道控制
    gen.CommandSend(0x0f00+(dac>>8)) # 小心运算优先级，不同于verilog,下同
    gen.CommandSend(0x0f00+(dac&0xff))
    gen.delay(10)
    # B通道控制
    gen.CommandSend(0x0f00+(0x80|(dac>>8)))
    gen.CommandSend(0x0f00+(dac&0xff))
    gen.delay(10)

    gen.fClose()
    gen.logclose()

    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def elecSingleChn(elinkNum = 1,chip = 0,chn = 0, dac = 100): #配置所有芯片的probe
    
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    
    if(chip == 0):
        print('calibration chip: 1~9')
    else:
        print('calibration chip: ' + str(chip))
    
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0x1255) # enable all chip, and make amplifier active. Accept external trigger

    # 选择Probe寄存器
    gen.CommandSend(0x0600)


    probe = probeMod() # 控制Probe bit数据的生成

    print("Calibration Channel: " + str(chn))
    gen.CommandSend(0x0501) #将数据通道指向FPGA内部SC/Probe模块
    probe.setChn(chn,chip)
    
    cfgByte = probe.formatOutput()
    for i in range(len(cfgByte)):      
        gen.CommandSend(0x0300+cfgByte[i]) #传输数据
    gen.CommandSend(0x0500) #关闭传输通道

    gen.CommandSend(0x0800) #开始向ASIC配置Probe
        
    sleep(0.5)

    
    # dac控制
    # A通道控制
    gen.CommandSend(0x0f00+(dac>>8)) # 小心运算优先级，不同于verilog,下同
    gen.CommandSend(0x0f00+(dac&0xff))
    gen.delay(10)
    # B通道控制
    gen.CommandSend(0x0f00+(0x80|(dac>>8)))
    gen.CommandSend(0x0f00+(dac&0xff))
    gen.delay(10)

    gen.fClose()
    gen.logclose()

    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def selfTrigModGen():
    tmpFile = open(cfgPath + 'selfTrigMod.dat','w+')
    for i in range(40):
        layerId = "0x{:02x} 0x{:02x} ".format(0xFE,i)
        tmpFile.write(layerId)
        tmpFile.write("0x0C 0x04 ")
        tmpFile.write("0xEE 0xEE ")
    tmpFile.close()
    
def trigNumSetGen():
    tmpFile = open(cfgPath + 'trigNumSet.dat','w+')
    for i in range(40):
        layerId = "0x{:02x} 0x{:02x} ".format(0xFE,i)
        tmpFile.write(layerId)
        tmpFile.write("0x0E 0x10 ")
        tmpFile.write("0xEE 0xEE ")
    tmpFile.close()

def elecSingleChnCfgGen(chip = 0,chn = 0, dac = 100,rgmin = 100): #配置所有芯片的probe
        
    # if(chip == 0):
    #     print('calibration chip: 1~9')
    # else:
    #     print('calibration chip: ' + str(chip))
    
    probeFullPath = cfgPath + 'elecCalibCfgFiles/' + 'chn' + str(chn) + '/'
    if not os.path.exists(probeFullPath):
        os.makedirs(probeFullPath)
    if(dac == rgmin):
        gen = generator(probeFullPath + 'adac' + str(dac) + '.dat')
    else:
        gen = generator(probeFullPath + 'dac' + str(dac) + '.dat')

    # 选择Probe寄存器
    if(dac == rgmin):
        for i in range(40):
            gen.CommandSend(0xFE00 + i)
            gen.CommandSend(0x0600)
            probe = probeMod() # 控制Probe bit数据的生成

            print("Calibration Channel: " + str(chn))
            gen.CommandSend(0x0501) #将数据通道指向FPGA内部SC/Probe模块
            probe.setChn(chn,chip)
        
            cfgByte = probe.formatOutput()
            for i in range(len(cfgByte)):      
                gen.CommandSend(0x0300+cfgByte[i]) #传输数据
            gen.CommandSend(0x0500) #关闭传输通道

            gen.CommandSend(0x0800) #开始向ASIC配置Probe
            gen.CommandSend(0xEEEE)
    
    gen.delay(100)
        
    #sleep(0.5)

    
    # dac控制
    # A通道控制
    for i in range(40):
        gen.CommandSend(0xfe00 + i)
        gen.CommandSend(0x0f00+(dac>>8)) # 小心运算优先级，不同于verilog,下同
        gen.CommandSend(0x0f00+(dac&0xff))
        gen.CommandSend(0xeeee)
        #gen.CommandSend('#Delay10')
        gen.delay(10)
        # B通道控制
        gen.CommandSend(0xfe00 + i)
        gen.CommandSend(0x0f00+(0x80|(dac>>8)))
        gen.CommandSend(0x0f00+(dac&0xff))
        #gen.CommandSend('\n10\n')
        gen.CommandSend(0xeeee)
        gen.delay(10)
    
    gen.fClose()
    gen.logclose()

def elecSwitchOffCfgGen(dac = 0): #配置所有芯片的probe
    probeFullPath = cfgPath + 'elecCalibClose/'
    if not os.path.exists(probeFullPath):
        os.makedirs(probeFullPath)
    gen = generator(probeFullPath + 'probeOff_DACOff.dat')
    
    for i in range(40):
        gen.CommandSend(0xfe00 + i)
        
        gen.CommandSend(0x0600)
        probe = probeMod() # 控制Probe bit数据的生成

        gen.CommandSend(0x0501) #将数据通道指向FPGA内部SC/Probe模块
        probe.closeChn()
        cfgByte = probe.formatOutput()
        for i in range(len(cfgByte)):      
            gen.CommandSend(0x0300+cfgByte[i]) #传输数据
        gen.CommandSend(0x0500) #关闭传输通道

        gen.CommandSend(0x0800) #开始向ASIC配置Probe
            
        sleep(0.5)

        
        # dac控制
        # A通道控制
        gen.CommandSend(0x0f00+(dac>>8)) # 小心运算优先级，不同于verilog,下同
        gen.CommandSend(0x0f00+(dac&0xff))
        gen.CommandSend(0x0f00+(0x80|(dac>>8)))
        gen.CommandSend(0x0f00+(dac&0xff))
        gen.CommandSend(0xeeee)

    gen.fClose()
    gen.logclose()

def lightCalibSingleGroupCfgGen(groupNum = 0, dac = 2000,rgmin = 2000):
    
    dacFullPath = cfgPath + 'wideRangelightCalibCfgFiles/' + 'group' + str(groupNum) + '/'
    if not os.path.exists(dacFullPath):
        os.makedirs(dacFullPath)
    if(dac == rgmin):
        gen = generator(dacFullPath + 'adac' + str(dac) + '.dat')
    else:
        gen = generator(dacFullPath + 'dac' + str(dac) + '.dat')
    
    if(dac == rgmin):
        for i in range(40):
            gen.CommandSend(0xfe00 + i)
            gen.CommandSend(0x0b00 + 0x50 + groupNum)
            gen.CommandSend(0xeeee)
    gen.delay(10)
    for i in range(40):
        gen.CommandSend(0xfe00 + i)
        gen.CommandSend(0x0700+(dac>>8)) # 小心运算优先级，不同于verilog,下同
        gen.CommandSend(0x0700+(dac&0xff))
        gen.CommandSend(0xeeee)
        gen.delay(10)
        # B通道控制
        gen.CommandSend(0xfe00 + i)
        gen.CommandSend(0x0700+(0x80|(dac>>8)))
        gen.CommandSend(0x0700+(dac&0xff))
        gen.CommandSend(0xeeee)
        gen.delay(10)
    

    gen.fClose()
    gen.logclose()
    
def lightCalibSwitchOff():
    FullPath = cfgPath + 'lightCalibClose/'
    if not os.path.exists(FullPath):
        os.makedirs(FullPath)
    gen = generator(FullPath + 'lightCalibClose.dat')
    for i in range(40):
        gen.CommandSend(0xfe00 + i)
        gen.CommandSend(0x0b00)
        gen.CommandSend(0x1964)
        gen.CommandSend(0xeeee)

def hvSet(elinkNum = 1,HBUNum = 1, voltageOffet = 0.0): #根据HBU编号找到对应的高压值，基于一定offset配置hv，如果HBUNum = 0则是按照指定电压配置

    if HBUNum == 0:
        voltage = voltageOffet
        volReg32bit = int((voltage-0.1)*24-105)
        hvWordH = 0x3080 + (volReg32bit>>8)
        hvWordL = 0x3000 + (volReg32bit&0x00FF)
        wordSend(elinkNum,hvWordH)
        wordSend(elinkNum,hvWordL)
    else:
        voltage = HVList[HBUNum-1] + voltageOffet
        DIFLoc = DIFOrderList[HBUNum - 1]
        dacPara = HVParaList[DIFLoc - 1]
        volReg32bit = int((voltage-0.1)*dacPara[0] + dacPara[1]) #根据不同dif的参数生成对应的dac道值 控制高压输出 
        hvWordH = 0x3080 + (volReg32bit>>8)
        hvWordL = 0x3000 + (volReg32bit&0x00FF)
        print(dacPara)
        print(HBUNum)
        print(voltage)
        print(volReg32bit)
        print(hvWordH)
        print(hvWordL)
        wordSend(elinkNum,hvWordH)
        wordSend(elinkNum,hvWordL)

def hvSwitch(elinkNum=1, onFlag = 1):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    if(onFlag):
        cmd = "HON"
    else:
        cmd = "HOF"
    cmdLength = 3
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0x0503) #选通HV配置数据传输通道

    gen.CommandSend(0x0302) #03是数据传输命令，02是STX符，是命令头
    checkSum = 0
    for i in range(cmdLength):
        checkSum+=ord(cmd[i])   #数据求和，用于校验
        gen.CommandSend(0x0300+ord(cmd[i]))
    gen.CommandSend(0x0303) #7:0 0x03是END符 ，ETX

    checkSum+=0x05 #将STX，ETX加入校验

    #校验码为求和码的ascii码
    letterHigh = ord(hex((checkSum>>4)&0x0F).upper()[2:])
    letterLow = ord(hex((checkSum&0x0F)).upper()[2:])
    gen.CommandSend(0x0300+letterHigh)
    gen.CommandSend(0x0300+letterLow)
    gen.CommandSend(0x03D0) #CR发送

    gen.CommandSend(0x0502) #关闭HV配置数据传输通道
    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)
    
def sclkFreqSel(elinkNum = 1,freqSel = 1):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    gen = generator(cmdPath + 'tmpCmd.dat')
    if(freqSel==0):
        gen.CommandSend(0x1500) #5MHz
    elif(freqSel==1):
        gen.CommandSend(0x1501) #1MHz
    elif(freqSel==2):
        gen.CommandSend(0x1502) #250KHz
    else:
        print('Frequence Select Parameter need be 0~2')

    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def acqWidthSel(elinkNum = 1,freqSel = 1):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    gen = generator(cmdPath + 'tmpCmd.dat')
    if(freqSel==0):
        gen.CommandSend(0x2000) #4ms
    elif(freqSel==1):
        gen.CommandSend(0x2001) #1ms
    elif(freqSel==2):
        gen.CommandSend(0x2002) #200us
    else:
        print('acqWidth Select Parameter need be 0~2')

    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def singleCellSet(elinkNum = 1):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0x0e01) #set to 1 cell

    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)



def maskLength(elinkNum = 1, masklength = 4):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
             enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum

    gen = generator(cmdPath+'tmpCmd.dat')
    gen.CommandSend(0x1b00+masklength)
    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = 'fupload -e' + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def fecReset(elinkNum = 1):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum
    gen = generator(cmdPath+'tmpCmd.dat')
    gen.CommandSend(0x1d00)
    gen.fClose()
    gen.logclose()
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

    
def wordSend(elinkNum = 1, word = 0x0000):
    infoSlince = 1
    if(type(elinkNum)==int):
        chnList = usedElinkList
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(word)
    gen.fClose()
    gen.logclose()
          
    for elink in enList:
        fupCmd = "fupload -e " + elink + ' ' + cmdPath + 'tmpCmd.dat'
        felixShellDo(fupCmd,infoSlince)

def FLXorGBT(GBTFlag = 0):
    infoSlince = 1
    if(GBTFlag == 0):
        gen = generator(cmdPath + 'tmpCmd.dat')
        gen.CommandSend(0xC0F9)
        gen.fClose()
        gen.logclose()
    else:
        gen = generator(cmdPath + 'tmpCmd.dat')
        gen.CommandSend(0xC0FA)
        gen.fClose()
        gen.logclose()      
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def gbtTrigEn(enable = 1):
    if(enable == 1):
        wordSend(['040'],0xC0F3)
    else:
        wordSend(['040'],0xC0F4)

def clearCycleCnt(ClearEn = 0):
    infoSlince = 1
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0xC0FE)
    gen.fClose()
    gen.logclose()
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def syncClk():
    infoSlince = 1
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0xC0F8)
    gen.fClose()
    gen.logclose()
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def startACQ(StartACQEn = 0):
    infoSlince = 1
    if(StartACQEn == 0):
        gen = generator(cmdPath + 'tmpCmd.dat')
        gen.CommandSend(0xC0F2)
        gen.fClose()
        gen.logclose()
    else:
        gen = generator(cmdPath + 'tmpCmd.dat')
        gen.CommandSend(0xC0F1)
        gen.fClose()
        gen.logclose()      
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def enterACQ():
    FLXorGBT(1)
    syncClk()
    clearCycleCnt()
    startACQ(1)

def quitACQ():
    startACQ(0)
    sleep(0.5)
    FLXorGBT(0)

def resetDIF():
    infoSlince = 1
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0xC0FC)
    gen.fClose()
    gen.logclose()
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def resetElink():
    infoSlince = 1
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0xC0FB)
    gen.fClose()
    gen.logclose()
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def resetElinkIn():
    wordSend(['040'],0xC0FF)

def resetAcqState():
    wordSend(['040'],0xD001)

def acqGapWidthSet(gapWidth = 50):
    gapWidthCmd = 0xD000 + gapWidth
    wordSend(['040'],gapWidthCmd)

def refreshSCAWidth(width = 10):
    widthCmd = 0xE000 + width
    wordSend(['040'],widthCmd)

def sync40M():
    FLXorGBT(1)
    wordSend(['040'],0xF100)
    wordSend(['040'],0x1F00)
    wordSend(['040'],0xF200)
    FLXorGBT(0)

def tstDelay():
    infoSlince = 1
    gen = generator(cmdPath + 'tmpCmd.dat')
    gen.CommandSend(0xC0FA)
    gen.CommandSend(0xF100)
    gen.CommandSend(0x2200)
    gen.CommandSend(0x1C00)
    gen.CommandSend(0x0100)
    gen.CommandSend(0xF200)
    gen.CommandSend(0xC0F9)
    gen.fClose()
    gen.logclose()
    fupCmd = "fupload -e " + '040' + ' ' + cmdPath + 'tmpCmd.dat'
    felixShellDo(fupCmd,infoSlince)

def elecSigTrigSel(elinkNum = 1,sysTrigerEn = 0):
    if(sysTrigerEn == 0):
        wordSend(elinkNum,0x2100)
    else:
        wordSend(elinkNum,0x2101)

def cfgHBU(linkNum = 1, fixInputDAC = 0, HBUNum = HBUOrderList ,outputMod = 'HL',tdcRamp = 1, forceEn = 0,selectThr = 200,trigDelay = 54,thrListFlag = 1,voltageOffet = 0.5): #tdcramp = 0 slowRamp
    """
    生成编号为 HBUNum[0] 的灵敏层的配置文件
    Args:
        linkNum (int): 配置文件的编号, 从 0 开始
        fixInptDAC (int): 目前是 0
        HBUNum (list): HBUNum[0] 是需要生成配置文件的灵敏层编号, 从 1 开始
        outputMod (string): 配置文件输出模式, 分为: 'HL', 'HT', 'AT'
        tdcRamp (int): 目前是 1
        forceEn (int): 模式开关, 分为 0 和 1 两种模式
        selectThr (int): 
        trigDelay (int):
        thrListFlag (int): 是否提取 threshold 列表, 1表示提取, 其他表示不提取
        voltageOffet (float): 作用与所有层的高压偏置值
    
    Returns:
        None: 无返回值
    """

    print("start")
    thrListSelected = []
    if(thrListFlag == 1):
        thrListSelected = thrList


    num = HBUNum[0]
    print(num)
    linkNum = linkNum + 1
    thrOfChips = ''
    j = 0
    for j in range(9):
        thrOfChips = thrOfChips + str(thrListSelected[(num-1)*9+j])
    print(thrOfChips)
    if(forceEn == 0):
        subPath = outputMod + '_thrOpt_wjx4_' + 'HVOptValidModSelectThr200/'
    else:
        subPath = outputMod + 'latest_ForceMod_delay150/'
    if not os.path.exists(cfgPath + subPath):
        os.makedirs(cfgPath + subPath)

    if(fixInputDAC == 1):
        if(forceEn == 0):
            cfgFileName = outputMod + '_link' + str(linkNum) + '_HBU' + str(num) +'_thr'+ thrOfChips + '_tdcRp' + str(tdcRamp) + '_fixInputDAC' 
        else:
            cfgFileName = outputMod + '_link' + str(linkNum) + '_HBU' + str(num) + '_thr1023_allChips' + '_tdcRp' + str(tdcRamp) + '_fixInputDAC'
    else:
        if(forceEn == 0):
            cfgFileName = outputMod + '_link' + str(linkNum) + '_HBU' + str(num) +'_thr'+ thrOfChips + '_tdcRp' + str(tdcRamp) 
        else:
            cfgFileName = outputMod + '_link' + str(linkNum) + '_HBU' + str(num) + '_thr1023_allChips' + '_tdcRp' + str(tdcRamp)

    # if(not os.path.exists(cfgPath + cfgFileName + '.dat')):
    #    print('generate new cfg file\n')
    #    dacList = []
    #    cfgFileHandle = fileHandle(cfgPath,cfgFileName,dacList,chipIDList,thrListSelected,fixInputDAC)
    #    cfgFileHandle.dacRead(fixInputDAC,num)
    #    cfgFileHandle.outputModSelect(outputMod,selectThr)
    #    #cfgFileHandle.thrSet(thr)
    #    cfgFileHandle.tdcRampSet(tdcRamp)
    #    cfgFileHandle.cfgFileWrite(num,forceEn) #函数内已包含file.close()
    #    cfgDatHandle = open(cfgPath + cfgFileName + '.txt')
    #    cfgDat = cfgDatHandle.read()
    #    cfgByte = filter(None,cfgDat.split(' '))
    #    if(i==1):
    #        cfgFileHandle.logRecordTime()
    #    cfgFileHandle.logWrite('\n####'+elink+'configured with'+cfgFileName+'#### \n') #记录通道对应的配置文件
    #    gen = generator(cfgPath + cfgFileName +'.dat')
    #    gen.CommandSend(0x0601)
    #    gen.CommandSend(0x0501)

    #    for byte in cfgByte:
    #        gen.CommandSend(0x0300+int(byte,16))

    #    gen.CommandSend(0x0500)
    #    gen.CommandSend(0x0800)

    #    gen.fClose()
    #    cfgFileHandle.logClose() #关闭log文件

        

    
    #fupCmd = "fupload -e " + elink + " " + cfgPath + cfgFileName + '.dat'
    #felixShellDo(fupCmd)
    #sleep(0.5)
    #print(linkNum)
    ##生成用于非FELIX的DAQ系统的配置文件
    gen = generator(cfgPath + subPath + cfgFileName +'eventSeparated.dat')
    gen.CommandSend(0xFE00 + linkNum - 1)
    gen.CommandSend(0x1309)
    gen.CommandSend(0x1502)
    if(forceEn == 0):
        gen.CommandSend(0x0C01)
    else:
        gen.CommandSend(0x0C04)
    #高压配置命令 前两层暂时为备用板
    if(num>0):
        if(forceEn == 1 and trigDelay == 54):
            voltage = 30
            print(f"voltage = {voltage}")
        else:
            voltage = HVList[num-1] + voltageOffet
            print(f"voltage = {voltage}")
        DIFLoc = DIFOrderList[num - 1]
        dacPara = HVParaList[DIFLoc - 1]
        print(dacPara)
        volReg32bit = int((voltage-0.1)*dacPara[0] + dacPara[1]) #根据不同dif的参数生成对应的dac道值 控制高压输出 
        hvWordH = 0x3080 + (volReg32bit>>8)  # 取高 8 位
        hvWordL = 0x3000 + (volReg32bit&0x00FF)  # 取低 8 位
        gen.CommandSend(hvWordH)
        gen.CommandSend(hvWordL)
    #else:
    #    if(num==1):
    #        gen.CommandSend(0x3083)
    #        gen.CommandSend(0x30C6)
    #    else:
    #        gen.CommandSend(0x3083)
    #        gen.CommandSend(0x30B6)     
        dacList = []
        cfgFileHandle = fileHandle(cfgPath,subPath + cfgFileName,dacList,chipIDList,thrListSelected,fixInputDAC)
        cfgFileHandle.dacRead(fixInputDAC,num)
        cfgFileHandle.outputModSelect(outputMod,selectThr)
        #cfgFileHandle.thrSet(thr)
        cfgFileHandle.tdcRampSet(tdcRamp)
        cfgFileHandle.trigDelaySet(trigDelay)
        cfgFileHandle.cfgFileWrite(num,forceEn) #函数内已包含file.close()
        cfgDatHandle = open(cfgPath + subPath + cfgFileName + '.txt')
        cfgDat = cfgDatHandle.read()
        cfgByte = filter(None,cfgDat.split(' '))
        gen.CommandSend(0x0601)
        gen.CommandSend(0x0501)

        for byte in cfgByte:
            gen.CommandSend(0x0300+int(byte,16))

        gen.CommandSend(0x0500)
        gen.CommandSend(0x0800)
        gen.CommandSend(0xEEEE)
        gen.fClose()
        print("end")
# if os.path.exists(cfgPath + cfgFileName+'.txt'): #删除不必要的txt文件
#     os.remove(cfgPath + cfgFileName+'.txt')

def cfgHBUwithTrigDelay(fixInputDAC = 0, trigDelay = 54, HBUNum = [27],elinkNum = 1,outputMod = 'HL',tdcRamp = 1, forceEn = 0,selectThr = 500,thrListFlag = 1): #tdcramp = 0 slowRamp
    thrListSelected = []
    if(thrListFlag == 1):
        thrListSelected = thrList
    elif(thrListFlag == 2):
        thrListSelected = thrList_2
    elif(thrListFlag == 3):
        thrListSelected = thrList_3

    if(type(elinkNum)==int):
        chnList = usedElinkList #chn list in setting_ustc_2b {'040','041'...}
        enList = []
        for i in range(elinkNum):
            enList.append(chnList[i])
    elif(type(elinkNum)==list):
        enList = elinkNum
    i = 0
    for elink in enList:
        num = HBUNum[i]
        i = i + 1
        thrOfChips = ''
        j = 0
        for j in range(6):
            thrOfChips = thrOfChips + str(thrListSelected[(num-1)*6+j])

        if(fixInputDAC == 1):
            if(forceEn == 0):
                cfgFileName = outputMod + '_HBU' + str(num) +'_thr'+ thrOfChips + '_tdcRp' + str(tdcRamp) + '_TrigDelay' + str(trigDelay) + '_fixInputDAC' 
            else:
                cfgFileName = outputMod + '_HBU' + str(num) + '_thr1023_allChips' + '_tdcRp' + str(tdcRamp) + '_TrigDelay' + str(trigDelay) + '_fixInputDAC'
        else:
            if(forceEn == 0):
                cfgFileName = outputMod + '_HBU' + str(num) +'_thr'+ thrOfChips + '_tdcRp' + str(tdcRamp) + '_TrigDelay' + str(trigDelay) 
            else:
                cfgFileName = outputMod + '_HBU' + str(num) + '_thr1023_allChips' + '_tdcRp' + str(tdcRamp) + '_TrigDelay' + str(trigDelay)

        if(not os.path.exists(cfgPath + cfgFileName+'.dat')):
            print('generate new cfg file'+'\n')
            dacList = []
            cfgFileHandle = fileHandle(cfgPath,cfgFileName,dacList,chipIDList,thrListSelected,fixInputDAC)
            cfgFileHandle.dacRead(fixInputDAC,num)
            cfgFileHandle.trigDelaySet(trigDelay)
            cfgFileHandle.outputModSelect(outputMod,selectThr)
            #cfgFileHandle.thrSet(thr)
            cfgFileHandle.tdcRampSet(tdcRamp)
            cfgFileHandle.cfgFileWrite(num,forceEn) #函数内已包含file.close()
            cfgDatHandle = open(cfgPath + cfgFileName + '.txt')
            cfgDat = cfgDatHandle.read()
            cfgByte = filter(None,cfgDat.split(' '))
            if(i==1):
                cfgFileHandle.logRecordTime()
            cfgFileHandle.logWrite('\n####'+elink+'configured with'+cfgFileName+'#### \n') #记录通道对应的配置文件
            gen = generator(cfgPath + cfgFileName +'.dat')
            gen.CommandSend(0x0601)
            gen.CommandSend(0x0501)

            for byte in cfgByte:
                gen.CommandSend(0x0300+int(byte,16))

            gen.CommandSend(0x0500)
            gen.CommandSend(0x0800)

            gen.fClose()
            cfgFileHandle.logClose() #关闭log文件
        
        fupCmd = "fupload -e " + elink + " " + cfgPath + cfgFileName + '.dat'
        felixShellDo(fupCmd)
        sleep(0.5)
        # if os.path.exists(cfgPath + cfgFileName+'.txt'): #删除不必要的txt文件
        #     os.remove(cfgPath + cfgFileName+'.txt')

# def genSingleHBUCfgFile(HBUNum = 27,outputMod = 'HT',tdcRamp = 1, forceEn = 0):
#     num = HBUNum
#     mon = str(time.localtime().tm_mon).zfill(2)
#     day = str(time.localtime().tm_mday).zfill(2)
#     hour = str(time.localtime().tm_hour).zfill(2)
#     min = str(time.localtime().tm_min).zfill(2)
#     currentTime = mon + day + hour + min
#     for i in range(6):
#         thrOfChips = thrOfChips + str(thrList[(num-1)*6+i-1]) 
#     cfgFileName = outputMod + '_HBU' + str(num) +'_thr'+ thrOfChips + '_' + currentTime
#     dacList = []
#     cfgFileHandle = fileHandle(cfgPath,cfgFileName,dacList,chipIDList,thrList)
#     cfgFileHandle.dacRead(num)
#     cfgFileHandle.outputModSelect(outputMod)
#     #cfgFileHandle.thrSet(thr)
#     cfgFileHandle.tdcRampSet(tdcRamp)
#     cfgFileHandle.cfgFileWrite(num,forceEn) #函数内已包含file.close()
#     cfgFileHandle.logRecordTime()
#     cfgFileHandle.logWrite('\n####'+elink+'configured with'+cfgFileName+'#### \n') #记录通道对应的配置文件
#     #生成包含打开fpga内sc通道等命令的实际配置文件
#     if(not os.path.exists(cfgFileName+'.dat')):

#     cfgDatHandle = open(cfgPath + cfgFileName + '.txt')
#     cfgDat = cfgDatHandle.read()
#     cfgByte = filter(None,cfgDat.split(' '))
#     # gen = generator(cfgPath + cfgFileName +'.dat')
#     # gen.CommandSend(0x0601)
#     # gen.CommandSend(0x0501)

#     # for byte in cfgByte:
#     #     gen.CommandSend(0x0300+int(byte,16))

#     # gen.CommandSend(0x0500)
#     # gen.CommandSend(0x0800)

#     # gen.fClose()


def cfgHCAL(fixInputDAC = 0, outputMod ='AT',forceEn = 0,waitTime = 0.1,tdcRamp = 1,selectThr = 250,thrListSelect = 1,trigDelay=54):
    i = 0
    for i in range(40):
        cfgHBU(i,fixInputDAC, [HBUOrderList[i]],outputMod,tdcRamp,forceEn,selectThr,trigDelay,thrListSelect,voltageOffet=1.5)
        sleep(waitTime)

def cfgHCALwithTrigDelay(fixInputDAC, trigDelay = 54, outputMod ='HL',forceEn = 0,waitTime = 0.1,tdcRamp = 1, selectThr = 190, thrListSelect = 1):
    i = 0
    for i in range(32):
        cfgHBUwithTrigDelay(fixInputDAC, trigDelay,[HBUOrderList[i]],[str(usedElinkList[i])],outputMod,tdcRamp,forceEn,selectThr,thrListSelect)
        sleep(waitTime)

def cfgHCALHV(offset = 0.5):
    i = 0
    for i in range(18):
            hvSet([usedElinkList[i]],HBUOrderList[i],offset) #1 = 0.5 + 0.5 first 0.5 is used to increase gain second 0.5 is used to adjust the inputdac output range 

def cfgHCALwithFixedMod(Mod = 1):
    if(Mod == 1):
        cfgHCAL(0,'HL',0,0.5,1,190,1)
    elif(Mod == 2):
        cfgHCAL(0,'AT',0,0.5,1,190,1)
    elif(Mod == 3):
        cfgHCAL(0,'HL',0,0.5,1,190,2)
    elif(Mod == 4):
        cfgHCAL(0,'HL',0,0.5,1,190,3)
    elif(Mod == 5):
        cfgHCAL(0,'HT',0,0.5,1,190,3)
    elif(Mod == 6):
        cfgHCAL(0,'AT',0,0.5,1,190,3)
    elif(Mod == 7):
        cfgHCAL(1,'HL',0,0.5,1,190,3)
    #cfgHCALLogFile = open('cfgHCALLogFiles/cfgHCALLogFile.txt','a')
    #cfgHCALLogFile.write('\n#### cfg time is'+year + mon + day+' '+hour+':'+minute +'####\n')
    #cfgHCALLogFile.write('\n#### cfg time with mod '+str(Mod) + '####\n')

def tluEn(enFlag = 1):
    if(enFlag == 1):
        wordSend(['040'],0xD002)
    else:
        wordSend(['040'],0xD003)

def initSysCosmicMod():
    sync40M()
    sleep(0.5)
    resetElinkIn()
    sleep(0.5)
    wordSend(32,0x0E01)#set cell num to 1
    sleep(0.5)
    #tluEn()
    #sleep(0.5)
    sclkFreqSel(32,2)
    sleep(0.5)
    refreshSCAWidth(2)
    sleep(0.5)
    #lockVldMod()

def startSys():
    realtimeEnable(32,0b001)
    sleep(1)
    sclkFreqSel(32,2)
    sleep(1)
    enterACQ()

def reStartACQ():
    quitACQ()
    resetAcqState()
    sleep(0.5)
    enterACQ()

def lockVldMod():
    wordSend(['040'],0xD004)

def unlockVldMod():
    wordSend(['040'],0xD005)

def trigGenDelay(delay = 1):
    delayCmd = 0x0E00 + delay
    wordSend(['040'], delayCmd)

def trigSwitch2external(enable = 1):
    if(enable):
        wordSend(['040'],0xC0F5)
    else:
        wordSend(['040'],0xC0F6)

def powerControl(enable = 1):
    if(enable):
        wordSend(['040'],0xA100)
        wordSend(['040'],0xA101)
        wordSend(['040'],0xA102)
        wordSend(['040'],0xA103)
    else:
        wordSend(['040'],0xA000)
        wordSend(['040'],0xA001)
        wordSend(['040'],0xA002)
        wordSend(['040'],0xA003)

def cosmicTst2layer():
    sync40M()
    wordSend(4,0x1309)
    wordSend(4,0x0400)
    sleep(0.5)
    resetElinkIn()
    sleep(0.5)
    realtimeEnable(4,0b001)
    sleep(0.5)
    sclkFreqSel(4,2)
    sleep(0.5)
    cfgHBU(HBUNum=[1,2,3,4],elinkNum=4)
    sleep(0.5)
    wordSend(1,0x3083)
    #wordSend(1,0x30b5)
    wordSend(1,0x30c6)
    wordSend(['041'],0x3083)
    #wordSend(['041'],0x30aa)
    wordSend(['041'],0x30b6)
    hvSet(['042'],3,1)
    hvSet(['043'],2,1)


