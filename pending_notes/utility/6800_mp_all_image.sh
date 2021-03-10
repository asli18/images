#!/bin/bash
echo "Make 6800 MP all image"

if [ $# -eq 1 ]; then
	if [ $1 -ge 2 ] && [ $1 -lt 4 ]; then
		rom=$1
		echo ROM ver.$1
	else
		echo ROM version invalid.
		return 0
	fi
else
	echo ROM version invalid.
	return 0
fi

boot_file="images/iot_boot.img"
app_file="images/iot_demo.img"
mp_file="images/mp_test_uart.img"
K=1024
boot_regular_size=$(( 64 * $K ))
app_regular_size=$(( 192 * $K ))
mp_regular_size=$(( 128 * $K ))
REV=$(svn info --xml | sed -n '/commit/,/\/commit/s/ *revision=\"\([0-9]*\)\">/\1/p')

echo "Image file check"
if [ -f $boot_file ] && [ -f $app_file ] && [ -f $mp_file ]; then
	#boot_size=$(wc -c images/iot_boot.img | awk '{print $1}')
	boot_size=$(stat -c%s $boot_file)
	app_size=$(stat -c%s $app_file)
	mp_size=$(stat -c%s $mp_file)
	if [ $boot_size -gt $boot_regular_size ]; then
		echo "iot_boot.img size error $boot_size"
		exit 1
	elif [ $app_size -gt $app_regular_size ]; then
		echo "iot_demo.img size error $app_size"
		exit 1
	elif [ $mp_size -gt $mp_regular_size ]; then
		echo "mp_uart_test.img size error $mp_size"
		exit 1
	fi
else
	echo "Lack of image file"
	return
fi

echo "Start creating ROM rev.$rom & SVN rev.$REV all image"

file="images/M88WI6800K_v"$rom"_r"$REV"_all_image.img"
tr "\000" "\377" < /dev/zero | dd of=$file ibs=1 count=1M
dd if=$boot_file of=$file conv=notrunc
dd if=$app_file of=$file ibs=192K obs=128K count=1 seek=1 conv=notrunc
dd if=$mp_file of=$file ibs=128K obs=128K count=1 seek=7 conv=notrunc

