__author__="Hongbin Liu, Weihao Wu"

import logging, coloredlogs, colorlog

##################################
## FE-I4B command protocol
field1 = {"LV1": 0b11101, "OTHERS": 0b10110}
field2 = {"BCR": 0b0001, "ECR": 0b0010, "CAL": 0b0100, "SLOW": 0b1000}
field3 = {"RD_REG": 0b0001, "WR_REG": 0b0010, "WR_FR": 0b0100, "GLB_RST": 0b1000, "GLB_PULSE": 0b1001, "RUN_MODE": 0b1010}
field4 = 0x8 #broadcast

###################################
## FELIX low-level software tools
fup_file_name = 'fupload_cmd.txt'
fdaq_file_name = 'fei4_data.dat'
fcheck_file_name = 'dataout.dat'

atlaspix_file_name = 'atlaspix_data.dat'

trig_file_name = 'fei4-matrix-arrayb.txt'
tot_file_name = 'fei4-matrix-arrayt.txt'

#fdaq_file_name_org = 'fei4_data.dat' #use to rename data data file
elink_number = '0'

#################################
## FELIX extral registers, based on RM3.7
FELIX_LINK_REG_RM3p7 = {0: {'CMDWR_DATA_ADDR': 0x5710,'CMDWR_TRIG_ADDR': 0x5700, 'CMDWR_TRIG': 0x1, 'CMDRD_ADDR': 0x6910, 'DATRD_ADDR': 0x6920, 'DATRD_MON': 0x6900},
                  1: {'CMDWR_DATA_ADDR': 0x5720,'CMDWR_TRIG_ADDR': 0x5700, 'CMDWR_TRIG': 0x2, 'CMDRD_ADDR': 0x6930, 'DATRD_ADDR': 0x6940, 'DATRD_MON': 0x6900},
                  2: {'CMDWR_DATA_ADDR': 0x5730,'CMDWR_TRIG_ADDR': 0x5700, 'CMDWR_TRIG': 0x4, 'CMDRD_ADDR': 0x6950, 'DATRD_ADDR': 0x6960, 'DATRD_MON': 0x6900},
                  3: {'CMDWR_DATA_ADDR': 0x5740,'CMDWR_TRIG_ADDR': 0x5700, 'CMDWR_TRIG': 0x8, 'CMDRD_ADDR': 0x6970, 'DATRD_ADDR': 0x6980, 'DATRD_MON': 0x6900}
                  }
FELIX_FEI4_CMD_REG_RM3p7 = {'TRIG_LINK':0x5750, 'CMD_FO_SEL':0x5760, 'TRIG_LATENCY':0x5770, 'CALIBRATION':0x5780, 'CAL_NUM':0x5790, 'CAL_INTERVAL':0x57a0, 'CAL_MULTIPLE_VALID':0x57b0}
FELIX_GBTLCK_REG_RM3p7 = 0x6730
FELIX_CLK_CONFIG_CMD_RM3p7 = "flx-init -T 1"

# flx_tools_path_vc709_rm3p7 = 'felix_tools/vc709_rm3.7/'
#modified by yuangy, change to absolute path in felix server in ustc
flx_tools_path_vc709_rm3p7=''

## FELIX extral registers, based on RM4.4
FELIX_LINK_REG_RM4p4 = {0: {'CMDWR_DATA_ADDR': 0x6730,'CMDWR_TRIG_ADDR': 0x6720, 'CMDWR_TRIG': 0x1, 'CMDRD_ADDR': 0x7850, 'DATRD_ADDR': 0x7860, 'DATRD_MON': 0x7840},
                 1: {'CMDWR_DATA_ADDR': 0x6740,'CMDWR_TRIG_ADDR': 0x6720, 'CMDWR_TRIG': 0x2, 'CMDRD_ADDR': 0x7870, 'DATRD_ADDR': 0x7880, 'DATRD_MON': 0x7840},
                 2: {'CMDWR_DATA_ADDR': 0x6750,'CMDWR_TRIG_ADDR': 0x6720, 'CMDWR_TRIG': 0x4, 'CMDRD_ADDR': 0x7890, 'DATRD_ADDR': 0x78a0, 'DATRD_MON': 0x7840},
                 3: {'CMDWR_DATA_ADDR': 0x6760,'CMDWR_TRIG_ADDR': 0x6720, 'CMDWR_TRIG': 0x8, 'CMDRD_ADDR': 0x78b0, 'DATRD_ADDR': 0x78c0, 'DATRD_MON': 0x7840}
                 }
