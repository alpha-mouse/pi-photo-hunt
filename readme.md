https://michael.lustfield.net/nginx/bottle-uwsgi-nginx-quickstart

pip3 install bottle
apt-get install uwsgi uwsgi-plugin-python3 python3-bottle nginx

create /var/www/photo_hunt/photos and edit main.py->config['photos_directory']
chmod 777 /var/www/photo_hunt/photos

usermod -aG video www-data

sudo ln -sf /etc/uwsgi/apps-available/photo_hunt.ini /etc/uwsgi/apps-enabled/photo_hunt.ini
sudo ln -sf /etc/nginx/sites-available/photo_hunt /etc/nginx/sites-enabled/default
sudo service uwsgi restart
sudo service nginx restart
