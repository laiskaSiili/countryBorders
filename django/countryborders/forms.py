from django import forms
import geopandas as gpd

class CountryForm(forms.Form):
    COUNTRIES = [('World', 'World')]
    COUNTRIES += [(x,x) for x in gpd.read_file('countryborders/data/ne_50m_admin_0_countries/ne_50m_admin_0_countries.shp')['ADMIN'].sort_values()]
    CS = (
        (4326, 'WGS84 (4326, geographic)'), 
        (3857, 'Pseudo Mercator (3857, projected)'),
        (2163, 'National Atlas Equal Area (2163, projected)')
    )

    show_largest_only = forms.BooleanField(required=False, initial=True, widget=forms.CheckboxInput(attrs={'onchange': 'countryform.submit();'}))
    coordinate_system = forms.ChoiceField(required=False, initial=CS[0][0], choices=CS, widget=forms.RadioSelect(attrs={'onchange': 'countryform.submit();'}))
    country = forms.ChoiceField(choices=COUNTRIES, widget=forms.Select(attrs={'onchange': 'countryform.submit();'}))