FELIX_FEI4_CMD_REG_RM4p4 = {'TRIG_LINK':0x6770, 'CMD_FO_SEL':0x6780, 'TRIG_LATENCY':0x6790}
FELIX_GBTLCK_REG_RM4p4 = 0x7730
FELIX_CLK_CONFIG_CMD_RM4p4 = "flx-init -T 1"

# flx_tools_path_flx712_rm4p4 = 'felix_tools/flx712_rm4.4/'#comment by yuangy
flx_tools_path_flx712_rm4p4 = ''

# FELIX extral registers, global variable
FELIX_LINK_REG = FELIX_LINK_REG_RM4p4
FELIX_FEI4_CMD_REG = FELIX_FEI4_CMD_REG_RM4p4
FELIX_GBTLCK_REG = FELIX_GBTLCK_REG_RM4p4
FELIX_CLK_CONFIG_CMD = FELIX_CLK_CONFIG_CMD_RM4p4
flx_tools_path = flx_tools_path_flx712_rm4p4 #'./feix_tools/'
fdaq_fupload_dir = flx_tools_path_flx712_rm4p4

# FELIX_LINK_REG = FELIX_LINK_REG_RM3p7
# FELIX_FEI4_CMD_REG = FELIX_FEI4_CMD_REG_RM3p7
# FELIX_GBTLCK_REG = FELIX_GBTLCK_REG_RM3p7
# FELIX_CLK_CONFIG_CMD = FELIX_CLK_CONFIG_CMD_RM3p7
# flx_tools_path = flx_tools_path_vc709_rm3p7
# fdaq_fupload_dir = flx_tools_path_vc709_rm3p7

# components I2C address
################################
I2C_DEV_DICT = {
                # Telescope
                'I2C_TEL_MUX_ADDR': 0b1110100,
                'I2C_FMC_MUX_ADDR': 0b1110000,
                'I2C_SI5345_ADDR': 0b1101000,

                # Caribou
                'I2C_CAR_PCA9846': 0b1110001,
                'I2C_CAR_PCA9539': 0b1110110,


                'I2C_CAR_MON_P1': 0b1000000,
                'I2C_CAR_MON_P2': 0b1000001,
                'I2C_CAR_MON_P3': 0b1000010,
                'I2C_CAR_MON_P4': 0b1000011,
                'I2C_CAR_MON_P5': 0b1000100,
                'I2C_CAR_MON_P6': 0b1000101,
                'I2C_CAR_MON_P7': 0b1000110,
                'I2C_CAR_MON_P8': 0b1001010,

                'I2C_CAR_PWR_DAC': 0b1001001,
                'I2C_CAR_BIAS_DAC1': 0b1001010,
                'I2C_CAR_BIAS_DAC2': 0b1001100,
                'I2C_CAR_BIAS_DAC3': 0b1001101,
                'I2C_CAR_BIAS_DAC4': 0b1001110,

                'I2C_CAR_INJ_DAC': 0b1001111,

                'I2C_CAR_DAC1': 0b1001001,
                'I2C_CAR_DAC2': 0b1001010,
                'I2C_CAR_DAC3': 0b1001011,
                'I2C_CAR_DAC4': 0b1001100,
                'I2C_CAR_DAC5': 0b1001101,
                'I2C_CAR_DAC6': 0b1001110,
                'I2C_CAR_DAC7': 0b1001111
                }

