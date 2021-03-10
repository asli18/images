#!/usr/bin/python2.7

import sys
import os

top = sys.argv[1]
version = sys.argv[2]
print "gen the firmware header file for version {0}".format(version)

check_usb = os.system("ls images | grep usb_host.img")
if check_usb != 0:
    check_sdio = os.system("ls images | grep sdio_host.img")
    if check_sdio != 0:
		check_mp_usb = os.system("ls images | grep mp_test_usb.img")
		if check_mp_usb != 0:
			check_mp_sdio = os.system("ls images | grep mp_test_sdio.img")
			if check_mp_sdio != 0:
				exit(0)

if check_usb == 0:
    sname = "{0}/images/usb_host.img".format(top)
    dname = "{0}/images/firmware_array.h".format(top)
elif check_sdio == 0:
    sname = "{0}/images/sdio_host.img".format(top)
    dname = "{0}/images/sdio_firmware_array.h".format(top)
elif check_mp_usb == 0:
    sname = "{0}/images/mp_test_usb.img".format(top)
    dname = "{0}/images/mp_firmware_array.h".format(top)
else:
    sname = "{0}/images/mp_test_sdio.img".format(top)
    dname = "{0}/images/mp_sdio_firmware_array.h".format(top)

# count the total bytes
src = open(sname, "rb")
c = src.read(1)
byte_count = 0

while c != "":
    byte_count = byte_count + 1
    c = src.read(1)

count = 0
dst = open(dname, "w")

src.seek(0)
c = src.read(1)

if check_usb == 0 or check_sdio == 0:
	dst.write('#define LYNX_FW_REV {0}\n'.format(version))
	dst.write('#define FIRMWARE_ARRAY_SIZE {0}\n'.format(byte_count))
	dst.write('static unsigned char lynx_static_firmware[FIRMWARE_ARRAY_SIZE]=\n')
else:
	dst.write('#define LYNX_MP_FW_REV {0}\n'.format(version))
	dst.write('#define MP_FIRMWARE_ARRAY_SIZE {0}\n'.format(byte_count))
	dst.write('static unsigned char lynx_static_mp_firmware[MP_FIRMWARE_ARRAY_SIZE]=\n')
dst.write('{\n')

while c != "":
    dst.write("0x{:02x}".format(ord(c)))
    dst.write(", ")
    count = count + 1
    if((count % 16) == 0):
        dst.write('\n')
    c = src.read(1)

dst.write('};')

src.close()
dst.close()
