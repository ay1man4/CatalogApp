# Catalog App

Catalog App is a website application which can be used to create catalog for any categorized items. It gives the ability to add, edit and delete items under each category.

## Install

Before using this script, you have to prepare the website environment and install required softwares. This illustration showing how to use VM environment using vagrant. Follow below steps to prepare the environment and DB:

- Install [vagrant](https://www.vagrantup.com/downloads.html) and [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
- Download and unzip the VM configuration [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip)
- Change terminal directory to vagrant directory inside unzipped directory
- Start the virtual Machine using `vagrant up`
- Once done run `vagrant ssh` to log into linux environment
- This website is running with sqlite3, but it can run with any DB by changing the DB engine in database_setup.py
- If DB engine changed, you have to create the DB before using the app
- You may start with demo Catagories using command `python3 seeder.py`

## Usage

In VM terminal run the website using below command:
`python3 application.py`

Items creation, edition and deletion can be accomplished by the website as well as json. Since website is self explanatory, below guide will emphasis JSON part only:

- **Show Categories**: `GET /api/v1/catalog.json`
- **Show One Category**: `GET /api/v1/catalog/<category>/items.json`, *category* is the name of category
- **Show One Item**: `GET /api/v1/catalog/<category>/<item>`, *category* and *item* are the name of category and item
- **Create New Category**: `POST /api/v1/catalog/category/new`, make sure to include category name in the body
- **Create New Item**: `POST /api/v1/catalog/<category>/new`, *category* is the name of category. Also, make sure to include item name and description in the body.
- **Edit Item**: `POST /api/v1/catalog/<category>/<item>/edit`, *category* and *item* are the name of category and item. Also, make sure to include new item name, description and category in the body
- **Delete Item**: `POST /api/v1/catalog/<category>/<item>/delete`, *category* is the name of category. Warning: deletion is not reversible.

## Deployment

App have been deployed in Amazon Lightsail server. It can be accessed using the following info:
- **IP address**: http://54.91.177.105
- **URL**: http://54.91.177.105.xip.io

Below is the list libraries installed in venv to run the App:
- Flask==1.0.2
- Flask-Migrate==2.3.1
- Flask-SQLAlchemy==2.3.2
- Flask-Testing==0.7.1
- httplib2==0.12.0
- oauth2client==4.1.3
- psycopg2-binary==2.7.6.1
- requests==2.21.0
- SQLAlchemy==1.2.15

## Server Configuration

Below are the main steps used to configure the server:
- Keep All system packages updated `sudo apt-get update && sudo apt-get upgrade`, if some packages still not updated, use `sudo apt-get update && sudo apt-get dist-upgrade`
- Prohibit remote root login by setting `PermitRootLogin no` in `/etc/ssh/sshd_config`
- Create new user using command `adduser` for example `adduser grader`
- Add created to sudoers by adding `grader ALL=(ALL) ALL` to `/etc/sudoers.d`
- **Configure ssh key authentication using the following steps**:
    - Create ssh key pairs in local machine, in windows, PUTTYgen software can be used.
    - Create .ssh directory in user home `mkdir ~/.ssh`
    - Inside .ssh create authorized_keys file using `touch ~/.ssh/authorized_keys` and copy public key into it
    - Secure the ssh directory and keys using `chmod 700 ~/.ssh` and `chmod 644 ~/.ssh/authorized_keys`
- Disable Password authentication by setting `PasswordAuthentication no` in `/etc/ssh/sshd_config`
- **Configure firewall using the following steps**:
    - Make sure the status is `inactive` using `sudo uwf status`
    - Deny all incoming `sudo uwf default deny incoming`
    - All all outgoing `sudo uwf default allow outgoing`
    - Allow SSH on default port `sudo uwf allow ssh`. It will be removed later.
    - Allow SSH on non-default port `sudo uwf allow 2200/tcp`
    - Allow Http on default port `sudo uwf allow www`
    - Allow NTP on port 123 `sudo uwf allow 123`
    - Enable firewall `sudo ufw enable`
    - Make sure to configure ssh to use non-default port by change and un-comment `# port 22` in `/etc/ssh/sshd_config` to `port 2200`
    - Restart ssh service to `service sshd restart`
    - Remove default ssh port rule by knowing it's number `sudo ufw status numbered` then `sudo ufw delete 3` where 3 here is the ssh rule
- Install webserver (Apache2) using `sudo apt-get apache2`
- Install mod_wsgi `pip install mod_wsgi`
- Configure Virtual Environment `pyvenv ~/venv/CatalogApp`
- Activate CatalogApp venv using `source ~/venv/CatalogApp/bin/activate`
- Clone project from github `git clone https://github.com/ay1man4/CatalogApp.git`
- Install required libraries in virtual environment `pip install -r ~/projects/CatalogApp/requirements.txt`
- Deactivate virtual environment `deactivate`
- **Setup Apache2 website config file and wsgi file using the following steps**:
    - Create config file `sudo touch /etc/apache2/sites-available/catalog.config`
    - Configure the virtual host and make sure to add wsgi configuration correctly specially below lines:
        - `WSGIDaemonProcess catalog python-home=/home/ayman/venv/CatalogApp user=ayman group=ayman threads=5`
        - `WSGIScriptAlias / /home/ayman/projects/CatalogApp/app.wsgi`
        - `Alias /static /home/ayman/projects/CatalogApp/app/static`
    - Activate config file `sudo a2ensite catalog.conf`
    - Setup wsgi file `sudo touch /home/ayman/projects/CatalogApp/app.wsgi`
    - Make sure to add the following lines to wsgi file:
        - `sys.path.insert(0, '/home/ayman/projects/CatalogApp')`
        - `from run import app as application`
    - Restart Apache server `sudo systemctl restart apache2`
    - Make sure it is working `sudo systemctl status apache2`

## Third party softwares:

Multiple third party softwares used in this project. Main softwares used listed below. However, more libraries have been used which already mentioned above:
- SSH configuration and sever ssh login: PUTTY, PUTTYgen, Pageant
- Virtual Box: configure test server before publishing on live server
- Visual Studio Code: used as code editor and git terminal
- GitHub: to host the code
- Amazon Lightsail: webserver to host the project


## Resources and References:

Multiple threads have been read to accomplish the project, below are the main pages:
- Updating System Packages: https://serverfault.com/questions/265410/ubuntu-server-message-says-packages-can-be-updated-but-apt-get-does-not-update
- Change Default SSH Port: https://www.godaddy.com/help/changing-the-ssh-port-for-your-linux-server-7306
- Flask Project Layout and strucure: 
    - http://flask.pocoo.org
    - http://flask-sqlalchemy.pocoo.org/2.3/
    - https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-one
    - https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-two
    - https://scotch.io/tutorials/build-a-crud-web-app-with-python-and-flask-part-three

## License

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

For more details, please refer to LICENSE file shipped with project.