# Country Borders

A barebone jupyter notebook and django app showcasing a specific usecase of reading country borders from a downloaded shapefile from naturalearthdata. It is shown how to read, reproject, manipulate the data, as well as how to overlay with additional dataset. The django app showcases how to render a the resulting plot serverside in matplotlib and displaying them on a website. 

## Installation
- Create and enter a new virtual environment using requirements.txt. On Windows using Miniconda is recommended due to dependencies such as geopandas.
- In the jupyter project folder, run *ipython kernel install --user --name=YOUR_VIRTUAL_ENV_NAME* to add a kernel a then run notebook with *jupyter notebook*
- In the django project folder, run *python manage.py runserver* and go to localhost:8000
