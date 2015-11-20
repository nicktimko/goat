# Provisioning

## Aptitude Packages

* git
* nginx
* python3
* python3-pip

Copy:

    sudo apt-get install -qqy git nginx python3 python3-pip

## Pip Packages

* virtualenv
* requirements.txt (install under a created virtual environment located as below)

Copy:

    sudo pip3 install virtualenv
    
## Folder structure
Assume we have a user account at `/home/username`

    /home/username
    └── sites
        └── SITENAME
             ├── database
             ├── source
             ├── static
             └── virtualenv

## Configuration

1. Copy `nginx-site` to `/etc/nginx/sites-available` and tweak names/paths as needed
1. Link to `sites-enabled` (`ln -s /etc/nginx/sites-available/<name> /etc/nginx/sites-enabled/<name>`)
1. Copy `upstart.conf` to `/etc/init/<taskname>.conf` and tweak
