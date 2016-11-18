## How to install MySQL on Ubuntu ##

pip install MySQL-python, sqlalchemy

apt-get -y install mysql-server
* Use root password gpscontrol
apt-get -y install mysql-client

CREATE USER 'gpscontrol'@'localhost' IDENTIFIED BY 'qazwsxedc';
GRANT ALL PRIVILEGES ON * . * TO 'gpscontrol'@'localhost';