###################################
## Slow Control Device address
DEV_ADDR = {'SYSTEM_CONTROL_ADDR': 0x01,
            'I2C_ADDR': 0x02,
            'GBT_ADDR': 0x03,
            'FEI4_ADDR': 0x04,
            'DUT_ADDR': 0x05,
            'I2C_DD_ADDR': 0x06,
            'MIMOSA_ADDR': 0x07,
            'si5345_SPI': 0x08
            # 'TEL_I2C_MUX_ZC706_ADDR': 0x11,
            # 'TEL_I2C_MUX_FMC_ADDR': 0x12,
            # 'TEL_SI5345_ADDR': 0x13,

            # 'CAR_DAC1': 0x30,
            # 'CAR_DAC2': 0x31,
            # 'CAR_DAC3': 0x32,
            # 'CAR_DAC4': 0x33,
            # 'CAR_DAC5': 0x34,
            # 'CAR_DAC6': 0x35,
            # 'CAR_DAC7': 0x36,

            # 'CAR_I2C_MUX': 0x14,
            # 'CAR_PCA9539': 0x15,
            # 'CAR_SI5345': 0x16,

            # 'CAR_MON_P1': 0x38,
            # 'CAR_MON_P2': 0x39,
            # 'CAR_MON_P3': 0x3a,
            # 'CAR_MON_P4': 0x3b,
            # 'CAR_MON_P5': 0x3c,
            # 'CAR_MON_P6': 0x3d,
            # 'CAR_MON_P7': 0x3e,
            # 'CAR_MON_P8': 0x3f,
            }

SYSTEM_CONTROL_REG = {'SYSTEM_RST_REG': 0x00, 'TEST_REG': 0x01}
# '0x02': si5345 reset
# Current monitor slave I2C address
# This will be fulfilled in the firmware
#MON_I2C_ADDR = {"P1": 0x40, "P2": 0x41, "P3": 0x42, "P4": 0x43, "P5": 0x44, "P6": 0x45, "P7": 0x46, "P8": 0x4a}

##############################################
## Telescope GBT Device address: registers addresses
# GBT_REG = {'SOFT_RXRST': 0x00, 'SOFT_TXRST': 0x01, 'CPLL_RST': 0x02, 'GTH_RX_RST': 0x03, 'GTH_TX_RST': 0x04, 'GBT_RX_RST': 0x05, 'GBT_TX_RST': 0x06, 'ODDEVEN': 0x07, 'LINK_RST': 0x08, 'FEI4_CMD_ENABLE': 0x09, 'MON_ALIGN_DONE': 0x0a, 'SC_BUS_STABLE': 0x0b, 'FEI4_CMD_VALID': 0x0c}
GBT_REG = {'LINK_RST': 0x01, 'MON_ALIGN_DONE': 0x11, 'SC_BUS_STABLE': 0x12}

FEI4_SC_REG= {'FEI4_CMD_ENABLE': 0x01, 'FEI4_CHANNEL_ENABLE': 0x2, 'FEI4_DOB_SYNC': 0x03, 'FEI4_DOB_SYNC_CHK': 0x04, 'FEI4_CMD_VALID': 0x11, 'FEI4_DOB_LOCKED': 0x12}

FEI4_CHAN_MAP = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9, 'K': 10, 'L': 11}

FEI4_IDELAY_MAP = {
  'A': {'IDELAY_LOAD_TRIG': 0x001, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 0, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x21},
  'B': {'IDELAY_LOAD_TRIG': 0x002, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 5, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x22},
  'C': {'IDELAY_LOAD_TRIG': 0x004, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 10, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x23},
  'D': {'IDELAY_LOAD_TRIG': 0x008, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 15, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x24},
  'E': {'IDELAY_LOAD_TRIG': 0x010, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 20, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x25},
  'F': {'IDELAY_LOAD_TRIG': 0x020, 'IDELAY_VALUE_REG': 0x03, 'IDELAY_VALUE_SHIFT': 25, 'IDELAY_MON_REG': 0x13, 'DOB_CHK_REG':0x26},
  'G': {'IDELAY_LOAD_TRIG': 0x040, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 0, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x27},
  'H': {'IDELAY_LOAD_TRIG': 0x080, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 5, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x28},
  'I': {'IDELAY_LOAD_TRIG': 0x100, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 10, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x29},
  'J': {'IDELAY_LOAD_TRIG': 0x200, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 15, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x2a},
  'K': {'IDELAY_LOAD_TRIG': 0x400, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 20, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x2b},
  'L': {'IDELAY_LOAD_TRIG': 0x800, 'IDELAY_VALUE_REG': 0x04, 'IDELAY_VALUE_SHIFT': 25, 'IDELAY_MON_REG': 0x14, 'DOB_CHK_REG':0x2c}
           }

