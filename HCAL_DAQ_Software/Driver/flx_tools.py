__author__ = 'Hongbin Liu, Weihao Wu'

from setting import *
import subprocess
import os, array
from time import sleep

    #comment by yuangy, fpepo is vc709 tool peek or poke
def pepo_wr(addr, value):
    pepo_cmd = fdaq_fupload_dir + 'fpepo ' + str(hex(addr)) + ' ' + str(hex(value))
    # communicate through shell
    p = subprocess.Popen([pepo_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]

def pepo_rd(addr):
    pepo_cmd = fdaq_fupload_dir + 'fpepo ' + str(hex(addr))
    # print(pepo_cmd)
    p = subprocess.Popen([pepo_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]
    # print(grep_stdout)
    # log.debug((grep_stdout[-9:-1], 16))
    try:
        pepo_rd_val = int(grep_stdout[-9:-1], 16)
    except:
        print('felix pepo return invalid value!')
    return pepo_rd_val

def pepo_rd_64(addr):
    pepo_cmd = fdaq_fupload_dir + 'fpepo ' + str(hex(addr))
    # print(pepo_cmd)
    p = subprocess.Popen([pepo_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]
    # print(grep_stdout)
    # log.debug((grep_stdout[-9:-1], 16))
    return int(grep_stdout[-17:-1], 16)

def pepo_rd_encoding(addr):
    pepo_cmd = fdaq_fupload_dir + 'fpepo ' + str(hex(addr))
    # print(pepo_cmd)
    p = subprocess.Popen([pepo_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]
    # print(grep_stdout)
    # log.debug((grep_stdout[-9:-1], 16))
    return int(grep_stdout[-17:-1], 16)


def bitlen(cmd):
    # Calculate the bit length of command data
    length = 0
    while (cmd):
        cmd >>= 1
        length += 1
    return(length)

def cmd_convert(cmd):
    """Convert the command data into the format for fupload
    @:param cmd: command data for FEI4B chip
    @:return cmd_for_fup: command data used for fupload
    @:caution: due to 4-bit Elink used in FELIX, FEI4 1-bit command data needs 4-bit FELIX output data
    @          due to LSB of CR in FELIX, the 4-bit data is exchanged in one Byte data (8-bit)
    """
    cmd_len = bitlen(cmd)
    if cmd_len == 0:
        log.error('the command should not be 0 bit')
        return 0
    cmd_for_fup = []
    if cmd_len % 2 == 1:  #The command for fupload is in unite of Byte
        cmd <<= 1
        cmd_len += 1
    # for j in range(8):
    #     cmd_for_fup.append(0b00110011)

    for i in range(bitlen(cmd)/2):
        bit_a = (cmd >> (cmd_len-i*2-1)) & 0b1
        bit_b = (cmd >> (cmd_len-i*2-2)) & 0b1
        cmd_for_fup.append(bit_b << 7 | bit_b << 6 | bit_b << 5 | bit_b << 4 | bit_a << 3 | bit_a << 2 | bit_a << 1 | bit_a)
        # cmd_for_fup.append((bit_a) << 7 | (bit_a) << 6 | (bit_a) << 5 | (bit_a) << 4 | (bit_b)<< 3 | (bit_b) << 2 | (bit_b) << 1 | (bit_b))

    return cmd_for_fup

def fup_file_wr(cmd, fup_file, insert_sleep=True):
    cmd = cmd_convert(cmd)
    if len(cmd) < 2:
        print("Invalid FE-I4B Command!")
        return 0
    if insert_sleep == True:
        fup_file_wr_sleep(1, fup_file)

    for i in range(len(cmd)):
        cmd_4char = "{0:#0{1}x}".format(cmd[i], 4)
        fup_file.write(str(cmd_4char) + ' ')

    if (len(cmd)%2 == 1):      # The command for the fupload must be even Bytes
        fup_file.write('0x00')
    fup_file.write('\n')

def fup_file_wr_zeros(delay_cnt, fup_file):
    fup_file.write('+ 0x00 ' + str(delay_cnt))
    fup_file.write('\n')

def fup_file_wr_sleep(time, fup_file):
    fup_file.write('\n')
    fup_file.write('& ' + str(time))
    fup_file.write('\n')

#def fup_file_wr_header(fup_file):
#    fup_file.write(' 0x56 ')  #a6 ')  #reversed: 56

#def fup_file_wr_trailer(fup_file):
#    fup_file.write(' 0x78 ')  #e1 ')  #reversed: 78

def fup_file_gen(cmd):
    """write command to an file that will be used for fupload
    @:param cmd: command data
    @:return none
    @:caution: due to 4-bit Elink used in FELIX, FEI4 1-bit command data needs 4-bit FELIX output data
    @          due to LSB of CR in FELIX, the 4-bit data is exchanged in one Byte data (8-bit)
    """
    if len(cmd) < 2:
        print("Invalid FEI4B Command!")
        return 0
    fup_file = open(fup_file_name, 'w')
    for i in range(len(cmd)):
        cmd_4char="{0:#0{1}x}".format(cmd[i],4)
        fup_file.write(str(cmd_4char) + ' ')
    fup_file.close()

def fup_cmd_issue():
    fup_cmd = fdaq_fupload_dir +'fupload -b 64 -e ' + elink_number + ' -r 1 ' + fup_file_name
    p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]

def fup_cmd_gen_issue(cmd):
    cmd_conv = cmd_convert(cmd)
    fup_file_gen(cmd_conv)
    fup_cmd = fdaq_fupload_dir +'fupload -b 64 -e ' + elink_number +' -r 1 '+ fup_file_name
    p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    grep_stdout = p.communicate()[0]

def fdaq_issue(time, fdaq_file):
    fdaq_cmd = fdaq_fupload_dir + 'fdaq -T -t ' + str(int(time)) + ' ' + fdaq_file + ' &'
    p = subprocess.Popen([fdaq_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # grep_stdout = p.stdout.readlines()
    # p = os.popen(fdaq_cmd)


def fdaq_issue_X(time, fdaq_file):
    fdaq_cmd = fdaq_fupload_dir + 'fdaq -f 4096 -X -T -t ' + str(int(time)) + ' ' + fdaq_file + ' &'
    p = subprocess.Popen([fdaq_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # p = os.popen(fdaq_cmd)
    # grep_stdout = p.stdout.readlines()

def fdaq_issue_XX(time, fdaq_file):
    fdaq_cmd = fdaq_fupload_dir + 'fdaq -f 4096 -X -t ' + str(int(time)) + ' ' + fdaq_file + ' &'
    p = subprocess.Popen([fdaq_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    # p = os.popen(fdaq_cmd)
    # grep_stdout = p.stdout.readlines()

def elink_num_set(gbt_link, group_number, path_number):
    global elink_number

    gbt_link &= 0x3
    group_number &= 0xf
    path_number &= 0xf
    felink_cmd = fdaq_fupload_dir + 'felink -G '+str(gbt_link) + ' -g ' + str(group_number) + ' -p ' + str(path_number)
    p = subprocess.Popen([felink_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output = p.stdout.readlines()[0]
    # log.debug(output)
    elink_number = '0x'+output[7:10]
    # output = os.popen(felink_cmd)
    # elink_info = output.readline() # only read the first line
    # elink_number = '0x'+elink_info[7:10]

# def fdaq_data_conv():
#     if os.path.exists('fei4_data.dat'):
#         os.remove('fei4_data.dat')
#     list_of_files = os.listdir(os.getcwd())
#     for each_file in list_of_files:
#         if each_file.startswith('fei4_data-'):
#             #print each_file
#             cmd = 'mv ' + str(each_file) + ' fei4_data.dat'
#             os.popen(cmd)

# def fei4_data_analysis_fcheck(data_file):
#     datain=open(data_file,'rb').read()
#     CC=array.array('B', datain)

#     if os.path.exists('dataout.dat'):
#         os.remove('dataout.dat')

#     fchk_cmd = fdaq_fupload_dir + 'fcheck -C -F 1 ' + data_file
    #fchk_cmd = fdaq_fupload_dir + 'fcheck ' + data_file
#     p = subprocess.Popen([fchk_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    #retvalue = os.popen(fchk_cmd).readlines()
#     grep_stdout = p.stdout.readlines()
#     sleep(0.5)
    # temp_data_file = 'dataout.dat'
    # datain=open(temp_data_file,'rb').read()
    # data=array.array('B', datain)
    # print(data)


def main():

    gbt_link = 0
    group_number = 0
    path_number = 2

    #test4()
if __name__ == "__main__":
    main()

