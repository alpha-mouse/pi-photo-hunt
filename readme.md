I'm not an expert in anything that follows. But I've installed everything like that.

https://www.raspberrypi.org/forums/viewtopic.php?t=197513

```
sudo apt install libatlas-base-dev
sudo pip3 install tensorflow bottle picamera gpiozero
apt-get install python3-bottle nginx

mkdir ~/Documents/Work
cd ~/Documents/Work
git clone https://github.com/alpha-mouse/pi-photo-hunt.git
cd pi-photo-hunt
mkdir photos
// chmod +x main.py

sudo ln -s $(pwd)/photo_hunt.service /etc/systemd/system
sudo chmod 644 photo_hunt.service
sudo systemctl daemon-reload
sudo systemctl enable photo_hunt.service
sudo systemctl start photo_hunt.service
sudo systemctl status photo_hunt.service

sudo ln -sf $(pwd)/photo_hunt /etc/nginx/sites-available
sudo ln -sf /etc/nginx/sites-available/photo_hunt /etc/nginx/sites-enabled/default
sudo service nginx restart
```

If jupyter is needed, then something like this should do the trick
```
sudo apt-get update && sudo apt-get install git make protobuf-compiler
sudo apt-get install libjpeg8-dev libopenjp2-7-dev libfreetype6-dev
sudo apt-get install python3 python3-pip
sudo pip3 install --upgrade pip
sudo -H pip3 install Cython contextlib2 lxml jupyter matplotlib imageio
sudo -H pip3 install pillow

cd ~/Documents/Work
git clone --depth 1 https://github.com/tensorflow/models.git
git clone --depth 1 https://github.com/cocodataset/cocoapi.git
cd cocoapi/PythonAPI
make
cp -r pycocotools ~/Documents/Work/models/research/

cd ~/Documents/Work/models/research/
protoc object_detection/protos/*.proto --python_out=.
export PYTHONPATH=$PYTHONPATH:~(pwd):~(pwd)/slim

jupyter notebook --ip 0.0.0.0
```

To enable hardware PWM
1. Accodring to https://jumpnowtek.com/rpi/Using-the-Raspberry-Pi-Hardware-PWM-timers.html
edit _/boot/config.txt_ and set the following value for `dtoverlay`
```
dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4
```
2. To allow non root access to PWM, according to https://github.com/raspberrypi/linux/issues/1983
edit _/etc/udev/rules.d/99-com.rules_ and add
```
SUBSYSTEM=="pwm*", PROGRAM="/bin/sh -c '\
        chown -R root:gpio /sys/class/pwm && chmod -R 770 /sys/class/pwm;\
        chown -R root:gpio /sys/devices/platform/soc/*.pwm/pwm/pwmchip* && chmod -R 770 /sys/devices/platform/soc/*.pwm/pwm/pwmchip*\
'"
```