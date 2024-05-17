#!/usr/bin/env bash
#sets up  web servers for the deployment of web_static

#Install Nginx if not already installed
sudo apt-get install -y nginx

#create directories
sudo mkdir  /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

echo "
<html>
   <head>
   </head>
   <body>
     Holberton School
   </body>
</html>" > /data/web_static/releases/test/index.html

if [ -L /data/web_static/current ]; then
	sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/  /data/web_static/current

#recursivery Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu: /data/

#add a location block for /hbnb_static in sites-available/default file
sudo sed -i '/server_name _;/a\\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}' /etc/nginx/sites-available/default

if [ -L /etc/nginx/sites-enabled/default ]; then
	sudo rm /etc/nginx/sites-enabled/default
fi

sudo ln -s /etc/nginx/sites-available/default  /etc/nginx/sites-enabled/

sudo nginx -t

sudo service nginx reload
