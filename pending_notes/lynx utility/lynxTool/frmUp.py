#!/usr/bin/python
"""
Lynx Firmware Upgrade Utility.
"""
__version__ = "$Revision: 1.4 $"

from PythonCard import dialog, model
from mpSerial import CSerial
import os
import ntpath
from txRxCmd import TxRxCmd
import serial
from xmodem import XMODEM
import time
import math
import sys
reload(sys)
sys.setdefaultencoding('utf8')  


class MyBackground(model.Background):

    uart = None
    txrxcmd= TxRxCmd()
    img_path =""
    task = ""
    firmware_img_path=""
    target_frm_size=0
    boot_loader=""
    log= None
    window_size= 20
    data_cached=""
    transfer_rate = 14400
    rx_ter_char='R>'

    def on_path0_mouseClick(self, event):
        pathname = self.components.path0txt.text

        file_path= self.chooseByWin()
        filename = ntpath.basename(file_path)
        path = ntpath.dirname(file_path)
        self.components.path0txt.text = file_path
        self.boot_loader =file_path


    def on_path1_mouseClick(self,event):
        pathname = self.components.path1txt.text
        configfile_path, filename, path = "", "", ""

        file_path= self.chooseByWin()
        filename = ntpath.basename(file_path)
        path = ntpath.dirname(file_path)
        self.components.path1txt.text = file_path


    def on_path2_mouseClick(self,event):
        pathname = self.components.path2txt.text

        file_path= self.chooseByWin()
        filename = ntpath.basename(file_path)
        path = ntpath.dirname(file_path)
        self.components.path2txt.text = file_path
        self.firmware_img_path = file_path
        b=2

    def selectAndImgChk(self, pathname):
        pattern = "Img files (*.img)|*.img"
        if os.path.isfile(pathname) is True:
            return pathname
        else:
            path, filename = os.path.split(pathname)
        result = dialog.openFileDialog(self, 'Open', path, filename, pattern)
        if result.accepted:
            print "Select target file"
            filename = ntpath.basename(result.paths[0])
            return result.paths[0]
        else:
            print "Not to select"
            return (None, None)

    def chooseByWin(self):
        pattern = "Img files (*.img)|*.img"
        result= dialog.openFileDialog(self,'Choose the image', '','',pattern)
        if result.accepted:
            filepath = result.paths[0]
            return filepath
        else:
            print "Not to select"
            return (None,None)
   
    def on_chk0_mouseClick(self,event):
        if event.target.checked:
            self.components.path0.enabled= True
        else:
            self.components.path0.enabled= False

    def on_chk1_mouseClick(self,event):
        if event.target.checked:
            self.components.path1.enabled= True
        else:            
            self.components.path1.enabled= False

    def on_chk2_mouseClick(self,event):
        if event.target.checked:
            self.components.path2.enabled= True
        else:
            self.components.path2.enabled= False

    def on_connect_mouseClick(self, event):
        comport = self.components.comportNum.text
        baud_rate = self.components.baudrateChoice.stringSelection
        self.log = self.components.log
        self.log.Clear()
        self.uart = CSerial(comport, baud_rate, 10)
        self.send_command("\r\n",  self.rx_ter_char, 10)
        ret = self.send_command("\r\n",  self.rx_ter_char, 10)
        if ret is not None:
            self.components.connect_state.text = "Connected"
            self.components.connect_state.foregroundColor = (43, 190, 45, 255)
            self.components.frmUp.enabled= True
            self.components.upgradeState.text=""
        self.uart.Close()

    def send_command(self, cmd_, end_ch, timeout=7):
        self.uart.Open()
        words=""
        # dataTpl = self.txrxcmd.command(self.uart,'fi', self.rx_ter_char,5)
        dataTpl = self.txrxcmd.command(self.uart, cmd_, end_ch, timeout)
        if dataTpl[0] == 0:
            print "no such cmd " + "{" + cmd_ + "}"
            self.uart.Close()
            return None
        elif dataTpl[0] == 1:
            formatted_str = dataTpl[1]
            words =formatted_str.split('\r\n')
            self.write_data_to_log2(words)
        else:
            print "command return error"
        self.uart.Close()
        return words

    def on_frmUp_mouseClick(self,event):
        bootloader_offset = 0
        bootloader_size = 10000
        config_offset = str(bootloader_offset + bootloader_size)
        config_size = 10000
        firmware_offset= str(int(config_offset) + config_size)
        firmware_size = "60000"

        if self.components.chk0.checked:
        #xr& download image
            self.send_command('\r\n',  self.rx_ter_char, 10)
            xr_ret = self.send_command('xr', 'C', 15)    # pull the image to mem address: 2c80
            list_= xr_ret 
            boot_addr = list_[2].split(" ")[0].split('=')[1]

            self.uart.Open()
            modem = XMODEM(self.getc, self.putc)
            stream1 = open(self.boot_loader, 'rb')
            print "self.boot_loader" + self.boot_loader
            self.components.upgradeState.text= "Upgrade bootcode..."
            x= modem.send(stream1)
            if x is False:
                self.components.upgradeState.text="Upgrade bootcode failed"
                return
            self.uart.Close()

            self.send_command('\r\n',  self.rx_ter_char, 10)
            time.sleep(1)
            self.send_command('\r\n',  self.rx_ter_char, 5)
            self.send_command('\r\n',  self.rx_ter_char, 5)
            time.sleep(3)
        #fi
            self.send_command('fi',  self.rx_ter_char,8)
            time.sleep(1)
        #fe
            self.components.upgradeState.text="Erasing Flash..."
            self.send_command('fe '+ str(bootloader_offset) + ' ' + str(bootloader_size),  self.rx_ter_char)
            self.send_command('\r\n',  self.rx_ter_char)
            time.sleep(3)
        #fw
            time.sleep(1)
            bootcode_size = os.path.getsize(self.boot_loader)
            print "burn bootcode image"
            self.components.upgradeState.text="Burning Bootcode img..."
            time.sleep(1)
            self.write_img_to_flash('0x00000', bootcode_size, boot_addr)
            self.components.upgradeState.text="Burning bootcode done"
            time.sleep(1)

        if self.components.chk1.checked:
            pass
        if self.components.chk2.checked:
        #xr& download image.
            self.send_command('\r\n',  self.rx_ter_char, 10)
            self.target_frm_size = os.path.getsize(self.firmware_img_path)#
            frm_size = os.path.getsize(self.firmware_img_path)
            timeout = math.floor(self.target_frm_size/self.transfer_rate) + 2#  

            xr_ret = self.send_command('xr', 'C', timeout)    # pull the image to mem address: 2c80
            list_= xr_ret 
            frm_addr = list_[2].split(" ")[0].split('=')[1]

            self.uart.Open()
            modem = XMODEM(self.getc, self.putc)
            frm_img= open(self.firmware_img_path, 'rb')
            self.components.upgradeState.text= "Upgrade firmware..."
            time.sleep(1)
            y= modem.send(frm_img)
            if y is False:
                self.components.upgradeState.text="Upgrade firmware failed"
                return
            self.uart.Close()
            self.send_command('\r\n',  self.rx_ter_char, 10)
            time.sleep(1)
            self.send_command('\r\n',  self.rx_ter_char, 5)
            self.send_command('\r\n',  self.rx_ter_char, 5)
            time.sleep(3)
        #fi
            self.send_command('fi',  self.rx_ter_char, 8)
            time.sleep(1)
        #fe
            self.components.upgradeState.text="Erasing Flash..."
            time.sleep(1)
            self.send_command('fe '+ firmware_offset +' ' + str(firmware_size),  self.rx_ter_char)
            self.send_command('\r\n',  self.rx_ter_char)

        #fw
            print "Burn firmware img"#
            self.components.upgradeState.text="Burning firmware img"
            time.sleep(3)
            self.write_img_to_flash('0x20000', frm_size, frm_addr)
            self.components.upgradeState.text="Burning firmware done"
            time.sleep(1)
        print "Done"
        self.components.connect_state.text = "Disconnected"
        self.components.connect_state.foregroundColor = (225, 26, 53, 255)
        self.components.frmUp.enabled= False


    def getc(self, size, timeout=1):
        return self.uart.serial.read(size)

    def putc(self, data, timeout=1):
        self.uart.serial.write(data)

    def write_data_to_log2(self, data):

        data_num_bf_insert = len(self.log._getItems()) #x
        new_data_num = len(data)            # y

        for i in range(new_data_num):
            self.log.InsertStringItem(data_num_bf_insert + i, unicode(data[i],errors='ignore'))
            self.log.SetStringItem(data_num_bf_insert + i, 0, unicode(data[i],errors='ignore'))

        if len(self.log._getItems()) >= self.window_size:
            if new_data_num <= data_num_bf_insert:
                for x in range(new_data_num):
                    self.log.DeleteItem(x)
            else:
                self.log.DeleteAllItems()

        self.log.redraw()

    def write_img_to_flash(self, offset, img_size, addr):
        total_img = hex(img_size + 32)
        flash_write = 'fw ' + offset + " " + total_img + " " + addr
        self.send_command(flash_write,  self.rx_ter_char, 10)


if __name__ == '__main__':
    app = model.Application(MyBackground)
    app.MainLoop()
