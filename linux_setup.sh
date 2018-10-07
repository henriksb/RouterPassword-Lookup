#!/usr/bin/bash

if [ "$EUID" -ne 0 ]
	then echo "[!] Please run as root"
	exit
fi

mv RouterPassword.py /usr/local/bin/RouterPassword
mv RouterScrape.py /usr/local/bin/RouterScrape.py
chmod +x /usr/local/bin/RouterPassword
echo "[+] Setup was successful. The script can now be run from anywhere by typing 'RouterPasswor'"
