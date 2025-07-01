__author__ = "Anshun Zhou"

import sys,os

regList = []

regList.append('Sel_Temp_sensor_to_ADC')
regList.append('NC_1')
regList.append('Trig_Ext')
regList.append('Flag_TDC_Ext')
regList.append('Start_Ramp_ADC_Ext')
regList.append('Start_Ramp_TDC_Ext')
regList.append('ADC_Gray')
regList.append('Chip_ID')
regList.append('EN_Probe_OTAq')
regList.append('EN_Analog_OTAq')
regList.append('Analogue_Output_OTAq')
regList.append('NC_2')
regList.append('EN_OR36')
regList.append('ADC_Ramp_Slope')
regList.append('ADC_Ramp_Current_Source')
regList.append('ADC_Ramp_Integrator')
regList.append('EN_input_dac')
regList.append('DAC_reference')
regList.append('Input_DAC')
regList.append('LG_PA_bias')
regList.append('High_Gain_PreAmplifier')
regList.append('EN_High_Gain_PA')
regList.append('Low_Gain_PreAmplifier')
regList.append('EN_Low_Gain_PA')
regList.append('Fast_Shaper_on_LG')
regList.append('Channel_0_to_35_PA')
regList.append('Low_Gain_Slow_Shaper')
regList.append('EN_Low_Gain_Slow_Shaper')
regList.append('Time_Constant_LG_Shaper')
regList.append('High_Gain_Slow_Shaper')
regList.append('EN_High_Gain_Slow_Shaper')
regList.append('Time_Constant_HG_Shaper')
regList.append('Fast_Shapers_Follower')
regList.append('EN_FS')
regList.append('Fast_Shaper')
regList.append('backup_SCA')
regList.append('SCA')
regList.append('Temp_sensor_high_current')
regList.append('Temp')
regList.append('EN_Temp')
regList.append('BandGap')
regList.append('EN_BandGap')
regList.append('EN_DAC')
regList.append('PP_DAC1')
regList.append('EN_DAC2')
regList.append('PP_DAC2')
regList.append('DAC1_Trigger')
regList.append('DAC2_Gain_Sel')
regList.append('TDC_Ramp_Slope')
regList.append('EN_TDC_Ramp')
regList.append('PP_TDC_Ramp')
regList.append('PP_ADC_Discri')
regList.append('PP_Gain_Select_Discri')
regList.append('Auto_Gain')
regList.append('Gain_Select')
regList.append('ADC_Ext_Input')
regList.append('Switch_TDC_On')
regList.append('Discriminator_Mask')
regList.append('EN_Discri_Delay_Vref_and_source_Trigger')
regList.append('PP_Discri_Delay_Vref_and_source_Trigger')
regList.append('Trigger_delay')
regList.append('Discri_4_bit_DAC_Threshold_Adjust')
regList.append('PP_Trigger_Discriminator')
regList.append('PP_4_bit_DAC')
regList.append('PP_Discri_Delay_Trigger')
regList.append('NC_3')
regList.append('PP_Delay_ValidHold')
regList.append('Delay_ValidHold')
regList.append('PP_Delay_RstColumn')
regList.append('Delay_RstColumn')
regList.append('EN_LVDS_receiver_NoTrig')
regList.append('PP_LVDS_receiver_NoTrig')
regList.append('EN_LVDS_receiver_ValEvt')
regList.append('PP_LVDS_receiver_ValEvt')
regList.append('EN_LVDS_receiver_TrigExt')
regList.append('LVDS_receiver_TrigExt')
regList.append('PP_40MHz_10MHz_Clock_LVDS')
regList.append('POD_bypass')
regList.append('End_ReadOut')
regList.append('Start_ReadOut')
regList.append('ChipSat')
regList.append('TransmitOn2')
regList.append('TransmitOn1')
regList.append('Dout2')
regList.append('Dout')

