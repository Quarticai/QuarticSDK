
Installation
---------------

Install using ``pip``:

::

    pip install quartic-sdk

...or follow the following steps to install it from the source:

::

    git clone https://github.com/Quarticai/QuarticSDK/
    python setup.py install

Example
----------

Here's an example on how the Quartic SDK can be used:

GraphQLClient
--------------

::

    # Assuming that the Quartic.ai server is hosted at `https://test.quartic.ai/`,
    # with the login credentials as username and password is "testuser" and `testpassword respectively,
    # then use GraphqlClient in the following format.

    from quartic_sdk import GraphqlClient

    client = GraphqlClient(url='https://test.quartic.ai/', username='testuser', password='testpassword')

    # Executing Query by:

    query='''
    query MyQuery {
      Site {
        id
        name
      }
    }
    '''

    result = client.execute_query(query=query)

    # To execute query asynchronously use the function below.

    # You should see the following result:

    {'data': {'Site': [{'id': '1', 'name': 'quartic'}, {'id': '8', 'name': 'ABC site 1'}, {'id': '12', 'name': 'XYC 123'}]}

    async def execute_graphql_query():
        query='''
            query MyQuery {
              Site {
                id
                name
              }
            }
            '''
        resp = await client.execute_async_query(query=query)
        return resp

    # Note: The above function will return a coroutine object.

    # Example to upload a file.

    query = '''
        mutation($file: Upload!,$edge_connector: Int!,$date_format: DateTime!) {
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

    response = client.execute_query(query=query, variables=variables)





Getting the assets, tags, batches from the server
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # Assuming that the Quartic.ai server is hosted at `https://test.quartic.ai/`,
    # with the login credentials as username and password is "testuser" and `testpassword respectively,
    # then use APIClient in the following format.

    from quartic_sdk import APIClient

    client = APIClient("https://test.quartic.ai", username="username", password="password")
    user_assets = client.assets() # Get the list of all assets that the user has access to

    asset = user_assets.get("name","Test Asset") # Get a specific asset with the name "Test Asset"
    asset_tags = asset.get_tags() # Gets the list of all tags

    asset_data = asset.data(start_time=1000000, stop_time=2000000) # Get the data of the asset for the given interval between start_time and stop_time. This returns downsampled tag data.
    print(asset_data) # Returns the data present in wide dataframe format.

    asset_data = asset.data(start_time=1000000, stop_time=2000000, wide_df=False) # Get the data of the asset for the given interval between start_time and stop_time in long df format. This returns downsampled tag data.
    print(asset_data) # Returns the data present in long dataframe format.

    # For getting raw data we need to use freeflowpaginated query using Graphql Client
    # Below is the example for the same
    # Assuming that the Quartic.ai server is hosted at `https://test.quartic.ai/`, 
    # with the login credentials as username and password is "testuser" and `testpassword respectively, 
    # then use GraphqlClient in the following format.

    from quartic_sdk import GraphqlClient

    client = GraphqlClient(url='https://test.quartic.ai/', username='testuser', password='testpassword')

    # Executing Query by:

    query='''
    query MyQuery($offset_map: CustomDict, $startTime: String!, $stopTime: String!, $tags: [Int]!, $limit: Int) 
    {
    freeflowPaginated (startTime: $startTime, stopTime: $stopTime, tags: $tags, limit: $limit, offsetMap: $offset_map ) 
    }
    '''
    # The varaibles passsed are as follows:
    # tags (required) : This is list of ids in int datatype
    # startTime (required) : startTime in epoch but in string format
    # stopTime (required) : stopTime in epoch but in string format
    # limit (optional) : limit the datapoints of query. defaults to 1500
    # offset_map (optional) : Dictionary where key is tag_id and value is the next offset returned by query executed.

    variables={
    "tags": [
        21295
    ],
    "startTime": "1706693453221",
    "stopTime": "1706697053222",
    "limit": 2,
    "offset_map": {}
    }

    result = client.execute_query(query=query)

    #You should see the following result:

    {
    "data": {
        "freeflowPaginated": {
        "data": {
            "21295": {
            "data": [
                [
                1706693453500,
                808
                ],
                [
                1706693454000,
                809
                ]
            ],
            "offset": 2
            }
        },
        "status": 200
        }
    }
    }

    #using the offset in result you can create the next offset in following way and recall the execute query function
    variables = {
    "tags": [
        21295
    ],
    "startTime": "1706693453221",
    "stopTime": "1706697053222",
    "limit": 2,
    "offset_map": {21295:result['data']['freeflowPaginated']['data']['21295']['offset']}
    }

    result = client.execute_query(query=query)

    #You should see the following result:

    {
    "data": {
        "freeflowPaginated": {
        "data": {
            "21295": {
            "data": [
                [
                1706693454500,
                810
                ],
                [
                1706693455000,
                811
                ]
            ],
            "offset": 4
            }
        },
        "status": 200
        }
    }
    }
