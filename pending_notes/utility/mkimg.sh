#!/bin/bash
model=1
scp=1
num=$1
firm_arr=0
rom=2

if [ $# -ge 2 ]; then
	if [ $2 -ge 2 ]; then
		rom=$2
		echo ROM ver.$2
		if [ $rom -gt 3 ]; then
			echo ROM version invalid.
			return 0
		fi
	else
		firm_arr=$2
	fi
fi


<<usage
Lynx
A1 rom=2
A2 rom=3

1: boot_test
2: iot_demo; Burn in flash memory at address 0x20000
3: udc_loopback_test; chose the same lib config as usb_host
4: udc_g_zero
5: mp_test_uart;
6: mp_test_usb;
7: mp_test_sdio;
8: usb_host; Need to turn off CONFIG_IOT_DEMO, because of wci.o (lib/wla/Makefile)
9: ate_dut; Turn on Flash booting option!! ATE test boot from flash!!! burn in flash memory at address 0x00
10: wtest;
11: serial_modem
12: iot_demo_wdk
13: mico_boot
14: mico_demo
15: iot_boot

iot_boot flash addr 0x0
iot_demo flash addr 0x20000

FreeRTOS and OS options can't be opened at the same time.
usage

if [ $1 = "mp_all" ]; then

	echo "Build MP 8000 firmware"
	mk clean-mp_test_uart
	make -C config/ MODEL=mp_test_uart ROM=$rom
	scp images/mp_test_uart.img aston@192.168.65.97:/home/aston/work/image

	echo "Build MP 7000U firmware"
	mk clean-mp_test_usb
	make -C config/ MODEL=mp_test_usb ROM=$rom
	scp images/mp_test_usb.img aston@192.168.65.97:/home/aston/work/image

	echo "Build MP 7000S firmware"
	mk clean-mp_test_sdio
	make -C config/ MODEL=mp_test_sdio ROM=$rom
	#scp images/mp_test_sdio.img aston@192.168.65.97:/home/aston/work/image
	cp images/mp_test_sdio.img ../lynx_mp_openwrt/camelot/package/montage/rootfs/src/files/lib/firmware/
	return
fi

if [ $model -eq 0 ]; then
mkcla
mkrlib
mklib
fi

if [ $num -eq 1 ]; then
	mk clean-boot_test
	mk boot_test
	if [ $scp -eq 1 ]; then
		scp images/boot_test.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 2 ]; then
	mk clean-iot_demo
	make -C config/ MODEL=iot_demo ROM=$rom
	if [ $scp -eq 1 ]; then
		scp images/iot_demo.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 3 ]; then
	make -C config/ MODEL=udc_loopback_test ROM=$rom
	#mk lib
	#mk clean-udc_loopback_test
	#mk udc_loopback_test
	if [ $scp -eq 1 ]; then
		scp images/udc_loopback_test.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 4 ]; then
	make -C config/ MODEL=udc_g_zero ROM=$rom
	#mk clean-udc_g_zero
	#mk udc_g_zero
	if [ $scp -eq 1 ]; then
		scp images/udc_g_zero.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 5 ]; then
	mk clean-mp_test_uart
	if [ $model -eq 1 ]; then
		make -C config/ MODEL=mp_test_uart ROM=$rom
	else
		mk mp_test
	fi
	if [ $scp -eq 1 ]; then
		scp images/mp_test_uart.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 6 ]; then
	mk clean-mp_test_usb
	#make -C config/ MODEL=mp_test_usb
	make -C config/ MODEL=mp_test_usb ROM=3
	#mk mp_test
	if [ $firm_arr -eq 1 ]; then
		make firm_arr
		scp images/mp_firmware_array.h aston@192.168.65.97:/home/aston/work/proj/lynx/linux/host/os_dep/linux/include/
	elif [ $scp -eq 1 ]; then
			scp images/mp_test_usb.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 7 ]; then
	mk clean-mp_test_sdio
	make -C config/ MODEL=mp_test_sdio ROM=$rom
	#mk mp_test
	#if [ $scp -eq 1 ]; then
		scp images/mp_test_sdio.img aston@192.168.65.97:/home/aston/work/image
	#fi
	if [ $firm_arr -eq 1 ]; then
		make firm_arr
		scp images/mp_sdio_firmware_array.h aston@192.168.65.97:/home/aston/work/proj/lynx/linux/host/os_dep/linux/include/
	fi
elif [ $num -eq 8 ]; then
	mk clean-usb_host
	make -C config/ MODEL=usb_host ROM=$rom
	if [ $firm_arr -eq 1 ]; then
		make firm_arr
		scp images/firmware_array.h aston@192.168.65.97:/home/aston/work/proj/lynx/linux/host/os_dep/linux/include/
	elif [ $firm_arr -eq 2 ]; then
		scp images/usb_host.img aston@192.168.65.97:/home/aston/work/image/app.img
	elif [ $scp -eq 1 ]; then
		scp images/usb_host.img aston@192.168.65.97:/home/aston/work/image
	fi
	#make firm_arr
	#scp images/usb_host.img aston@192.168.65.97:/home/aston/work/image
elif [ $num -eq 9 ]; then
	mk clean-ate_dut
	if [ $model -eq 1 ]; then
		make -C config/ MODEL=ate_dut ROM=$rom
	else
		mk ate_dut
	fi
	if [ $scp -eq 1 ]; then
		scp images/ate_dut.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 10 ]; then
	mk clean-wtest
	make -C config/ MODEL=wtest ROM=$rom
	#mk wtest
	if [ $scp -eq 1 ]; then
		scp images/wtest.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 11 ]; then
	mk clean-serial_modem
	#mk serial_modem
	mk -C config/ MODEL=serial_modem ROM=$rom
	if [ $scp -eq 1 ]; then
		scp images/serial_modem.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 12 ]; then
	mk clean-iot_demo_wdk
	#mk iot_demo
	make -C config/ MODEL=iot_demo_wdk ROM=$rom
	if [ $scp -eq 1 ]; then
		scp images/iot_demo_wdk.img aston@192.168.65.97:/home/aston/work/image
	fi
elif [ $num -eq 13 ]; then
	mk clean-mico_boot
	make -C config/ MODEL=mico_boot ROM=$rom
	scp images/mico_boot.img aston@192.168.65.97:/home/aston/work/image
elif [ $num -eq 14 ]; then
	mk clean-mico_demo
	mkcla
	mklib
	mk mico_demo
	#make -C config/ MODEL=mico_demo
	scp images/mico_demo.img aston@192.168.65.97:/home/aston/work/image
elif [ $num -eq 15 ]; then
	mk clean-iot_boot
	make -C config/ MODEL=iot_boot ROM=$rom
	scp images/iot_boot.img aston@192.168.65.97:/home/aston/work/image
fi

echo ROM ver.$2

if [ $scp -eq 0 ]; then
	ba-elf-gdb rlib/rlib
fi


