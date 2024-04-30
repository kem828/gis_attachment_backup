# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 06:29:25 2024

@author: 388560
"""

from arcgis.gis import GIS
from arcgis import features
from arcgis.features import FeatureLayerCollection
import arcpy
import pathlib
from datetime import date
import asyncio
import requests
import pandas as pd
import getpass


def generate_gis_object(username = '', password = '', portal = 'https://www.arcgis.com', manual_retry = True):
    """ Get GIS Object from portal
    
    Args:
        username (str): username credentials used to login to portal
        password (str): password creentials for passed user
        portal (str): portal url of hosted data
        manual_retry (bool): bool to denote if user will enter credentials manually if connection fails
        
    Returns:
        gis (GIS object): esri portal connection object used for arcgis api for python
    """
    try:
        gis = GIS(url = portal, username = username, password = password)
    except:
        if manual_retry is True:
            print('Failed to login to portal, please enter Username and Password')
            username = input('Username:')
            password = getpass.getpass('Password:')
        else:
            pass
    return gis

    
def get_layer(itemid, gis, layer_index = 0, table = False):
    """ Get featureset object of specified layer with optional query
    
    Args:
        layer_index (int): the index of the layer you are querying. Might need to experiment to identify
        the relevant layer, as service indexes are not 1:1 with layer indexes
        table (bool): whether or not the layer in question is a table. Different i/o options for tables (for no reason mostly!)
        query_str (str): optional sql query to pass to service to retrieve only a subset
        itemid (str): the portal item id of the hosted feature layer being retrieved
        gis (GIS): esri portal connection object used for arcgis api for python
        
    Returns:
        list including:
        fs (featureset): esri featureset object. This is the json with layer metadata and attributes used
        in many esri services. Note that this is an arcgis api for python fs objct, not an arcpy fs! Although there is a
        conversion function available https://developers.arcgis.com/python/api-reference/arcgis.features.toc.html#featureset
        name (str): string of the layer name, used for saving
    """
    
    feature_layer = gis.content.get(itemid)
    if table is False:
        layer = feature_layer.layers[layer_index]
    else:
        layer = feature_layer.tables[layer_index]
        
    
    name = layer.properties['name']
    #fs = layer.query(where=query_str)
    
    return layer


def fetch_and_save_attachment(attachment, save_path):
    """ gets information from attachment manager and saves file to relevant path
    
    Args:
        attachment (dict): attachment information from attachment manager
        save_path (str): base backup folder to save image
        
        """
    record_id = attachment['PARENTOBJECTID']
    attachment_id = attachment['ID']
    name = attachment['NAME']
    image_url = attachment['DOWNLOAD_URL']
    image_save_path = f'{save_path}/{record_id}/{attachment_id}'
    image_path = pathlib.Path(image_save_path)
    image_path.mkdir(parents=True, exist_ok=True)
    img_data = requests.get(image_url).content
    with open(f'{image_path}/{name}', 'wb') as handler:
        handler.write(img_data)

def backup_feature_layer(save_path, fs, gdb_name, name):
    """ Makes sure local path\gdb exists, then save the feature layer without attachments
    
    Args:
        save_path (str): base backup folder featurer layer
        fs (featureset object): feature set that is being saved
        gdb_name (str): name of gdb to save backup to
        name (str): name of featureclass to save in gdb
        
        """
    path = pathlib.Path(save_path)
    if arcpy.Exists(rf'{save_path}/{gdb_name}'):
        fs.save(rf'{save_path}/{gdb_name}',name)
    else:
        path.mkdir(parents=True, exist_ok=True)
        #In classic esri fashion, path vars dont work, just strings
        arcpy.management.CreateFileGDB(save_path, gdb_name)
        fs.save(rf'{save_path}/{gdb_name}',name)

'''
Configuration below
Presumably this is to be stored in an external config file
Or as notebook parameters depending on use case

Can easily be changed when that is the case


    Args:
        fs_list (list): a list of objects containing per feature layer configuration information.
        This is the list of layers that will be exported
        Contains one or more objects as documented below as out_layer:
            out_layer (dict) : object in fs_list:
                layer_index (int): the index of the layer you are querying. Might need to experiment to identify
                the relevant layer, as service indexes are not 1:1 with layer indexes
                table (bool): whether or not the layer in question is a table. Different i/o options for tables (for no reason mostly!)
                query_str (str): optional sql query to pass to service to retrieve only a subset
                itemid (str): the portal item id of the hosted feature layer being retrieved
                gis (GIS): esri portal connection object used for arcgis api for python
        
        username (str): username credentials used to login to portal
        password (str): password creentials for passed user
        portal (str): portal url of hosted data
        manual_retry (bool): bool to denote if user will enter credentials manually if connection fails
        save_path (str): root folder to save the relevant data
        gdb_name (str): name of gdb to save feature set to
        add_date_to_path (bool): save everything in a subset of the save+path using todays date
        arcpy.env.overwriteOutput (bool): do you want to overwrite if it exists? no actual error handling if it is no....
'''
##
###BEGIN CONFIG

#credentials
username = 'USERNAME'
password = 'PASSWORD'
portal = 'https://www.arcgis.com'
manual_retry = True

#feature service information
fs_list = [{'itemid' : '017b7a572ff94943b867ace0cba0950e',
            'layer_index' : 0,
            'query_str' : "CreationDate >= date '2022-05-02' and CreationDate < date '2022-05-03'",
            'table' : False,
            'oid_field' : 'OBJECTID'}]

#output information (currently just paths, would need to add module for other save methods)
save_path = 'C:/Test/cleanstat_backup'
gdb_name = 'cleanstat.gdb'
add_date_to_path = True
output_excel_name = 'attachments.xlsx'


#As far as I can tell, this is the method to change the over write environment var for arcgis api for python
#Which means it is inaccessible when arcpy is not licensed?!
#Seems like an oversight unless there is a separate environment\method Im missing
arcpy.env.overwriteOutput = True
###END CONFIG
##

gis = generate_gis_object(username = username, password = password, portal = portal, manual_retry = manual_retry)

if add_date_to_path is True:
    today = date.today()
    save_path += f"/{today.strftime('%m_%d_%Y')}"



for out_layer in fs_list:
    attachment_list = []
    oid_list = []
    failed_oid_list = []
    layer = get_layer(itemid = out_layer['itemid'], 
                             gis = gis,
                             layer_index = out_layer['layer_index'], 
                             table = out_layer['table'])
    
    
    fs = layer.query(where=out_layer['query_str'])
    name = layer.properties['name']

    for feature in fs:
        oid_list.append(feature.attributes[out_layer['oid_field']])
    
    backup_feature_layer(save_path, fs, gdb_name, name)

    am = features.managers.AttachmentManager(layer)
    attachments = am.search(object_ids = oid_list, return_url = True) 
        
    for attachment in attachments:
        attachment_list.append(attachment)
        fetch_and_save_attachment(attachment, save_path)
    
    df_out = pd.DataFrame(attachment_list)
    df_out.to_excel(f'{save_path}/{output_excel_name}')
        
        
