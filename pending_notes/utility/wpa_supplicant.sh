#! /bin/bash

sudo ifconfig lynx-0 hw ether 00:12:13:14:15:16                                                     |
#cd ~/work/lynx-2.0_test_image_r46/lynx-2.0_test_image/wpa_conf/
sudo wpa_supplicant -Dnl80211 -c ~/work/lynx-2.0_test_image_r46/lynx-2.0_test_image/wpa_conf/${1}.conf -i lynx-0 -dt 




sudo ifconfig lynx-0 hw ether 00:11:33:55:77:99
sudo wpa_supplicant -Dnl80211 -c ~/work/script/wpa.conf -i lynx-0 -dt 
#取得 IP
sudo dhclient lynx-0



