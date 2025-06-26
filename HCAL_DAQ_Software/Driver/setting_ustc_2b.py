__author__="Guangyuan Yuan, Anshun Zhou"


cmdPath = './CMDLib/'
cfgPath = './cfgFiles/'
dacFilesPath = './dacAdjust/dacAdjustFiles'
cmd_link3='0E6'#system cmd
cfgFileList = {
    0:'CFG_externalTrig',
    1:'ValidTH_1us_500dac',
    2:'ValidTH_1us_250dac',
    3:'ValidTH_250THR_Vopcomp_27',
    4:'ValidTH_250THR_Vopcomp_28',
    5:'VopExtchipConfiguration_25',
    6:'VopExtchipConfiguration_29',
    7:'ValidHGLG_250THR_27',
    8:'ValidHGLG_250THR_28',
    9:'ValidHGLG_250THR_29',
    10:'ValidTH_375THR_27',
    11:'ValidTH_326THR_27',
    12:'ValidTH_326THR_28',
    13:'ValidTH_326THR_29',
    14:'ValidTH_375THR_28',
    15:'ValidTH_350THR_28',
    16:'ValidTH_230THR_19',
    17:'ValidTH_230THR_20',
    18:'ValidTH_280THR_20',
    19:'ValidTH_250THR_20',
    20:'ValidTH_375THR_29',
    21:'ValidTH_375THR_25',
    22:'Valid_Thr376_28',
    23:'Valid_Thr376_29',
    24:'VLD_Thr230_11',
    25:'VLD_Thr170_27',
    26:'VLD_Thr160_27',
    27:'extHgTDC_DACThr500',
    28:'VLD_Thr376_UnComp',
    30:'ValidTH_375THR_30',
    31:'ValidTH_250THR_21',
    32:'ValidTH_250THR_22',
    33:'ValidTH_250THR_5',
    34:'ValidTH_250THR_6',
    35:'ValidTH_375THR_31',
    36:'ValidTH_375THR_32',
    37:'Valid_HT_EBU28_10141851',#thr 420
    38:'Valid_HT_EBU28_10141852'  #thr 170
}

usedElinkList = {
        
        #GBT1
	
        #0: '062',
	0: '040',
        1: '041',
        2: '042',
        3: '043',
        4: '044',
        5: '045',
        6: '046',
        7: '047',
        8: '048',
        9: '049',
        10: '04A',
        11: '04B',
        12: '04C',
        13: '04D',
        14: '04E',
        15: '04F',
        16: '050',
        17: '051',
        18: '052',
        19: '053',
        20: '054',
        21: '055',
        22: '056',
        23: '057',
        24: '058',
        25: '059',
        26: '05A',
        27: '05B',
        28: '05C',
        29: '05D',
        30: '05E',
        31: '05F',
        32: '060',
        33: '061',
        #虚拟通道
        34: '062'
        }

# 20个虚拟通道
FEC_name_list3={0: '0C0',
        1: '0C2',
        2: '0C4',
        3: '0C6',
        4: '0C8',
        5: '0CA',
        6: '0CC',
        7: '0CE',
        8: '0D0',
        9: '0D2',
        10: '0D4',
        11: '0D6',
        12: '0D8',
        13: '0DA',
        14: '0DC',
        15: '0DE',
        16: '0E0',
        17: '0E2',
        18: '0E4',
        19: '0E6'}

cmd_link2='0A6'

elink4b_name_list2 = {
        0: '080',
        1: '082',
        2: '084',
        3: '086',
        4: '088',
        5: '08A',
        6: '08C',
        7: '08E',
        8: '090',
        9: '092',
        10: '094',
        11: '096',
        12: '098',
        13: '09A',
        14: '09C',
        15: '09E',
        16: '0A0',
        17: '0A2',
        18: '0A4'}
FEC_cmd_link2='0A4'
FEC_name_list2={0:'081',1:'085',2:'089',3:'08D',4:'091',5:'095',6:'099',7:'09D'}

cmd_link1='066'

elink4b_name_list1 = {
        0: '040',
        1: '042',
        2: '044',
        3: '046',
        4: '048',
        5: '04A',
        6: '04C',
        7: '04E',
        8: '050',
        9: '052',
        10: '054',
        11: '056',
        12: '058',
        13: '05A',
        14: '05C',
        15: '05E',
        16: '060',
        17: '062',
        18: '064'}

FEC_cmd_link1='064'
FEC_name_list1={0:'041',1:'045',2:'049',3:'04D',4:'051',5:'055',6:'059',7:'05D'}


elink4b_name_list0 = {
        0: '000',
        1: '002',
        2: '004',
        3: '006',
        4: '008',
        5: '00A',
        6: '00C',
        7: '00E',
        8: '010',
        9: '012',
        10: '014',
        11: '016',
        12: '018',
        13: '01A',
        14: '01C',
        15: '01E',
        16: '020',
        17: '022',
        18: '024'}

FEC_cmd_link0='024'
FEC_name_list0={0:'001',1:'005',2:'009',3:'00D',4:'011',5:'015',6:'019',7:'01D'}

elink_addr_list={0:0x1100, 1:0x1170, 2:0x11c0, 3:0x1230, 4:0x1280, 5:0x12f0, 6:0x1340, 7:0x13b0}
