#sudo wpa_supplicant -Dnl80211 -c ./wpa_conf/lynx.conf -i lynx-0 -dt
sudo ifconfig lynx-0 hw ether 00:11:22:33:44:11
sudo wpa_supplicant -Dnl80211 -c ./wpa_conf/${1}.conf -i lynx-0 -dt