fei4_glreg_list = [0x0, 0x100, 0x800, 0x4601, 0x40, 0xd405, 0xd4, 0x6914, 0xf258, 0xaa, 0x784c, 0x56d4, 0x6200, 0x0, 0xd526, 0x1a96, 0x38, 0xab, 0x32ff, 0x640, 0xffff, 0x0, 0x0, 0x0, 0x0, 0xd200, 0x58, 0x8000, 0x8206, 0x0007, 0x0, 0xf400]
FEI4_CHANNELS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L']
# TRIG_LINK: valid Hitor link, 1 GBT link should be selected
# CMD_FO_SEL: selection the fei4 command source between the Central Router (fupload software) or the fast command generator, 1: fast command
# TRIG_LATENCY: the latency to generate trigger command, after receiving the Hitor signal
# CALIBRATION: manually send one calibration command at the rise edge
# CAL_NUM: the number of calibration commands to send in the multiple calibration mode
# CAL_INTERVAL: the clock circles between two calibration commands in the multiple calibration mode
# CAL_MULTIPLE_VALID: enable the multiple calibration mode

MIM_SC_REG= {'MIM_FIFO_RST': 0x01, 'MIM_RST': 0x02, 'MIM_START': 0x03, 'MIM_DUAL_CHAN': 0x04, 'MIM_TEST_MODE': 0x05, 'MIM_JTAG_VS_DATA': 0x06, 'MIM_FRAME_CNT': 0x07, 'MIM_FRAME_EN': 0x08}

##########################
## H35
DUT_REG = {'DUT_SOFT_RST': 0x10, 'DUT_IO_RST': 0x11, 'DUT_CFG_START': 0x12, 'DUT_CFG_OUT_EN': 0x13, 'DUT_CFG_LEN': 0x14, 'DUT_CFG_RAM_RST': 0x15, 'DUT_DOB_SYNC_RST': 0x16, 'DUT_TRIGGER': 0x17, 'DUT_TRIGGER_CNT_RST': 0x18, 'DUT_DOB_FSM_RST': 0x19, 'DUT_TRIGGER_DURATION': 0x1a, 'INJ_FLG': 0x20, 'INJ_PLS_CNT': 0x21, 'INJ_HIGH_CNT': 0x22, 'INJ_LOW_CNT': 0x23, 'INJ_OUT_EN': 0x24, 'DUT_CFG_ERROR': 0x30, 'DUT_TRIGGER_DURATION_MON': 0x31, 'DUT_DOB_SYNC_LOCKED': 0x32}

# DUT_REG = {'CFG_FLG': 0x10, 'CFG_REG_LIMIT': 0x11, 'CFG_SHIFT_LIMIT': 0x12, 'CFG_CLK_EN': 0x13, 'CFG_RAM_WR_EN': 0x14, 'RAM_WR_DAT': 0x15, 'CFG_RAM_ADDR': 0x16, 'CFG_OUT_EN': 0x17, 'INJ_FLG': 0x20, 'INJ_PLS_CNT': 0x21, 'INJ_HIGH_CNT': 0x22, 'INJ_LOW_CNT': 0x23, 'INJ_OUT_EN': 0x24, 'INJ_TRI_DELAY': 0x25, 'INJ_MON_CNT_RST': 0x26, 'CFG_RAM_RD_DAT': 0x30, 'INJ_MON_CNT_A1': 0x31, 'INJ_MON_CNT_A2': 0x32, 'INJ_MON_CNT_A3': 0x33, 'INJ_MON_CNT_A4': 0x34}
# # DAC7678 for power rail control
# PWR_DAC_ADR = 0x30  #0x49
# # DAC7678 for current source control
# CUR_DAC_ADR = 0x32  #0x4B
# # DAC7678 for injection amplitude control
# INJ_DAC_ADDR = 0x36  #0x4F

INJ_DAC_CH = dict(INJ1=6, INJ2=4, INJ3=2, INJ4=0)

# DAC7678 for bias generation
# BIAS_DAC_ADDR =  [0x4A, 0x4C, 0x4D, 0x4E]

# #INJ_DAC_CH = 3

VOL_CALIB_FACTOR = 3.62

# Bias DAC reference voltage
CAR_REF_VOLTAGE = 4.096

# The 2 LSB of PCA9539 is reserved for other usage
PWR_CH_MASK = 0x00ff

# Power switch mask of each channel
ON_OFF_MASK = {"P1": 0x8000, "P2": 0x4000, "P3": 0x2000, "P4": 0x1000, "P5": 0x0100, "P6": 0x0200, "P7": 0x0400, "P8": 0x0800}


