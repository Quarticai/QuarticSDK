
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
    asset_data = asset.data(start_time=1000000, stop_time=2000000) # Get the data of the asset for the given interval between start_time and stop_time. This returns an iterator, which can be iterated to get all the data points present.
    print(asset_data[0]) # Returns the data present at the 0th index