chipIDList = ['10000000','11000000','01000000','01100000','11100000','10100000','00100000','00110000','10110000'] #gray chip id LSB -> MSB 0000_0010 -> 0000_0011

thrList = []

#USTC threshold
#chip1 chip2 chip3 chip4 chip5 chip6
singleEBUChipThrList = [230,230,230,230,230,230,230,230,230]  #HBU1
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,250,230,240,250,250,250,250,230] #HBU2
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU3
singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU4
singleEBUChipThrList = [230,230,230,230,230,230,230,230,230] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,250,250,240,260,250,240,250,255] #HBU5
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] 0
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [255,250,250,255,245,250,250,250,250] #HBU6
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #
singleEBUChipThrList = [225,225,225,225,230,225,225,225,225] #  HBU7
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU8
singleEBUChipThrList = [255,260,260,260,270,260,250,260,260] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,275,275,235,260,235,240,235,240]  #HBU9
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [230,260,260,255,235,245,230,230,230] #HBU10
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU11
singleEBUChipThrList = [265,290,300,260,260,270,260,260,260] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU4
singleEBUChipThrList = [250,250,250,240,260,240,250,250,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [240,240,240,240,250,240,240,240,230] #HBU13
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,250,240,240,260,250,240,240,240] #HBU14
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU15
singleEBUChipThrList = [250,260,250,250,260,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU16
singleEBUChipThrList = [250,250,250,250,260,250,240,240,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [240,250,240,240,260,250,250,240,240] #HBU17
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] 
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,250,250,250,260,250,240,250,250] #HBU18
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU19
singleEBUChipThrList = [250,250,240,250,260,250,250,240,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU20
singleEBUChipThrList = [250,250,240,250,260,250,250,250,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [240,240,250,250,250,250,250,250,240] #HBU21
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [240,250,240,250,250,250,240,250,240] #HBU22
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU23
singleEBUChipThrList = [235,250,240,250,260,250,250,240,240] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU24
singleEBUChipThrList = [240,240,240,240,250,240,240,250,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,250,250,250,255,250,250,250,245] #HBU25
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [240,240,240,250,260,250,240,260,240] #HBU26
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU27
singleEBUChipThrList = [250,250,250,250,260,250,240,240,240] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU28
singleEBUChipThrList = [250,250,250,250,250,250,240,250,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [260,260,320,260,270,260,260,260,260] #HBU29
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [260,340,300,260,260,240,240,240,240] #HBU30
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU31
singleEBUChipThrList = [240,310,290,225,235,230,230,230,240] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU32
singleEBUChipThrList = [240,250,240,250,250,240,250,250,240] #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [230,230,230,230,235,230,230,230,230] #HBU33
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [250,260,250,250,260,240,250,250,240] #HBU34
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU35
singleEBUChipThrList = [250,250,240,250,250,250,250,250,240] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU36
singleEBUChipThrList = [260,250,250,250,250,240,260,260,250] #
thrList.extend(singleEBUChipThrList)
regConfigList = []
singleEBUChipThrList = [230,240,230,240,240,240,230,240,230] #HBU37
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [275,280,275,275,320,275,275,275,275] #HBU38
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU39
singleEBUChipThrList = [270,265,265,265,250,250,235,275,275] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU40
singleEBUChipThrList =  [270,265,265,265,250,250,235,275,275] #
thrList.extend(singleEBUChipThrList)
regConfigList = []
singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #HBU41
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250]  #
thrList.extend(singleEBUChipThrList)
singleEBUChipThrList = [220,220,220,210,215,215,215,215,215] #HBU42
#singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU43
singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)
#singleEBUChipThrList = [390,390,390,390,390,390,390,390,390] #HBU44
singleEBUChipThrList = [250,250,250,250,250,250,250,250,250] #
thrList.extend(singleEBUChipThrList)





# regConfigList 的总 bit 数: 1186
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('000000000001')
regConfigList.append('chipID') # Chip_ID, 8 bit
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('00')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('1')
regConfigList.append('inputDAC')  # Input_DAC, 36x9 bit
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
temp = ''
for i in range(36):  #i start from 1
    temp = temp + '101101001101000'
regConfigList.append(temp) # Channel_0_to_35_PA, 36x15 bit
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('101') # low gain shaper
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('011') # high gain shaper
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('3FF') # DAC1_Trigger, 10 bit
regConfigList.append('0111110100') # DAC2_Gain_Sel (gain trigger)
#regConfigList.append('0011001000') # gain trigger
regConfigList.append('1') # TDC_Ramp_Slope
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0') # Auto_Gain
regConfigList.append('0') # Gain_Select
regConfigList.append('0')
regConfigList.append('0') # Switch_TDC_On
temp = '0'
for i in range(35):  #i start from 1
    temp = temp + '0'
regConfigList.append(temp)
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('00110110') # Trigger_delay == 54
temp = '0'
for i in range(143):  #i start from 1
    temp = temp + '0'
regConfigList.append(temp)
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0')
regConfigList.append('0000')
regConfigList.append('0')
regConfigList.append('001110')
regConfigList.append('0')
regConfigList.append('001110')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('1')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')
regConfigList.append('0')
regConfigList.append('1')

HVList = [  42.52, 42.52, 43.02, 42.34, 42.02, 42.03, 43.07, 42.07, 42.16, 42.66,
            43.12, 42.18, 42.69, 42.24, 42.74, 42.20, 42.26, 42.28, 42.30, 42.34,
            42.31, 42.31, 42.34, 42.37, 42.94, 42.44, 42.44, 42.44, 42.48, 42.98,
            42.48, 42.48, 43.07, 42.00, 42.34, 42.57, 42.34, 42.84, 31.50, 33.00, 31.50, 33.5]
#ndl 两层暂时设置为31V高压
HVParaList = [[24.4705,-105.9799],[24.9529,-108.0434],[24.9529,-123.0152],[24.9529,-123.0152],[24.9529,-110.5387],[24.9529,-105.5482],[25.0392,-126.9955],[24.8671,-109.1153],\
    [24.8397,-120.1867],[24.8397,-120.1867],[25.3005,-127.6026],[24.5376,-85.1526],[26.1534,-156.5664],[25.7482,-137.898],[25.1136,-111.621],[25.1765,-97.264],[23.9776,-70.4062],[23.9776,-72.804],[23.9776,-58.4174],[25.572,-138.5501],\
    [24.0377,-68.7896],[25.2396,-121.0116],[23.9776,-60.8152],[23.7997,-59.3173],[23.9776,-41.6331],\
    [25.2396,-107.1298],[24.0377,-71.1934],[24.0377,-51.9632],[24.0377,-51.9632],[22.893,-34.679],\
    [24.0377,-66.3859],[25.3082,-111.5514],[22.893,-30.3394],[22.893,-30.1004],[24.0377,-71.1934],[24.0377,-61.5783],[25.3028,-131.7937],[25.3028,-124.2029],\
    [23.9177,-49.5545],[23.9177,-49.5545],[23.9177,-49.5545],[24.1585,-60.7932]]

#HBUOrderList = [37,23,22,25,18,17,35,1,19,2,4,15,16,10,9,11,13,14,20,7,5,8,38,36,12,3,29,24,31,21,33,32,34,30,27,26,6,28]
#HBUOrderList = [7,5,8,38,36,12,3,29,24,31,33,21,32,34,30,27,26,6,0,28,37,23,22,25,18,17,35,1,19,2,4,15,16,10,11,9,13,14,20,0]
#HBUOrderList = [38,37,36,35,34,33,32,31,30,29,28,27,26,25,24,23,22,21,20,19,18,17,16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0,0]
HBUOrderList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,40,42]

DIFOrderList = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42]#坐标=HBU的编号
