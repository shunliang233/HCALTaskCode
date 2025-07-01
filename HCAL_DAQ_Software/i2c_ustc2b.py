from Driver.setting import *
from Driver.setting_ustc_2b import *
import subprocess
from time import sleep
import sys, os
from Driver.flx_tools import pepo_wr, pepo_rd, pepo_rd_64#,pepo_rd_encoding

def elink_config(enable=1,GBT=1,egroup=1,fh=1,epath=0):
	#GBT0, toHost, egroup0~4: 0x1100~0x1140; fromHost, egroup0~4: 0x1170~0x11b0
	#GBT1, toHost, egroup0~4: 0x11C0~0x1200; fromHost, egroup0~4: 0x1230~0x1270
	#GBT2, toHost, egroup0~4: 0x1280~0x12C0; fromHost, egroup0~4: 0x12F0~0x1330
	#GBT3, toHost, egroup0~4: 0x1340~0x1380; fromHost, egroup0~4: 0x13B0~0x13F0
	#epath:: 1: 16b elink; 2: lowest 8b elink; 3: 2rd low 8b elink; 4 lowest 4b elink; 5: 2rd low 4b elink; ........
	elink_addr=elink_addr_list[GBT*2+fh]+(egroup<<4)

	gbt_th_grep = pepo_rd_64(elink_addr)
	if enable==1:
		#enable elink
		pepo_wr(elink_addr, gbt_th_grep | ((1<<epath)&0xffff))
	else:
		#disable elink
		pepo_wr(elink_addr, gbt_th_grep & (0xffffffffffffffff-(1<<epath)))

#def elink_encoding(GBT=1,egroup=1,fh=1,epath=0,encoding=0):
#	#encoding:0 direct 1 8b10b 2 HDLC
#	elink_addr = elink_addr_list[GBT*2+fh]+(egroup<<4)
#	#elink_addr = int(elink_addr)
#	#elink_addr = elink_addr + 1
#	#elink_addr = hex(elink_addr)
#	gbt_th_grep = pepo_rd_encoding(elink_addr)
#	if encoding == 0:
#		gbt_th_grep = str(gbt_th_grep)
#		gbt_th_grep = list(gbt_th_grep)
#		gbt_th_grep[epath*2] = '0'
#		gbt_th_grep[epath*2+1] = '0'
#		gbt_th_grep = ''.join(gbt_th_grep)
#		gbt_th_grep = int(gbt_th_grep)
#		pepo_wr(elink_addr,gbt_th_grep)
#	elif encoding == 1:
#		gbt_th_grep = str(gbt_th_grep)
#		gbt_th_grep = list(gbt_th_grep)
#		gbt_th_grep[epath*2] = '1'
#		gbt_th_grep[epath*2+1] = '0'
#		gbt_th_grep = ''.join(gbt_th_grep)
#		gbt_th_grep = int(gbt_th_grep)
#		pepo_wr(elink_addr,gbt_th_grep)v
#	else:
#		gbt_th_grep = str(gbt_th_grep)
#		gbt_th_grep = list(gbt_th_grep)
#		gbt_th_grep[epath*2] = '0'
#		gbt_th_grep[epath*2+1] = '1'
#		gbt_th_grep = ''.join(gbt_th_grep)
#		gbt_th_grep = int(gbt_th_grep)
#		pepo_wr(elink_addr,gbt_th_grep)
#
def sc_wr_ustc(wr_link, wr, sc_dev_addr, sc_reg_addr, sc_value):
	# wr: 0 write, 1 read
	cmd_data = ((wr << 46) | (sc_dev_addr & 0x3f) << 40) | ((sc_reg_addr & 0xff) << 32) | (sc_value & 0xffffffff)
	fupload_name="sc_wr_data.txt" #generate upload file outside github catalog
	fup_file = open(fupload_name, "w")
	for i in range(6):
		fup_file.write('0x')
		fup_file.write('{:02x}'.format(cmd_data & 0xff))
		fup_file.write(' ')
		cmd_data = cmd_data >>8
	fup_file.close()
	#clk link
	if wr_link==2:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0a6' + ' -r 1 ' + fupload_name
	#data link
	elif wr_link==3:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0e6' + ' -r 1 ' + fupload_name
	elif wr_link==1:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '066' + ' -r 1 ' + fupload_name
	elif wr_link==0:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '026' + ' -r 1 ' + fupload_name
	else:
		print('error elink')
		return -1
	p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	grep_stdout = p.communicate()[0]

def i2c_wr_ustc(wr_link, i2c_dev_addr, i2c_reg_addr, i2c_value):
	sc_dev_addr = DEV_ADDR['I2C_ADDR']
	cmd_data = ((sc_dev_addr << 40) | ((i2c_reg_addr & 0xff) << 32) | ((i2c_dev_addr & 0x7f) << 16) + (i2c_value & 0xff))
	fupload_name="i2c_wr_data.txt"
	fup_file = open(fupload_name, "w")
	for i in range(6):
		fup_file.write('0x')
		fup_file.write('{:02x}'.format(cmd_data & 0xff))
		fup_file.write(' ')
		cmd_data = cmd_data >>8
	fup_file.close()
	fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0a7' + ' -r 1 ' + fupload_name
	p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	grep_stdout = p.communicate()[0]
	sleep(0.01)

def i2c_rd_ustc(wr_link, i2c_dev_addr, i2c_reg_addr, i2c_value):
	sc_dev_addr = DEV_ADDR['I2C_ADDR']
	cmd_data = (0x1 << 46) | (sc_dev_addr << 40) | ((i2c_reg_addr & 0xff) << 32) | ((i2c_dev_addr & 0x7f) << 16)
	fupload_name="i2c_wr_data.txt"
	fup_file = open(fupload_name, "w")
	for i in range(6):
		fup_file.write('0x')
		fup_file.write('{:02x}'.format(cmd_data & 0xff))
		fup_file.write(' ')
		cmd_data = cmd_data >>8
	fup_file.close()
	fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0a7' + ' -r 1 ' + fupload_name
	p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	grep_stdout = p.communicate()[0]
	sleep(0.1)

def spi_wr_ustc(GBT,wr_rd, spi_reg_addr, spi_value):
	sc_dev_addr = DEV_ADDR['si5345_SPI']
	cmd_data = (sc_dev_addr << 40) | wr_rd << 24 | ((spi_reg_addr & 0xffff) << 8) | (spi_value & 0xff)
	fupload_name="spi_wr_data.txt"
	fup_file = open(fupload_name, "w")
	for i in range(6):
		fup_file.write('0x')
		fup_file.write('{:02x}'.format(cmd_data & 0xff))
		fup_file.write(' ')
		cmd_data = cmd_data >>8
	fup_file.close()
	if GBT==3:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0e7' + ' -r 1 ' + fupload_name
	elif GBT==2:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '0a7' + ' -r 1 ' + fupload_name
	elif GBT==1:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '067' + ' -r 1 ' + fupload_name
	else:
		fup_cmd = fdaq_fupload_dir + 'fupload -b 64 -e ' + '027' + ' -r 1 ' + fupload_name
	p = subprocess.Popen([fup_cmd], shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	grep_stdout = p.communicate()[0]
	sleep(0.001)

def main():
	sc_wr_ustc(1,0x07,0x03,0x03)

if __name__ == "__main__":
	main()
