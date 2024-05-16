#!/usr/bin/env bash
#sets up  web servers for the deployment of web_static

#Install Nginx if it not already installed
apt-get install -y nginx
#create necessary directories
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

#recursivery Give ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu: /data/

#create a file with some contents in test directory
sudo touch /data/web_static/releases/test/index.html

echo "
<html>
   <head>
   </head>
   <body>
     Holberton School
   </body>
</html>" > /data/web_static/releases/test/index.html

#create a symbolic link with of test directory with current directory
sudo ln -s /data/web_static/releases/test/  /data/web_static/current

#add a location block for /hbnb_static in sites-available/default file
sudo sed -i '/server_name _;/a\\tlocation \/hbnb_static {\n\t\talias \/data\/web_static\/current;\n\t}' /etc/nginx/sites-available/default

sudo rm /etc/nginx/sites-enabled/default

sudo ln -s /etc/nginx/sites-available/default  /etc/nginx/sites-enabled/

sudo nginx -t

service nginx reload
