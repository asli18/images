#! /bin/bash

sudo ifconfig lynx-0 hw ether 00:12:13:14:15:16                                                     |
#cd ~/work/lynx-2.0_test_image_r46/lynx-2.0_test_image/wpa_conf/
sudo wpa_supplicant -Dnl80211 -c ~/work/lynx-2.0_test_image_r46/lynx-2.0_test_image/wpa_conf/${1}.conf -i lynx-0 -dt 


