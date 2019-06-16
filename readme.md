https://www.raspberrypi.org/forums/viewtopic.php?t=197513

```
pip3 install bottle
apt-get install python3-bottle nginx

mkdir ~/Documents/Work
cd ~/Documents/Work
git clone --depth=1 https://github.com/alpha-mouse/pi-photo-hunt.git
cd pi-photo-hunt
mkdir photos
//? chmod 777 photos
chmod +x main.py

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