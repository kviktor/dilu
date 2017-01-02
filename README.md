# DILU - Django Import LookUp

Easy way to search for Django functions or classes.


## Installation

On Ubuntu/Debian install the required packages
(python3-dev for uWSGI, the others for [GeoDjango](https://docs.djangoproject.com/en/1.10/ref/contrib/gis/install/geolibs/)),
then clone the repository, create a virtualenv, install the required Python libraries, create the database and 
finally run `import.sh` to collect the function/class names and import them into the database.

```sh
sudo apt-get install python3-dev binutils libproj-dev gdal-bin
git clone git@github.com:kviktor/dilu.git
cd dilu
mkvirtualenv dilu -p /usr/bin/python3
pip install -r requirements.txt
cd dilu
./manage.py migrate
./import.sh
```

## Known issues

* wrong line numbers and code for wrapped functions
* the shortest import path is not always the best import path
* no tests
* the documentation links are kinda meh
