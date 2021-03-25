===================
Basic Functionality
===================

This article explains the various classes of Quartic SDK along with their methods and
available attributes.

APIClient
------------

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

    client = APIClient(host="http://test.quartic.ai", username="username", password="password")

It can be noted that the class provides two methods of authentication to the user.

The two methods are BasicAuthentication and OAuth2.0:
*****************************************************

BasicAuthentication:
~~~~~~~~~~~~~~~~~~~~

The user must pass the username and password along with the hostname in the APIClient
to ensure all the successive API calls are authenticated via Basic Authentication

::

    client = APIClient(host="http://test.quartic.ai", username="username", password="password")

OAuth2.0
~~~~~~~~

The user must pass the OAuth token along with the hostname to ensure that all the
successive API calls are authenticated via OAuth2.0. For the detailed information on fetching
tokens, please refer to the Global Settings article in the Quartic Knowledge Base.

::

    client = APIClient(host="http://test.quartic.ai", oauth_token="9865c994212e495690c2db3fc6cbdfea")

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

::

    client_assets = client.assets()

.context_frames
~~~~~~~~~~~~~~~

This method returns the list of context frames which are created using the assets
that the user has access to. The list of context frames are an
object of type ``EntityList``. More details on the class is provided below.

::

    client_context_frames = client.context_frames()

.tags
~~~~~

This method requires the following parameters to be called:

**asset\_id (mandatory)**: The asset\_id of the asset whose tags are to
be returned.

::

    tags_of_asset_id_1 = client.tags(1)

.edge_connectors
~~~~~~~~~~~~~~~~

This method returns the list of all the data sources which the user has access to.
The list of data sources are an object of type ``EntityList``. More details on the class
are provided below.

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
-  **status**: The streaming status of the asset :- 0.INIT, 1.ACTIVE, 2.PARTIAL_STREAMING, 3.INACTIVE, 4.UNASSIGNED_TAGS

The available methods are as follows:
*************************************

.get\_tags
~~~~~~~~~~

The method returns all the tags present in the given asset in the form
of ``EntityList`` where each object refers to ``Tag``.

.batches
~~~~~~~~

The method returns all the batches present in the given asset in the
form of ``EntityList`` where each object refers to ``Batch``.

.data
~~~~~

The method returns the tag data iterator for all the tags present in the
asset for the set ``start_time`` and ``stop_time``. It can be used to
iterate through the data in batches of 200,000 datapoints. More details
are provided under the ``TagDataIterator`` subsection.

The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) This refers to the
   ``start_time`` for fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) This refers to the ``stop_time``
   for fetching the data of the asset.
-  **granularity (optional)**: This refers to the granularity at which
   data is required. If the granularity provided, the method returns the
   data in the tag for the given time range with the lower of the
   closest possible granularity: Raw (granularity of the datasource),
   5s, 30s, 60s, 300s, 1200s, 3600s, 10800s, 21600s, 43200s or 86400s.
   The default granularity is Raw.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user is supposed to pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.

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
-  **tag_data_type**: The tag data types:- 0.Double, 1.String, 2.Boolean, 3.Int, 4.Long, 5.Float
-  **short_name**: Tag short name
-  **edge_connector**: The data source ID
-  **tag_process_type**: The tag process types:- 1.Process Variable, 2.Condition Variable, 3.Process Alarm, 4.Process Event, 5.Anomaly Score, 6.Predicted Variable, 7.Others, 8.Workflow, 9.Influencing Score
-  **category**: Intelligence Categories:- 1.Energy, 2.Throughput, 3.Reliability, 4.Quality, 5.Safety, 6.Environment
-  **uom_name**: The name of measurement unit:- 1.Celsius, 2.Fahrenheit, 3.Pound per square inch, 4.Pascal, 5.Millibar, 6.Pound-force per square inch, 7.dB, 8.Acceleration of gravity, 9.Inch per second, 10.Revolutions per minute, 11.Meter, 12.Centemeter, 13.Millimeter, 14.Metre per second squared, 15.Millimetre per second, 16.Volt, 17.Amperes, 18.Milliampere, 19.Poiseuille, 20.Poise, 21.Kinematic, 22.Stokes, 23.Standard litre per minute, 24.On/Off, 25.Percent, 26.pH, 27.kilogram, 28.Percent On, 29.None, 30.Millimetre per second squared, 31.Counts, 32.Gallon, 33.Gallon per minute, 34.Inch, 35.Micro Simens, 36.Micro Simens Per Centimeter, 37.Parts Per Million, 38.Running/Stopped, 39.Open/Closed, 40.0/1, 41.Liters, 42.Hertz, 43.Hours, 44.Tonnes, 45.Optical density, 46.in/s pk, 47.Gs p-p, 48.Gs rms, 49.Gs pk, 50.kg/h, 51.kQ, null.No unit
-  **asset**: ID of the asset
-  **created_by**: The user ID, who created this tag
-  **value_table**: The key value pair where key is the integer while the value is the string

