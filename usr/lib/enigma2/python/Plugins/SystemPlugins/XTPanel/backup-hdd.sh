
echo "HDD-CHECK" > /media/hdd/hdd-check;

if [ -f /media/hdd/hdd-check ] ; then
	build-usb-image.sh /media/hdd | tee /tmp/USB-Full-Backup.log
    
else
	echo "Image creation failed - "
	echo "e.g. wrong backup destination or"
	echo "no space left on backup device"
fi
