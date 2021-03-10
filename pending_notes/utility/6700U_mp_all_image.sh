
echo "Make 6700U MP all image on Cheetah(boot + ecos + 6700 FW)"

<<usage
update sflash.img first (sflash = boot + (cdb)64K + ecos)
make -C config/mptest/ MODEL=test
or
make clean
make all images
usage

sflash_file="images/sflash.img"
app_v2_file="lynx_fw/v2/mp_test_usb.img"
app_v3_file="lynx_fw/v3/mp_test_usb.img"

K=1024
sflash_regular_size=$(( 2560 * $K ))
app_regular_size=$(( 128 * $K ))
REV=$(svn info --xml | sed -n '/commit/,/\/commit/s/ *revision=\"\([0-9]*\)\">/\1/p')

echo "Image file check"
if [ -f $sflash_file ] && [ -f $app_v2_file ] && [ -f $app_v3_file ]; then
	#boot_size=$(wc -c images/iot_boot.img | awk '{print $1}')
	sflash_size=$(stat -c%s $sflash_file)
	app_v2_size=$(stat -c%s $app_v2_file)
	app_v3_size=$(stat -c%s $app_v3_file)

	if [ $sflash_size -gt $sflash_regular_size ]; then
		echo "sflash.img size error $sflash_size"
		return
	elif [ $app_v2_size -gt $app_regular_size ]; then
		echo "mp_test_usb.img v2 size error $app_v2_size"
		return
	elif [ $app_v3_size -gt $app_regular_size ]; then
		echo "mp_test_usb.img v3 size error $app_v3_size"
		return
	fi
else
	echo "Lack of image file"
	return
fi

echo "Start creating rev.$REV all image"

file="images/ecos_r"$REV"_all_image.img"
tr "\000" "\377" < /dev/zero | dd of=$file ibs=1 count=4352K # 0x40 * 64 + 128 + 128
dd if=$sflash_file of=$file conv=notrunc
dd if=$app_v2_file of=$file ibs=128K obs=128K count=1 seek=32 conv=notrunc
dd if=$app_v3_file of=$file ibs=128K obs=128K count=1 seek=33 conv=notrunc

#scp $file aston@192.168.65.97:/tftpboot/
#scp $file aston@192.168.65.97:/home/aston/work/image

