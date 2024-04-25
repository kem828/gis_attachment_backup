# json_service_to_feature_service
<div id="top"></div>




<!-- ABOUT THE PROJECT -->
## About The Project


This is a simple script saves a hosted feature layer locally, in addition to extracting and saving all attachments



### Prerequisites


* ArcGIS Pro\ArcGIS Enterprise python environment

Tested on Pro Environment 3.1.0\ Enterprise 11.1


<p align="right">(<a href="#top">back to top</a>)</p>



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
            'oid_field' : 'OBJECTID'}]

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


