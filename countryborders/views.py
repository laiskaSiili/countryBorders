# -*- coding: UTF-8 -*-

from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import CountryForm


####################
# COUNTRY TEST SETUP
####################

# FROM https://stackoverflow.com/questions/25428512/draw-a-map-of-a-specific-country-with-cartopy
# AND FROM http://deeplearning.lipingyang.org/2018/07/21/django-sending-matplotlib-generated-figure-to-django-web-app/
from cartopy.io import shapereader
import geopandas
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from io import BytesIO
import urllib, base64

# get country borders from natural earth data (http://www.naturalearthdata.com/)
resolution = '10m'
category = 'cultural'
name = 'admin_0_countries'
shpfilename = shapereader.natural_earth(resolution, category, name)
# read the shapefile using geopandas
DF = geopandas.read_file(shpfilename)
# create choices tuples for dropdown
CHOICES = [(x, x) for x in DF['ADMIN'].sort_values().values]


class DrawCountry(View):

    def get(self, request, country='Germany'):
        # ge country borders
        poly = DF.loc[DF['ADMIN'] == country]['geometry'].values[0]
        # extract bounding box
        bbox = poly.bounds
        # add_geometries seems to expect nested data (multipolygons)
        if str(poly).startswith('POLYGON'):
            poly = [poly]
        # plot and set extent
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.add_geometries(poly, crs=ccrs.PlateCarree(), facecolor='none', edgecolor='0.5')
        ax.set_extent([bbox[0],bbox[2],bbox[1],bbox[3]], crs=ccrs.PlateCarree())
        # create base64 uri as image source in html
        buf = BytesIO()
        plt.savefig(buf, format='png', dpi=300)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
        # close buffer and also close plot
        buf.close()
        plt.close()

        # create form and fill contex context 
        ctx ={}
        ctx['image_base64'] = image_base64
        form = CountryForm()
        form.fields['country'].choices = CHOICES
        form.fields['country'].initial = country
        ctx['form'] = form
        return render(request, 'countryborders/country.html', ctx)