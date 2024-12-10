# gis_attachment_backup
<div id="top"></div>




<!-- ABOUT THE PROJECT -->
## About The Project


This is a script\notebook saves a hosted feature layer locally, in addition to extracting and saving all attachments



### Prerequisites


* ArcGIS Pro\ArcGIS Enterprise python environment

Tested on Pro Environment 3.1.0\ Enterprise 11.1


<p align="right">(<a href="#top">back to top</a>)</p>



## Configuration
Args:

fs_list (list): 
a list of objects containing per feature layer configuration information.
This is the list of layers that will be exported
Contains one or more objects as documented below as out_layer:

            out_layer (dict) : object in fs_list:
            layer_index (int): the index of the layer you are querying. Might need to experiment to identify
            the relevant layer, as service indexes are not 1:1 with layer indexes
            table (bool): whether or not the layer in question is a table. Different i/o options for tables (for no reason mostly!)
            query_str (str): optional sql query to pass to service to retrieve only a subset
            itemid (str): the portal item id of the hosted feature layer being retrieved
            gis (GIS): esri portal connection object used for arcgis api for python
            oid_field (str): The field in the feature layer designated as the oid. case sensitive (not the alias!)
            attach_to_gdb (bool) : True -> attach all exported attachments as blob in the relevant gdb layer\table, False-> Don't

environment specific:

            username (str): username credentials used to login to portal
            password (str): password credentials for passed user
            portal (str): portal url of hosted data
            manual_retry (bool): bool to denote if user will enter credentials manually if connection fails
            save_path (str): root folder to save the relevant data
            gdb_name (str): name of gdb to save feature set to
            add_date_to_path (bool): save everything in a subset of the save+path using todays date
            check_count (int): print the status after every x saves
            arcpy.env.overwriteOutput (bool): do you want to overwrite if it exists? no actual error handling if it is no....

<!-- USAGE EXAMPLES -->
## Usage

set relevant configuration in script:

#credentials


username = 'USERNAME'

password = 'PASSWORD'

portal = 'https://www.arcgis.com'

manual_retry = True


#feature service information


fs_list = [{'itemid' : 'itemidstring!',
            'layer_index' : 0,
            'query_str' : "CreationDate >= date '2022-05-02' and CreationDate < date '2022-05-03'",
            'table' : False,
            'oid_field' : 'OBJECTID',
            'attach_to_gdb' : True}]

#output information (currently just paths, would need to add module for other save methods)


save_path = 'C:/PATH/TO/FOLDER'

gdb_name = 'LOCAL_GDB_NAME.gdb'

add_date_to_path = True



configration vars are documented in script
(Presumably these would be set in external config, as tool params or as notebook schedule params)
I'll write that when we know which


<!-- CONTACT -->
## Contact

Keinan Marks -  keinan@keinanmarks.com


<p align="right">(<a href="#top">back to top</a>)</p>