# DAC channels specified for power rail control
DAC_CH_NUMBER_PWR = dict(P1=0, P2=2, P3=4, P4=6, P5=1, P6=3, P7=5, P8=7)

# H35Demo
# PWR_INIT_VOL = dict(P1=3.3, P2=2.0, P3=3.3, P4=3.3, P5=1.8, P6=1.5, P7=1.2, P8=2.0)
PWR_INIT_VOL = dict(P1=3.3, P2=1.0, P3=1.83, P4=1.83, P5=1.8, P6=1.5, P7=1.2, P8=2.0)
ATLASPIX_PWR_INIT_VOL = dict(P2=1.0, P3=1.83, P4=1.83)
ATLASPIX_PWR_NAME = {'P2': "VSSA", 'P3': "VDDA", 'P4': "VDDD"}
# pwr_init_cfg = {'P2': 1.0, 'P3': 1.83, 'P4': 1.83}


# Current monitor resolution(Unit: mA)
CUR_RES = {"P1": 0.05, "P2": 0.05, "P3": 0.05, "P4": 0.05, "P5": 0.05, "P6": 0.05, "P7": 0.05, "P8": 0.05}

# # Current monitor address
# MON_I2C_ADDR = {"P1": 0x38, "P2": 0x39, "P3": 0x3a, "P4": 0x3b, "P5": 0x3c, "P6": 0x3d, "P7": 0x3e, "P8": 0x3f}

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(log_color)s%(levelname)-8s%(reset)s : %(log_color)s%(message)s%(reset)s"
logging.root.setLevel(LOG_LEVEL)
formatter = colorlog.ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
if not len(log.handlers):
  log.setLevel(LOG_LEVEL)
  log.addHandler(stream)


# class logger :
#     def myLogger(self):
#         logger=logging.getLogger('ProvisioningPython')
#         if not len(logger.handlers):
#             logger.setLevel(logging.DEBUG)
#             now = datetime.datetime.now()
#             handler=logging.FileHandler('/root/credentials/Logs/ProvisioningPython'+ now.strftime("%Y-%m-%d") +'.log')
#             formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
#             handler.setFormatter(formatter)
#             logger.addHandler(handler)
#         return self.logger
# log = logger()

################ MIMOSA
###########Instraction Register
MIM_IR = {'bsr': 0x5, 'dev_id': 0xE, 'bias_dac': 0xF, 'line0pat_reg': 0x10,
          'dis_discri': 0x11, 'seq_pix_reg': 0x12, 'ctrl_pix_reg': 0x13,
          'line1pat_reg': 0x14, 'seq_suze_reg': 0x15, 'header_reg': 0x16,
          'ctrl_suze_reg': 0x17, 'ctrl_8b10b_reg0': 0x18, 'ctrl_8b10b_reg1': 0x19,
          'ro_mode1': 0x1D, 'ro_mode0': 0x1E, 'bypass': 0x1F}

    ###########Data Register length
MIM_DR_LEN = {'dev_id': 32, 'bsr': 10, 'bias_dac': 152, 'line0pat_reg': 1152,
              'dis_discri': 1152, 'seq_pix_reg': 128, 'ctrl_pix_reg': 40,
              'line1pat_reg': 1152, 'seq_suze_reg': 160, 'header_reg': 64,
              'ctrl_suze_reg': 48, 'ctrl_8b10b_reg0': 144, 'ctrl_8b10b_reg1': 312,
              'ro_mode1': 8, 'ro_mode0': 8, 'bypass': 1}

MIM_DEV_ID = 0x4d323601

def bin_rev_n(bin_dat, n):
    temp = bin_dat & 0xffff
    res = 0
    for bit in range(0, n):
        res <<= 1
        res |= (temp >> bit) & 0x1
    return res

def bit_rev_8b(bin_dat):
    temp = bin_dat & 0xff
    res = 0
    for bit in range(0, 8):
        res <<= 1
        res |= (temp >> bit) & 0x1
        # print bin(res)
    return res

def bit_rev_32b(bin_dat):
    temp = bin_dat & 0xffffffff
    res = 0
    for bit in range(0, 32):
        res <<= 1
        res |= (temp >> bit) & 0x1
        # print bin(res)
    return res
