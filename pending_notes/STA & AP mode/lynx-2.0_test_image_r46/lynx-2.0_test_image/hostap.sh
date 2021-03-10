#sudo wpa_supplicant -Dnl80211 -c ./wpa_conf/lynx.conf -i lynx-0 -dt
sudo hostapd ./ap_conf/${1}.conf -dd
 