The available methods are as follows:
*************************************

.data
~~~~~

The method returns the tagdata iterator for the selected tag for the set
``start_time`` and ``stop_time``, which can be used to iterate through
the data in batches of 200,000 datapoints. More details under the
``TagDataIterator`` subsection. The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) Refers to the ``start_time`` for
   fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) Refers to the ``stop_time`` for
   fetching the data of the asset.
-  **granularity (optional)**: This refers to the granularity at which
   data is required. If the granularity provided, the method returns the
   data in the tag for the given time range with the lower of the
   closest possible granularity: Raw (granularity of the datasource),
   5s, 30s, 60s, 300s, 1200s, 3600s, 10800s, 21600s, 43200s or 86400s.
   The default granularity is Raw.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user is supposed to pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.

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
-  **asset**: Asset ID
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
-  **connector_protocol**: The different datasource types:- 200.ABDF1, 201.OPTO22, 202.OPCDA, 203.OSIPI, 204.MODBUS, 205.MQTT, 206.OPCUA, 207.SQL
-  **last_streamed_on**: Last streamed on epoch
-  **update_interval**: Update interval in ms
-  **name**: Name of the datasource
-  **stream_status**: The stream status for the datasource:- 0.INIT, 1.ACTIVE, 2.PARTIAL STREAMING, 3.INACTIVE, 4.UNASSIGNED TAGS
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

The method returns the tag data iterator for all the tags present in the
datasource for the set ``start_time`` and ``stop_time``. It can be used to
iterate through the data in batches of 200,000 datapoints. More details
are provided under the ``TagDataIterator`` subsection.

The method parameters are as follows:

-  **start\_time (mandatory)**: (epoch) This refers to the
   ``start_time`` for fetching the data of the datasource.
-  **stop\_time (mandatory)**: (epoch) This refers to the ``stop_time``
   for fetching the data of the data ource.
-  **granularity (optional)**: This refers to the granularity at which
   data is required. If the granularity provided, the method returns the
   data in the tag for the given time range with the lower of the
   closest possible granularity: Raw (granularity of the datasource),
   5s, 30s, 60s, 300s, 1200s, 3600s, 10800s, 21600s, 43200s or 86400s.
   The default granularity is Raw.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user must pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.

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

.exclude
~~~~~~~~

This method filters the given EntityList to return an updated list that
doesn't contain the entity which has the ``name`` attribute value as
``value``.

::

    updated_entity_list = client_assets.exclude("id", 1)

.data
~~~~~

This method is present only for the ``Tag`` type EntityList, and it
returns the data present in the given tags. It returns a TagDataIterator
instance, and has the following parameters:

-  **start\_time (mandatory)**: (epoch) Refers to the ``start_time`` for
   fetching the data of the asset.
-  **stop\_time (mandatory)**: (epoch) Refers to the ``stop_time`` for
   fetching the data of the asset.
-  **granularity (optional)**: This refers to the granularity at which
   data is required. If granularity is provided, the method returns the
   data in the tag for the given time range with the lower of the
   closest possible granularity: Raw (granularity of the datasource),
   5s, 30s, 60s, 300s, 1200s, 3600s, 10800s, 21600s, 43200s or 86400s.
   The default granularity is Raw.
-  **return\_type (optional)**: The user can pass either ``pd``, which
   will return the pandas dataframe iterator, or ``json`` which will
   return json object on return. This value takes the ``pd`` value as
   default.
-  **transformations (optional)**: The user must pass the list
   of interpolations and aggregations here. Further details on
   transformations is provided towards the end of this documentation.

TagDataIterator
------------------

Querying data for any set of tags in any given duration returns an
instance of ``TagDataIterator``, which can be used to iterate between
the given time range. When the ``.data`` of tags/assets is called, the
method divides the complete interval between ``start_time`` and
``stop_time`` into different time\_ranges, with each range containing up
to 200,000 data points for all the tags. The user can loop through this
interval to get all the data points.

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
