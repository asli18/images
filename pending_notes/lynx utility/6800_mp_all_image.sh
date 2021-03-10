
echo "Make 6800 MP all image"

boot_file="images/iot_boot.img"
app_file="images/mp_test_uart.img"
K=1024
boot_regular_size=$(( 64 * $K ))
app_regular_size=$(( 128 * $K ))
REV=$(svn info --xml | sed -n '/commit/,/\/commit/s/ *revision=\"\([0-9]*\)\">/\1/p')

echo "Image file check"
if [ -f $boot_file ] && [ -f $app_file ]; then
	#boot_size=$(wc -c images/iot_boot.img | awk '{print $1}')
	boot_size=$(stat -c%s $boot_file)
	app_size=$(stat -c%s $app_file)
	if [ $boot_size -gt $boot_regular_size ]; then
		echo "iot_boot.img size error $boot_size"
		return
	elif [ $app_size -gt $app_regular_size ]; then
		echo "mp_test_uart.img size error $app_size"
		return
	fi
else
	echo "Lack of image file"
	return
fi

echo "Start creating rev.$REV all image"

file="images/M88WI6800K_r"$REV"_all_image.img"
tr "\000" "\377" < /dev/zero | dd of=$file ibs=1 count=1M
dd if=$boot_file of=$file conv=notrunc
dd if=$app_file of=$file ibs=128K obs=128K count=1 seek=7 conv=notrunc

scp $file aston@192.168.65.97:/home/aston/work/image

