# Country Borders

A barebone django app showcasing a specific usecase of pulling country borders from naturalearthdata, rendering them serverside in matplotlib and displaying them on a website. 

## Installation
- Install dependencies according using requirements.txt. On Windows using Miniconda is recommended due to dependencies such as geopandas and cartopy.
- **Important:** After installing modules, uninstall shapely and reinstall using *pip install --no-binary :all: shapely* [See github discussion here](https://github.com/SciTools/cartopy/issues/879)
- In the project folder, run *python manage.py runserver* and go to localhost:8000
