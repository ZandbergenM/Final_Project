#!/usr/bin/env python
# coding: utf-8

# In[146]:


import pandas as pd
import matplotlib.pyplot as plt
from pprint import pprint
get_ipython().run_line_magic('matplotlib', 'inline')

from arcgis.gis import GIS
from arcgis.geocoding import geocode
from arcgis.features import Feature, FeatureLayer, FeatureSet, GeoAccessor, GeoSeriesAccessor
from arcgis.features import SpatialDataFrame
from arcgis.geometry import Geometry, Point
from arcgis.geometry.functions import buffer


# In[147]:


gis = GIS("https://www.arcgis.com", "XXXXXX", "XXXXXX") 
#Log into arcgis with username and password


# In[148]:


gis


# ## Read and create DF from CSV file in previous Notebook

# In[149]:


prop_list_df = pd.read_csv(r'C:\Users\zandb\OneDrive\Documents\Northeastern\Classwork\GIS 6345 Geospatial Programming\Final Project\Data\houses_for_sale_filtered_my_criteria.csv')
prop_list_df.shape #91 potential properties that meet criteria from previous notebook


# In[150]:


prop_list_df.columns
#Need to change "STATE or PROVINCE" to "STATE". I manually changed in excel file created in notebook part 2


# In[151]:


prop_list_df = pd.DataFrame.spatial.from_xy(prop_list_df, 'LONGITUDE','LATITUDE')
type(prop_list_df)
#created a spatial data frame


# ## Geocode and Symbols

# In[152]:


#testing geocode and symbols on 1 property
prop1 = prop_list_df[prop_list_df['MLS']==1619623]
prop1


# In[255]:


#Handy website to create symbols http://esri.github.io/arcgis-python-api/tools/symbol.html
house_symbol = {"angle":0,"xoffset":12,"yoffset":12,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/Basic/RedFlag.png","contentType":"image/png","width":24,"height":24}
grocery_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/Shopping.png","contentType":"image/png","width":24,"height":24}
coffee_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/Coffee.png","contentType":"image/png","width":24,"height":24}
restaurant_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/Dining.png","contentType":"image/png","width":24,"height":24}
bar_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/Pub.png","contentType":"image/png","width":24,"height":24}
transportation_symbol =  {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/Transportation/esriDefaultMarker_191_Black.png","contentType":"image/png","width":24,"height":24}
parks_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/OutdoorRecreation/Park.png","contentType":"image/png","width":24,"height":24}
shops_symbol = {"angle":0,"xoffset":0,"yoffset":0,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/PeoplePlaces/DepartmentStore.png","contentType":"image/png","width":24,"height":24}
destination_symbol = {"angle":0,"xoffset":0,"yoffset":12,"type":"esriPMS","url":"http://static.arcgis.com/images/Symbols/Basic/RedStickpin.png","contentType":"image/png","width":24,"height":24}
fill_symbol = {"type": "esriSFS","style": "esriSFSNull",
               "outline":{"color": [255,0,0,255]}}

fill_symbol2 = {"type": "esriSFS","style": "esriSFSNull",
               "outline":{"color": [0,0,0,255]}}


# ## 1.5 mile extent around test property

# In[154]:


paddress = prop1.ADDRESS + ", " + prop1.CITY + ", " + prop1.STATE
prop_geom_fset = geocode(paddress.values[0], as_featureset=True)
#Property address turned into a feature set


# In[155]:


prop_geom = prop_geom_fset.features[0]
prop_geom
#geometry of featureset, use WKID for spatial reference


# In[156]:


prop_geom.attributes


# In[238]:


prop_geom = prop_geom_fset.features[0]
prop_buffer = buffer([prop_geom.geometry], 
                     in_sr = 4326, buffer_sr=4326,
                     distances= 1.5, unit=9035)[0]
#in_sr = WKID WGS 84, unit 9035 = miles

prop_buffer_f = Feature(geometry=prop_buffer)
prop_buffer_fset = FeatureSet([prop_buffer_f])
#Turn buffer into featureset


# In[256]:


prop_buffer.extent #extent of buffer around property in Seattle


# ## Create Dictionary for Geocoded features

# In[220]:


neighborhood_data_dict = {}
#Use https://developers.arcgis.com/rest/geocode/api-reference/geocoding-category-filtering.htm#GUID-20D9858C-C27C-4C9C-BE4C-1EDB36E04D62 
# categories for Geocoding


# In[233]:





# In[240]:


groceries = geocode('groceries', search_extent=prop_buffer.extent, out_sr = 4326,
                    max_locations=20, as_featureset=True)
neighborhood_data_dict['groceries'] = []

for place in groceries:
    sea_map2.draw(place.geometry, symbol=grocery_symbol)
    neighborhood_data_dict['groceries'].append(place.attributes['PlaceName'])


# In[252]:


place


# In[258]:


groceries.features


# In[163]:


sea_map2 = gis.map('Seattle, WA')
sea_map2.basemap='gray'
sea_map2


# In[164]:


sea_map2.draw(prop_buffer_fset, symbol=fill_symbol2)
sea_map2.draw(prop_geom_fset, symbol=house_symbol)


# In[165]:


restaurants = geocode('Food', search_extent = prop_buffer.extent, max_locations=20)
neighborhood_data_dict['restaurants'] = []


# In[166]:


coffees = geocode('coffee', category = 'Coffee Shop', search_extent=prop_buffer.extent, max_locations=10)
neighborhood_data_dict['coffees'] = []


# In[167]:


bars = geocode('bar', category = 'Bar or Pub', search_extent=prop_buffer.extent, max_locations=10)
neighborhood_data_dict['bars'] = []


# In[168]:


shops_service = geocode("store", category='Shops and Service', search_extent=prop_buffer.extent, max_locations=25)
neighborhood_data_dict['shops'] = []


# In[169]:


transport = geocode("Bus Station" or "Metro Station", category='Travel and Transport', search_extent=prop_buffer.extent, max_locations=20)
neighborhood_data_dict['transport'] = []


# In[170]:


parks = geocode("Park",category='Parks and Outdoors', search_extent=prop_buffer.extent, max_locations=20)
neighborhood_data_dict['parks'] = []


# In[259]:



neighborhood_df = pd.DataFrame.from_dict(neighborhood_data_dict, orient='index')
neighborhood_df = neighborhood_df.transpose()
neighborhood_df


# In[254]:


neighborhood_df.count().plot(kind = 'bar')
plt.title('Facilities within 1.5 miles of {}'.format(prop1.ADDRESS.values[0]))


# In[199]:


neighborhood_data_dict.keys()


# In[200]:


neighborhood_data_dict.get('groceries')


# In[ ]:




