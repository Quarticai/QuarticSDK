===================
Basic Functionality
===================

This article explains the various classes of Quartic SDK along with their methods and
available attributes.

===============
GraphQL Client
===============

GraphQLClient
------------

Class refers to the Graphql client which is used as the interface between
the user querying the Quartic AI Platform and their use case.

This class has the following parameters for initialization:

-  **url (mandatory)**: Refers to the host URL the user connects to for
   making API calls.
-  **username (optional)**: Required for Basic Authentication.
-  **password (optional)**: Required for Basic Authentication.
-  **token (optional)**: Required for OAuth2.0 Authentication.
-  **ssl (optional)**: Required when the host needs to be
   verified for SSL.
- **timeout (optional)**: Required if the user wants to specify timeout for API calls.

Here's an example:

::

    client = GraphqlClient(url='https://stag.quartic.ai', username="username", password="password")

The two methods are Basic Authentication and OAuth2.0:
*****************************************************

Basic Authentication:
~~~~~~~~~~~~~~~~~~~~

The user must pass the username and password along with the hostname in the GraphqlClient
to ensure the successive API calls are authenticated via Basic Authentication.

::

    client = GraphqlClient(host="https://test.quartic.ai", username="username", password="password")

OAuth2.0
~~~~~~~~

The user must pass the OAuth token along with the hostname to ensure that all the
successive API calls are authenticated via OAuth2.0. For detailed information on fetching
tokens, please refer to the Quartic Knowledge Base.

::

    client = GraphqlClient(url="https://test.quartic.ai", oauth_token="9865c994212e495690c2db3fc6cbdfea")



The available methods are as follows:
*************************************

.version
~~~~~~~~

This method returns the current version of the package.

::

    client.version() # Returns 2.1.0 as of the time of writing this document

.execute_query
~~~~~~~~

This method executes the GraphQL query.

-  **query\_params (required)**: User needs to pass the string in the format given below:

::

    query='''
        query MyQuery {
          Site {
            id
            name
          }
        }'''

-  **variables\_params (optional)**: User can pass a dictionary of variables which are defined in the query in the format below.

::

    query = '''
        mutation($file: Upload!, $edge_connector: Int!, $date_format: DateTime!) {
            uploadTelemetryCsv(
                file: $file,
                fileName: "123",
                edgeConnector: $edge_connector,
                dateFormat: $date_format
                )
                {
                taskId
                status
            }
        }
    '''

    variables = {
        'file': open('<path/to/file>', 'rb'),
        'edge_connector': 'edgeConnector Id',
        'date_format': 'DatTime format'
    }


::

    client.execute_query(query, variables) # Returns a json response on a success.


===============
API Client
===============

Class refers to the API client which is used as the interface between
the user querying the Quartic AI Platform and their use case.

This class has the following parameters for initialization:

-  **host (mandatory)**: Refers to the host the user connects to for
   making API calls.
-  **username (optional)**: Required for Basic Authentication.
-  **password (optional)**: Required for Basic Authentication.
-  **oauth\_token (optional)**: Required for OAuth2.0 Authentication.
-  **verify\_ssl (optional)**: Required when the host needs to be
   verified for SSL.
-  **cert\_path (optional)**: Required for verification of SSL certificates for HTTPS requests.

Here's an example:

::

    client = APIClient(host="https://test.quartic.ai", username="username", password="password")

It can be noted that the class provides two methods of authentication to the user.

The two methods are BasicAuthentication and OAuth2.0:
*****************************************************

Basic Authentication:
~~~~~~~~~~~~~~~~~~~~

The user must pass the username and password along with the hostname in the APIClient
to ensure all the successive API calls are authenticated via Basic Authentication

::

    client = APIClient(host="https://test.quartic.ai", username="username", password="password")

OAuth2.0
~~~~~~~~

The user must pass the OAuth token along with the hostname to ensure that all the
successive API calls are authenticated via OAuth2.0. For the detailed information on fetching
tokens, please refer to the Global Settings article in the Quartic Knowledge Base.

::

    client = APIClient(host="https://test.quartic.ai", oauth_token="9865c994212e495690c2db3fc6cbdfea")

The available methods are as follows:
*************************************

.version
~~~~~~~~

This method returns the current version of the package.

::

    client.version() # Returns 0.0.0 as of the time of writing this document

.assets
~~~~~~~

This method returns the list of assets that the authenticated user has
access to. The list of assets are an object of type ``EntityList``. More
details on the class is provided below.

The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the Assets accordingly.
   Filter conditions can be like
|   ``{"created_at__gt": "2020-04-05 17:59:50.466338+00:00", "status": 1}``
    ``{"created_at__lt": "2021-04-05 17:59:50.466338", "status": 1}``

   Note : timestamps to be passed according to ISO 8610 format in query_params
::

    client_assets = client.assets()

.context_frames
~~~~~~~~~~~~~~~

This method returns the list of context frames which are created using the assets
that the user has access to. The list of context frames are an
object of type ``EntityList``. More details on the class is provided below.

The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the ContextFrame Occurrences accordingly.
   Filter conditions can be like
   ``{"start_ef_occurrence": "A3412", "stop_ef_occurrence": "C7415"}``

::

    client_context_frames = client.context_frames()

.tags
~~~~~

The method parameters as included in v2.0.0 are as follows:

**asset\_id (mandatory)**: The asset\_id of the asset whose tags are to
be returned.

**query\_params (optional)**: User can pass a dictionary of conditions
and condition values to filter the tags accordingly.
Filter conditions can be like
|``{"tag_type": 1, "edge_connector": 674}``

::

    tags_of_asset_id_1 = client.tags(1)

.edge_connectors
~~~~~~~~~~~~~~~~

This method returns the list of all the data sources which the user has access to.
The list of data sources are an object of type ``EntityList``. More details on the class
are provided below.

The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the Assets accordingly.
   Filter conditions can be like

   ``{"created_at__gt": "2020-04-05 17:59:50.466338+00:00", "connector_protocol": 206}``

   ``{"created_at__lt": "2020-04-05 17:59:50", "connector_protocol": 206}``

   ``{"updated_at__lt": "2020-04-05", "connector_protocol": 206}``

   Note : timestamps to be passed according to ISO 8610 format in query_params

::

    edge_connectors = client.edge_connectors()

.list\_models
~~~~~~~~~~~~~

This method lists the ML models and its parameters and requires the
following parameters to be called:

-  **is\_active (optional)**: If ``is_active`` is true, ``list_models``
   will list the models which are active in the Quartic AI Platform.
-  **ml\_node (optional)**: If ``ml_node`` (numeric field) is specified,
   ``list_models`` will list all the custom models that are deployed
   into a specific ml node.

.products
~~~~~~~~~~
This method is used to fetch list of all product belongs to a particular client.
The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the Products accordingly.
   Filter conditions can be like

   ``{"created_at__gt": "2020-04-05 14:19:38"}``

   Note : timestamps to be passed according to ISO 8610 format in query_params

::

    products = client.products()

.sites
~~~~~~~
This method is used to fetch all sites available for a user's client.
The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the Products accordingly.
   Filter conditions can be like

   ``{"start__gt": "2021-04-05 14:19:38", "stop__lt": "2021-04-06 11:19:38}``

::

    sites = client.sites()

Entity
---------

Entity is the parent term by which all the objects accessible in the SDK
are referred to. The available methods are as follows:

An object of this class is initialiazed with two parameters. These are
automatically created and depend on the user's query through the client.

-  **body\_json (mandatory)**: This is the json object which is used to
   create the related ``Entity`` object.
-  **api\_helper (mandatory)**: This is the APIHelper object which
   contains information about the authentication and is used for making
   API calls.

The available methods are as follows:
*************************************

get
~~~

The attribute value of the object is returned for the given name.

-  **name (mandatory)**: Refers to the attribute name whose value is to be returned.

Asset
--------

This refers to the asset entity which contains the details of the asset.
Asset contains all the properties of the base entity defined above.
When one prints the name of the asset object, the class returns the name along with the ID of the asset and the
template as `Asset: {asset_name}_{asset_id}`. The available attributes in the class are:

-  **id**: The ID of the asset
-  **name** : The name of the asset
-  **edge_connectors**: The datasource IDs whose tags belong to this asset
-  **last_overhaul_date**: The last overhaul date of the asset in epoch
-  **onboarded_at**: The onboarded at time of the asset in epoch
-  **created_at**: The created at time of the asset in epoch
-  **status**: The streaming status of the asset. They are given by:
.. list-table:: Asset streaming status
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 0
     - INIT
   * - 1
     - ACTIVE
   * - 2
     - PARTIAL_STREAMING
   * - 3
     - INACTIVE
   * - 4
     - UNASSIGNED_TAGS



The available methods are as follows:
*************************************

.get\_tags
~~~~~~~~~~

The method returns all the tags present in the given asset in the form
of ``EntityList`` where each object refers to ``Tag``.

The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the tags accordingly.
   Filter conditions can be like
|   ``{"tag_type": 1, "edge_connector": 674}``

.batches
~~~~~~~~

The method returns all the batches present in the given asset in the
form of ``EntityList`` where each object refers to ``Batch``.

The method parameters as included in v2.0.0 are as follows:

-  **query\_params (optional)**: User can pass a dictionary of conditions
   and condition values to filter the batches accordingly.
   Filter conditions can be like

   ``{"created_at__gt": "2021-04-05 14:19:38.303717+00:00"}``

   Note : timestamps to be passed according to ISO 8610 format in query_params

.data
~~~~~

The method returns the downsampled tag data for all the tags present in the
asset for the set ``start_time`` and ``stop_time``. Using ``sampling_data_points``
parameter you can control the downsampled points.

The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) This refers to the
   ``start_time`` for fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) This refers to the ``stop_time``
   for fetching the data of the asset.
-  **sampling\_data\_points (optional)**: This refers to the sampling_data_points at which
   the downsampled data is required. If the sampling_data_points provided, the method returns the
   data in the tag for the given time range with the datapoints equal to sampling_data_points.
   The default sampling_data_points is 1500.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user is supposed to pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.
-  **wide\_df (optional)**: When passed as ``true``, the data is returned
   in a wide format, and when passed as ``false``, it is returned in a
   long format. By default, the setting is ``true``.

Tag
------

This refers to the tag entity which contains the details of the tag. Tag
contains all the properties of the base Entity defined above.
When one prints the name of the tag object, it returns the name alongwith the ID of the tag, with the
template as `Tag: {tag_name}_{tag_id}`

The available attributes in this class are:

-  **id**: Tag ID
-  **name**: Tag Name
-  **tag_type**: The tag types:- 1.Raw, 2.Soft, 3.Aggregation, 4.Bitwise, 5.Writeback
-  **tag_data_type**: The tag data types. They are given by
.. list-table:: Tag Data Types
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 0
     - DOUBLE
   * - 1
     - STRING
   * - 2
     - BOOLEAN
   * - 3
     - INT
   * - 4
     - LONG
   * - 5
     - FLOAT
   * - 6
     - SPECTRAL
-  **short_name**: Tag short name
-  **edge_connector**: The data source ID
-  **tag_process_type**: The tag process types. They are given by:
.. list-table:: Tag Process Type
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 1
     - PROCESS_VARIABLE
   * - 2
     - CONDITION_VARIABLE
   * - 3
     - PROCESS_ALARM
   * - 4
     - PROCESS_EVENT
   * - 5
     - ANOMALY_SCORE
   * - 6
     - PREDICTED_VARIABLE
   * - 7
     - OTHERS
   * - 8
     - WORKFLOW
   * - 9
     - INFLUENCING_SCORE
-  **category**: Intelligence Categories. They are given by:
.. list-table:: Tag Intelligence Categories
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 1
     - Energy
   * - 2
     - Throughput
   * - 3
     - Reliability
   * - 4
     - Quality
   * - 5
     - Safety
   * - 6
     - Environment
-  **uom_name**: The name of measurement unit.
-  **asset**: ID of the asset
-  **created_by**: The user ID, who created this tag
-  **value_table**: The key value pair where key is the integer while the value is the string

The available methods are as follows:
*************************************

.data
~~~~~

The method returns the downsampled tagdata for the selected tag for the set
``start_time`` and ``stop_time``,Using ``sampling_data_points``
parameter you can control the downsampled points. The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) Refers to the ``start_time`` for
   fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) Refers to the ``stop_time`` for
   fetching the data of the asset.
-  **sampling\_data_\points (optional)**: This refers to the sampling_data_points at which
   the downsampled data is required. If the sampling_data_points provided, the method returns the
   data in the tag for the given time range with the datapoints equal to sampling_data_points.
   The default sampling_data_points is 1500.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **wavelengths (optional)**: This parameter is only valid for spectral
   type tags.User can pass a dict with key as "wavelengths" and value as
   the list of wavelength values for which user wants to fetch the data.
   By default for a given spectral tag, data for all of its available
   wavelengths will be fetched. By passing this paramter user can choose
   to fetch for the specified wavelengths.
-  **transformations (optional)**: The user is supposed to pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.
-  **wide\_df (optional)**: When passed as ``true``, the data is returned
   in a wide format, and when passed as ``false``, it is returned in a
   long format. By default, the setting is ``true``.


.wavelengths
~~~~~~~~~~~~

The method returns the list of all the wavelengths for the given spectral
tag entity, and throws an error otherwise. The method parameters are as follows:

- **start\_time (optional)**: (epoch) Refers to the ``start_time`` for evaluating
  the wavelengths for the spectral tag. In case this is not provided, this defaults
  to the time, when the given spectral tag is created at.
- **stop\_time (optional)**: (epoch) Refers to the ``stop_time`` for evaluating
  the wavelengths for the spectral tag. In case this is not provided, this defaults
  to the current datetime value

Batch
--------

This refers to the batch entity which contains the details of the tag.
Tag contains all the properties of the base Entity defined above.
When one prints the name of the batch object, it returns the name alongwith the ID of the batch and the
template as `Batch: {batch_name}_{batch_id}`

The available attributes in this class are:

-  **id**: Batch ID
-  **batch_name**: Batch Name
-  **start**: Batch start time in epoch
-  **stop**: Batch stop time in epoch
-  **notes**: List of notes regarding the batch
-  **is_questionable**: Whether the batch is questionable

EdgeConnector
--------------

This refers to the datasource entity which contains the details of
the datasource. Datasource contains all the properties of the base Entity defined
above.
When one prints the name of the datasource object, it returns the ID of the datasource and the
template as `datasource: {datasource_name}_{datasource_id}`

The available attributes in this class are:

-  **id**: Datasource ID
-  **created_at**: Time of creation of data source in epoch
-  **edge_device**: ID of the edge node
-  **connector_protocol**: The different datasource types are as follows:
.. list-table:: Data Source connector protocol
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 200
     - ABDF1
   * - 201
     - OPTO22
   * - 202
     - OPCDA
   * - 203
     - OSIPI
   * - 204
     - MODBUS
   * - 205
     - MQTT
   * - 206
     - OPCUA
   * - 207
     - SQL
-  **last_streamed_on**: Last streamed on epoch
-  **update_interval**: Update interval in ms
-  **name**: Name of the datasource
-  **stream_status**: The stream status for the datasource are as follows:
.. list-table:: Data Source streaming status
   :widths: 50 50
   :header-rows: 1

   * - Integer
     - Constant
   * - 0
     - INIT
   * - 1
     - ACTIVE
   * - 2
     - PARTIAL_STREAMING
   * - 3
     - INACTIVE
   * - 4
     - UNASSIGNED_TAGS
-  **created_by**: ID of the user who created the datasource
-  **config**: Configurations of the data source
-  **parent**: In case of query datasource, this refers to the ID of the parent datasource

The available methods are as follows:
*************************************

.get\_tags
~~~~~~~~~~

The method returns all the tags present in the given datasource in the form
of ``EntityList`` where each object refers to ``Tag``.

.data
~~~~~

The method returns the downsampled tag data for all the tags present in the
datasource for the set ``start_time`` and ``stop_time``. Using ``sampling_data_points``
parameter you can control the downsampled points.

The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) This refers to the
   ``start_time`` for fetching the data of the datasource.
-  **stop\_time (mandatory)**: (epoch) This refers to the ``stop_time``
   for fetching the data of the data ource.
-  **sampling\_data\_points (optional)**: This refers to the sampling_data_points at which
   the downsampled data is required. If the sampling_data_points provided, the method returns the
   data in the tag for the given time range with the datapoints equal to sampling_data_points.
   The default sampling_data_points is 1500.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user must pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.
-  **wide\_df (optional)**: When passed as ``true``, the data is returned
   in a wide format, and when passed as ``false``, it is returned in a
   long format. By default, the setting is ``true``.

.historical_data
~~~~~~~~~~~~~~~~

The method returns the historical tag data iterator for all the tags present in the
datasource for the set ``start_time`` and ``stop_time``. It can be used to iterate
through the ddata in custom batches as decided by the user. More details are
provided under the ``HistoricalTagDataIterator`` subsection.

The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) This refers to the
   ``start_time`` for fetching the data of the datasource.
-  **stop\_time (mandatory)**: (epoch) This refers to the ``stop_time``
   for fetching the data of the data source.
-  **batch_size (optional)**: This refers to the number of rows in each page
   while iterating through the historical data
-  **max_records (optional)**: This refers to the maximum number of records
   that are to be fetched in the API call
-  **tags (optional)**: (EntityList) This is the entitylist of tags. This is an
   optional value, and will take all the data source tags by default
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.

ContextFrame
---------------

This refers to the context frame entity which contains the details of
the tag. ContextFrame contains all the properties of the base Entity defined
above.
When one prints the name of the ContextFrame object, it returns the ID of the ContextFrame and the
template as `ContextFrame: {context_frame_id}`

The available attributes in this class are:

- **id**: ContextFrame ID
- **name**: ContextFrame name
- **description**: ContextFrame description
- **pu_or_wc**: ID of the Process Unit/Work cell

The available methods are as follows:
*************************************

-  **occurrences**: The method returns all the occurrences of the given
   ContextFrame in the form of ``EntityList`` where each object refers
   to ``ContextFrameOccurrence``.

   The method parameters as included in v2.0.0 are as follows:

   -  **query\_params (optional)**: User can pass a dictionary of conditions
      and condition values to filter the ContextFrame Occurrences accordingly.
      Filter conditions can be like
      ``{"start_ef_occurrence": "A3412", "stop_ef_occurrence": "C7415"}``

ContextFrameOccurrence
-------------------------

This refers to the context frame occurrence entity which contains the
details of the tag. ContextFrameOccurrence contains all the properties of the base Entity
defined above.
When one prints the name of the ContextFrame object, it returns a random unique integer denoting the occurrence, with the
template as ``ContextFrameOccurrence: {random_integer}``

The available attributes in this class are:

-  **id**: ContextFrameOccurrence ID
-  **start_ef_occurrence**: Start event frame occurrence for the context frame
-  **stop_ef_occurrence**: Stop event frame occurrence for the context frame
-  **is_valid**: Whether the context frame occurrence is valid
-  **context_frame**: Context Frame ID

Model
--------

This refers to Model entity, which contains the details of the model,
Model contains all the properties of the base Entity defined above.
When one prints the name of the model object, it returns the name alongwith the ID of the model, with the
template as `Model: {model_name}_{model_id}`

The available attributes in this class are:

-  **model_id**: Unique ID for the model
-  **model_name**: Name given for the model
-  **feature_tags**: IDs of tags used as Feature
-  **output_tag**: ID of the tag in which prediction results are stored
-  **target_tag**: ID of the tag which is used as the parent for prediction output tag
-  **is_spectral_model**: Boolean if the model is spectral or not

The available methods are as follows:
*************************************

.model\_instance
~~~~~~~~~~~~~~~~

This method returns the Model object (created and deployed by extending model base- BaseQuarticModel).

EntityList
-------------

This class contains the list of entities, where each entity can be of
the type ``Asset``, ``Tag``,
``ContextFrame``,\ ``ContextFrameOccurrence``, ``Model`` and ``Batch``.

The class requires the following parameters for initialization:

-  **class\_type (mandatory)**: Refers to the type of objects it will
   contain. These can be ``Asset``, ``Tag``, ``ContextFrame``,
   ``ContextFrameOccurrence``, ``Model`` or ``Batch``.
-  **entities\_list (optional)**: Refers to the list of entities, which
   will be contained in the list. The types should match the
   ``class_type`` as provided. In case this is not present, it will
   default to an empty list.

The available methods are as follows:
*************************************

.get
~~~~

The method returns the first item in the list whose attribute ``name``
has the value ``value``. It requires the following parameters:

-  **name (mandatory)**: Refers to the name of the attribute.
-  **value (mandatory)**: Refers to the value of this attribute.

The usage is as below:

::

    asset_with_id_1 = client_assets.get("id", 1)

.all
~~~~

The method returns all the entities present in the list.

::

    all_assets = client_assets.all()

.first
~~~~~~

This method returns the first element of the EntityList.

::

    first_asset = client_assets.first()

.last
~~~~~

This method returns the last element of the EntityList.

::

    last_asset = client_assets.last()

.add
~~~~

This method adds the given object into the list. If the object already
exists or it belongs to a different class\_type, it throws an exception.

::

    client_assets.add(new_asset_entity)

.filter
~~~~~~~~
This method filters the given EntityList to return an updated list that contains only those entities which satisfy all the conditions given in arguments.
It works with all primitive attribtues of the ``Entity`` in the ``EntityList``, if the specific operation is defined for that data type.


It takes multiple keyword arguments as a parameter (**\*\*kwargs**) to filter the entities.

For a simple filter operation that includes entities by checking for equality, the format is: `entity_attribute=value`

For operators other than equality, the format is: `entity_attribute__operator=value`

You can |reference_link| for a list of possible operators.

.. |reference_link| raw:: html

   <a href="https://docs.python.org/3/library/operator.html" target="_blank">refer here</a>


::

   filtered_entity_list = client_assets.filter(status='Inactive')
   filtered_entity_list = client_assets.filter(country__ne='India')



.exclude
~~~~~~~~

This method filters the given EntityList to return an updated list that
doesn't contain entities which satisfy any of the conditions given in arguments.

It takes the same arguments as ``.filter`` above but negates the conditions to exclude them.
::

    updated_entity_list = client_assets.exclude(id=5)
    updated_entity_list = client_assets.exclude(created_at__lt=first_asset.created_at)

.data
~~~~~

This method is present only for the ``Tag`` type EntityList, and it
returns the data present in the given tags. It returns downsampled 
data for given tags, and has the following parameters:

-  **start\_time (mandatory)**: (epoch) Refers to the ``start_time`` for
   fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) Refers to the ``stop_time`` for
   fetching the data of the asset.
-  **sampling\_data\_points (optional)**: This refers to the sampling_data_points at which
   the downsampled data is required. If the sampling_data_points provided, the method returns the
   data in the tag for the given time range with the datapoints equal to sampling_data_points.
   The default sampling_data_points is 1500.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user must pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.
-  **wide\_df (optional)**: When passed as ``true``, the data is returned
    in a wide format, and when passed as ``false``, it is returned in a
    long format. By default, the setting is ``true``.

TagData
------------------

Querying data for any set of tags in any given duration returns downsampled
tag data.Using ``sampling_data_points`` parameter you can control the downsampled
points. When the ``.data`` of tags/assets is called, the
method queries for data between ``start_time`` and ``stop_time`` 
and downsample the data points for all the tags for given ``sampling_data_points``.

HistoricalTagDataIterator
-------------------------

Querying historical data for any set of tags in any given duration returns
an instance of ``HistoricalTagDataIterator``, which can be used to iterate
between the given time range. When the ``.historical_data`` of data source
is called, the class queries via cursor, based upon the entered ``batch_size``

The available methods are as follows:
*************************************

.get_complete_data_in_range
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The method loops through the complete range and returns the final data frame
which is required. Note that this is meant to be used only for pandas return
of historical data and not for json return. The method has the following parameters:

-  **historical\_data\_iterator (mandatory)** This is the historicaldataiterator
   object whose complete data is to be returned

Transformations:
****************

The tag data iterator is created based upon the multiple transformations
that a user might need. The transformations is a list of dictionaries
where each dictionary contains the details of interpolation/aggregation
to be performed on the data. The different transformations are:

Interpolation:
~~~~~~~~~~~~~~

Interpolation requires the following keys to be present:

-  **transformation\_type (mandatory)**: Refers to the type of
   transformation and must always be ``interpolation``.
-  **column (mandatory)**: Refers to the column which is to be
   interpolated.
-  **method (mandatory)**: Refers to the interpolation method; the
   options are: linear, spline, cubic interpolation, and polynomial.
-  **order (mandatory)**: Refers to the order of the interpolation, and
   is required for all methods except ``linear``.
-  **limit\_direction (optional)**: Refers to the direction in which the
   interpolation takes place. The default value is ``forward``.

Aggregation:
~~~~~~~~~~~~

Aggregation requires the following keys to be present:

-  **transformation\_type (mandatory)**: Refers to the type of
   transformation and must always be ``aggregation``.
-  **aggregation\_column (mandatory)**: Refers to the column being
   aggregated.
-  **aggregation\_dict (mandatory)**: This dictionary refers to the
   methods on which the different columns in the dataset are to be
   aggregated.

Procedure
---------------

This refers to the product (Product Harbour) procedures. Procedures are present/created within the Product

The available attributes in this class are:

- **id**: Procedure ID
- **name**: Procedure name
- **additional_attributes**: This field contains additional information and fields of Procedure like receipe_type, formula and receipe_version
- **procedure_state**: state among 5 values
- **test_results**: 
- **site**: Site id under which procedure gets created
- **product**: ID of the Product under which that procedure gets created
- **created_by**: The user ID, who created this procedure
- **created_at**: created at date time
- **updated_at**: updated at date time


The available methods are as follows:
*************************************

-  **fetch_unit_procedures**: The method returns all the UnitProcedures of the given
   Procedure in the form of ``EntityList`` where each object refers
   to ``ProcedureStep``.

   The method parameters as included in v2.0.0 are as follows:

   -  **query\_params (optional)**: User can pass a dictionary of conditions
      and condition values to filter the UnitProcedures accordingly.

ProcedureStep
---------------

This refers to the Node/Child(UnitProcedure/Operation/Phase/PhaseStep) added in Procedure Node in the hierarchy.

The available attributes in this class are:

- **id**: ProcedureStep ID
- **name**: ProcedureStep name
- **step_type**: Integer Field denoted the type of node(UnitProcedure/Operation/Phase/PhaseStep) at each step
- **order**: Sequence in which we want to add child nodes inside parent(ProcedureStep) node
- **parent**: ID of the parent ProcedureStep Node under which that procedure step gets created
- **procedure**: ID of the Procedure under which that procedure step gets created
- **step_components**: list of components involved
- **created_at**: created at date time
- **updated_at**: updated at date time


The available methods are as follows:
*************************************

-  **fetch_substep_details**: The method returns all the ProcedureStep details like Operation/Phase/PhaseStep in the
   form of ``EntityList`` where each object refers to ``ProcedureStep``.

   The method parameters as included in v2.0.0 are as follows:

   -  **query\_params (optional)**: User can pass a dictionary of conditions
      and condition values to filter the ProcedureStep accordingly.

Product
-------

This refers to the Product under which all the Procedure and Procedure Step hierarchy is present or created.
This is the root node of the entire hierarchy.

The available attributes in this class are:

- **id**: Product ID
- **name**: Product name
- **client**: Client id under which procedure gets created
- **description**: This contains description of the product
- **created_by**: The user ID, who created this product
- **created_by_name**: The user name, who created this product
- **created_at**: created at date time
- **updated_at**: updated at date time


The available methods are as follows:
*************************************

-  **get_procedures**: The method returns all the Procedures of the given
   Product in the form of ``EntityList`` where each object refers
   to ``Procedure`` Entity.

   The method parameters as included in v2.0.0 are as follows:

   -  **query\_params (optional)**: User can pass a dictionary of conditions
      and condition values to filter the Procedures accordingly.

Site
----

This refers to the User's Client Site.

The available attributes in this class are:

- **id**: Site ID
- **name**: Site name
- **country_name**: Country name
- **state_name**: State name
- **pin_code**: PinCode where site belongs
- **address_line_1**: Line one of the site address
- **address_line_2**: Line two of the site address
- **country**: Country Id site belongs to
- **state**: State Id site belongs to
- **client**: Client Id site belongs to
