# -*- coding: utf-8 -*-
"""
Created on Fri Jun 15 15:58:25 2018

@author: Aneesh
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 15:28:22 2017

@author: Aneesh
"""
import random as rn

PING_CMD = 0xB0B0
FPGA_RD_REGS = 0x5000
FPGA_WR_REGS = 0x5000
SET_SDRAM_ADDR = 0x6000
SET_SDRAM_DATA = 0x6004
GET_SDRAM_DATA = 0x6004
SET_I2C = 0x7004
GET_I2C = 0x7004
SET_I2C_16B = 0x7005
GET_I2C_16B = 0x7005
SET_SENSOR_I2C = 0x7104
GET_SENSOR_I2C = 0x7104
SET_SPI = 0x3004
GET_SPI = 0x3004
SET_SD_ADDR = 0x2000
SET_SD_DATA = 0x2004
GET_SD_DATA = 0x2004
ERASE_SAVE_TABLE = 0xA004
ERASE_QSPI_64KB = 0xA000
ERASE_QSPI_32KB = 0xA001
ERASE_QSPI_4KB  = 0xA002
TRANS_SDRAM_TO_QSPI = 0xA003
TRANS_QSPI_TO_SDRAM = 0xE000
QSPI_STATUS_CMD     = 0xA008
TRANS_TEMP_TO_QSPI  = 0xE00C
TRANS_SENSOR_INIT_LOW_TEMP_TO_QSPI = 0xE00D
TRANS_SENSOR_INIT_HIGH_TEMP_TO_QSPI = 0xE00E

TRANS_SENSOR_INIT_TEMP_RANGE0_TO_QSPI = 0xE00D
TRANS_SENSOR_INIT_TEMP_RANGE1_TO_QSPI = 0xE00E
TRANS_SENSOR_INIT_TEMP_RANGE2_TO_QSPI = 0xE00F
TRANS_SENSOR_INIT_TEMP_RANGE3_TO_QSPI = 0xE010
TRANS_SENSOR_INIT_TEMP_RANGE4_TO_QSPI = 0xE011
TRANS_SENSOR_INIT_TEMP_RANGE5_TO_QSPI = 0xE012
TRANS_SENSOR_INIT_TEMP_RANGE6_TO_QSPI = 0xE013




MARK_BADPIX = 0xA00C
UNMARK_BADPIX = 0xA00D
SWITCH_TO_FACTORY_SETTINGS = 0xA006
SAVE_USER_SETTINGS = 0xA005
LOAD_USER_SETTINGS = 0xA009
LOAD_FACTORY_SETTINGS = 0xA00A
SAVE_OLED_SETTINGS  = 0xA007

BLK_SIZE= 512
header = 0xE0
dev_id, dev_no = 0x3E, 0xFF    
footer1 = 0xFF
footer2 = 0xFE


def con_cmd(header,dev_id, dev_no, cmd_type, cmd, \
            length, data, footer1, footer2):
    pkt =[]
    pkt.append(header)
    pkt.append(0)
    pkt.append(1)
    pkt.append(dev_id)
    pkt.append(dev_no)
    pkt.append((length+3) & 0xFF)
    pkt.append(cmd_type)
    pkt.append(cmd>>8)
    pkt.append(cmd & 0xFF)
#    pkt.append(length >> 8)
    if(length!=0):
        pkt.extend(data)
    
    crc = 0
    for i in range(len(pkt)-1-2):
        crc=crc+pkt[i+1+2]
    crc = crc%256
#    crc = ~crc & 0xFF
#    crc = (crc+1)%256
    return pkt+[crc, footer1, footer2]

