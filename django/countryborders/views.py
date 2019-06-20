# -*- coding: UTF-8 -*-

from django.views import View
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from .forms import CountryForm

import geopandas as gpd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import urllib, base64


class DrawCountry(View):

    NUM_CITIES = 5
    DF_COUNTRIES = gpd.read_file('countryborders/data/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp')
    DF_POP_PLACES = gpd.read_file('countryborders/data/ne_10m_populated_places/ne_10m_populated_places.shp')

    def get(self, request):
        ctx = {}
        ctx['form'] = CountryForm()
        return render(request, 'countryborders/country.html', ctx)

    def post(self, request):
        ctx = {}
        form = CountryForm(request.POST)
        if form.is_valid():
            country_name = form.cleaned_data['country']
            coordinate_system = form.cleaned_data['coordinate_system']
            # select country from dataframe and also get 5 most populated places for country
            if country_name == 'World':
                country = DrawCountry.DF_COUNTRIES.copy()
                country_cities_top5 = DrawCountry.DF_POP_PLACES.copy().sort_values(by=['POP_MAX'], ascending=False).head(DrawCountry.NUM_CITIES)
            else:
                country = DrawCountry.DF_COUNTRIES[DrawCountry.DF_COUNTRIES['ADMIN'] == country_name].copy()
                country_cities_top5 = DrawCountry.DF_POP_PLACES[(DrawCountry.DF_POP_PLACES['ADM0NAME']==country_name)].copy().sort_values(by=['POP_MAX'], ascending=False).head(DrawCountry.NUM_CITIES)
            
            # Reproject data according to projection form field
            country = country.to_crs(epsg=coordinate_system)
            country_cities_top5 = country_cities_top5.to_crs(epsg=coordinate_system)
            
            # if show_largest_only checked, replace geometry with largest polygon
            if form.cleaned_data['show_largest_only']:
                try:
                    max_area = 0
                    for multipoly in country.geometry:
                        for poly in multipoly:
                            if poly.area > max_area:
                                largest_poly = poly
                                max_area = poly.area
                    country['geometry'] = largest_poly
                    country_cities_top5 = country_cities_top5[country_cities_top5.intersects(largest_poly)]
                except TypeError:
                    pass

            # overlay with different markersizes corresponding to the population sizes.
            def get_markersizes(dataseries, min_markersize, max_markersize):
                min_data = dataseries.min()
                max_data = dataseries.max()
                return [(v - min_data) / (max_data - min_data) * (max_markersize - min_markersize) + min_markersize for v in dataseries]
            markersizes = get_markersizes(country_cities_top5['POP_MAX'], 40, 400)

            fig, ax = plt.subplots()
            ax.set_axis_off()
            country.plot(ax=ax, color='lightgrey', edgecolor='black')
            # only attempt to plot markers if any exists at all
            if country_cities_top5.shape[0] > 0:
                gpd.plotting.plot_point_collection(ax, country_cities_top5['geometry'], color='red', markersize=markersizes)

            # create base64 uri as image source in html
            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=300)
            image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
            buf.close()
            plt.close()

            ctx['image_base64'] = image_base64

        ctx['form'] = form
        return render(request, 'countryborders/country.html', ctx)