def ping(ping_length):
    cmd = PING_CMD
    cmd_type = 0x57
    length = ping_length
    data = [rn.randint(0,255) for x in range(ping_length)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def fpga_read(addr):
    cmd = FPGA_RD_REGS | (addr & 0xFFF)
    cmd_type = 0x52
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
        
    
def fpga_write(addr, data):    
    cmd = FPGA_WR_REGS | (addr & 0xFFF)
    cmd_type = 0x57
    length = 4
    data = [(data & 0xFF000000)>>24,(data & 0xFF0000)>>16,\
            (data & 0xFF00)>>8, (data & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def i2c_write( dev_addr, reg_addr, wr_data):
    cmd = SET_I2C
    cmd_type = 0x57
    length = 2+len(wr_data)
    data = [(dev_addr & 0xFF), (reg_addr & 0xFF)]
    data.extend([x for x in wr_data])
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    

def i2c_write_16b( dev_addr, reg_addr, wr_data):
    cmd = SET_I2C_16B
    cmd_type = 0x57
    length = 2+len(wr_data)
    data = [(dev_addr & 0xFF), (reg_addr & 0xFF)]
    data.extend([x for x in wr_data])
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
        
def i2c_read(dev_addr, reg_addr, read_len):
    cmd = GET_I2C
    cmd_type = 0x52
    length = 3
    data = [(dev_addr & 0xFF), (reg_addr & 0xFF), (read_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def i2c_read_16b(dev_addr, reg_addr, read_len):
    cmd = GET_I2C_16B
    cmd_type = 0x52
    length = 3
    data = [(dev_addr & 0xFF), (reg_addr & 0xFF), (read_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def sensor_i2c_write( dev_addr, reg_addr, wr_data):
    cmd = SET_SENSOR_I2C
    cmd_type = 0x57
    length = 3+len(wr_data)
    data = [(dev_addr & 0xFF), (reg_addr>>8 & 0xFF), (reg_addr & 0xFF) ]
    data.extend([x for x in wr_data])
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
        
def sensor_i2c_read(dev_addr, reg_addr, read_len):
    cmd = GET_SENSOR_I2C
    cmd_type = 0x52
    length = 4
    data = [(dev_addr & 0xFF), (reg_addr>>8 & 0xFF), (reg_addr & 0xFF),\
            (read_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
def set_spi(data):
    cmd = SET_SPI
    cmd_type = 0x57
    length = 2
    data = [(data>>8) & 0xFF, data & 0xFF]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def set_sdram_addr(addr):
    cmd = SET_SDRAM_ADDR
    cmd_type = 0x57
    length = 4
    data = [ (addr & 0xFF000000)>>24, (addr & 0xFF0000)>>16, \
            (addr & 0xFF00)>>8, (addr & 0xFF),]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def set_sdram_data(wr_len):
    cmd = SET_SDRAM_DATA
    cmd_type = 0x57
    length = wr_len
    data = [rn.randint(0,255) for x in range(wr_len)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def get_sdram_data(rd_len):
    cmd = GET_SDRAM_DATA
    cmd_type = 0x52
    length = 2
    data = [(rd_len & 0xFF00)>>8, (rd_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
def get_qspi_status():
    cmd = QSPI_STATUS_CMD
    cmd_type = 0x52
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    

    
def sensor_init_temp_range0_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE0_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def sensor_init_temp_range1_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE1_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
def sensor_init_temp_range2_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE2_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)    
    
def sensor_init_temp_range3_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE3_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)


def sensor_init_temp_range4_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE4_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)
    
    
def sensor_init_temp_range5_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE5_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)    

def sensor_init_temp_range6_save():
    cmd = TRANS_SENSOR_INIT_TEMP_RANGE6_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  
    
def sensor_init_low_temp_save():
    cmd = TRANS_SENSOR_INIT_LOW_TEMP_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def sensor_init_high_temp_save():
    cmd = TRANS_SENSOR_INIT_HIGH_TEMP_TO_QSPI
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)   

def mark_bad_pix():
    cmd = MARK_BADPIX
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  


def unmark_bad_pix():
    cmd = UNMARK_BADPIX
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  


def switch_to_factory_settings():
    cmd = SWITCH_TO_FACTORY_SETTINGS
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  

def save_user_settings():
    cmd = SAVE_USER_SETTINGS
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  

def load_user_settings():
    cmd = LOAD_USER_SETTINGS
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  


def load_factory_settings():
    cmd = LOAD_FACTORY_SETTINGS
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  


def save_oled_settings():
    cmd = SAVE_OLED_SETTINGS
    cmd_type = 0x57
    length = 0
    data = []
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)  

def erase_save_table(dest_addr):
    cmd = ERASE_SAVE_TABLE
    cmd_type = 0x57
    length = 4 
    data = [(dest_addr & 0xFF000000)>>24,(dest_addr & 0xFF0000)>>16,\
            (dest_addr & 0xFF00)>>8,(dest_addr & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def erase_qspi_64KB(dest_addr,block_num):
    cmd = ERASE_QSPI_64KB 
    cmd_type = 0x57
    length = 6 
    data = [(dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16, \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (block_num & 0xFF00)>>8,block_num & 0xFF]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def erase_qspi_32KB(dest_addr,block_num):
    cmd = ERASE_QSPI_32KB 
    cmd_type = 0x57
    length = 6 
    data = [(dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16, \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (block_num & 0xFF00)>>8,block_num & 0xFF]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def erase_qspi_4KB(dest_addr,block_num):
    cmd = ERASE_QSPI_4KB 
    cmd_type = 0x57
    length = 6 
    data = [(dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16, \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (block_num & 0xFF00)>>8,block_num & 0xFF]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def transfer_data_to_qspi(src_addr,dest_addr,transfer_len): 
    cmd    = TRANS_SDRAM_TO_QSPI
    cmd_type = 0x57
    length = 12 
    data = [(src_addr & 0xFF000000)>>24, (src_addr & 0xFF0000)>>16,\
            (src_addr & 0xFF00)>>8, (src_addr & 0xFF),  \
            (dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16,  \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (transfer_len & 0xFF000000)>>24, (transfer_len & 0xFF0000)>>16, \
            (transfer_len & 0xFF00)>>8, (transfer_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)


def transfer_data_to_sdram(src_addr,dest_addr,transfer_len): 
    cmd    = TRANS_QSPI_TO_SDRAM
    cmd_type = 0x57
    length = 12 
    data = [(src_addr & 0xFF000000)>>24, (src_addr & 0xFF0000)>>16,\
            (src_addr & 0xFF00)>>8, (src_addr & 0xFF),  \
            (dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16,  \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (transfer_len & 0xFF000000)>>24, (transfer_len & 0xFF0000)>>16, \
            (transfer_len & 0xFF00)>>8, (transfer_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

def transfer_temp_data_to_qspi(src_addr,dest_addr,transfer_len): 
    cmd    = TRANS_TEMP_TO_QSPI
    cmd_type = 0x57
    length = 12 
    data = [(src_addr & 0xFF000000)>>24, (src_addr & 0xFF0000)>>16,\
            (src_addr & 0xFF00)>>8, (src_addr & 0xFF),  \
            (dest_addr & 0xFF000000)>>24, (dest_addr & 0xFF0000)>>16,  \
            (dest_addr & 0xFF00)>>8, (dest_addr & 0xFF),  \
            (transfer_len & 0xFF000000)>>24, (transfer_len & 0xFF0000)>>16, \
            (transfer_len & 0xFF00)>>8, (transfer_len & 0xFF)]
    return con_cmd(header,dev_id,dev_no, cmd_type, cmd, \
                   length, data, footer1, footer2)

