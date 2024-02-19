# QuarticSDK

> Quartic SDK is Quartic.ai's external software development kit which allows users to use assets, tags, and other intelligence outside the Quartic AI Platform. Using the Quartic SDK, third party developers who have access to the Quartic AI Platform can build custom applications.

[![Documentation Status](https://readthedocs.org/projects/quarticsdk/badge/?version=stable)](https://quarticsdk.readthedocs.io/en/stable/?badge=stable)

## Installation
---
Install using `pip`

```
pip install quartic-sdk
```
to Install complete package with all supported model libraries:
```
pip install quartic-sdk[complete]
```

...or follow the following steps to install it from the source:
```
git clone https://github.com/Quarticai/QuarticSDK/
python setup.py install
```

## Example
---
Comprehensive documentation is available at https://quarticsdk.readthedocs.io/en/latest/

Here's an example on how the Quartic SDK can be used:

#### Getting the assets, tags, batches from the server
```python
# Assuming that the Quartic.ai server is hosted at `https://test.quartic.ai/`, 
# with the login credentials as username and password is "testuser" and `testpassword respectively, 
# then use APIClient in the following format.

from quartic_sdk import APIClient
client = APIClient("https://test.quartic.ai/", username="testuser", password="testpassword")
user_assets = client.assets() # Get the list of all assets that the user has access to

asset = user_assets.get("name","Test Asset") # Get a specific asset with the name "Test Asset"
asset_tags = asset.get_tags() # Gets the list of all tags

first_tag=asset_tags.first() # Returns the first in the list of tags
tag_data = first_tag.data(start_time=1000000,stop_time=2000000) # Returns the downsampled data present in the first tag for the time range of 1000000 to 2000000 in wide data format.
```
```python
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

result = client.execute_query(query=query, variables=variables)

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
          ]
        }
      },
      "offset_map":{"21295":4}
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
  "offset_map": offset_map
}

result = client.execute_query(query=query,variables=variables)

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
          ]
        }
      },
      "offset_map":{"21295":6}
      "status": 200
    }
  }
}

```

```python

# If jwt auth expires the above code will throw Permission Error

# Another way to handle this is using retry mechanism which on permission error will handle the recreation of client.
# It is mentioned as below

from quartic_sdk import APIClient

retry_count = 2  # Number of times to retry the code
retry_delay = 5  # Delay in seconds between retries

while retry_count > 0:
    try:
        client = APIClient("https://test.quartic.ai/", username="testuser", password="testpassword")
        user_assets = client.assets()  # Get the list of all assets that the user has access to

        asset = user_assets.get("name", "Test Asset")  # Get a specific asset with the name "Test Asset"
        asset_tags = asset.get_tags()  # Gets the list of all tags

        first_tag = asset_tags.first()  # Returns the first in the list of tags
        tag_data = first_tag.data(start_time=1000000,
                                  stop_time=2000000)  # Returns the data present in the first tag for the time range of 1000000 to 2000000

        # If the code reaches here without exceptions, break out of the loop
        break
    except PermissionError:
        # If the refresh token expires, this error is thrown and recreation of client is needed to update the tokens
        retry_count -= 1
        if retry_count > 0:
            print(f"PermissionError: Retrying in {retry_delay} seconds...")
            time.sleep(retry_delay)
        else:
            # If still the error persist, the password might have been changed
            print("PermissionError: Maximum retries reached. Exiting.")
            break

```

```python

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

#You should see the following result:

{'data': {'Site': [{'id': '1', 'name': 'quartic'}, {'id': '8', 'name': 'ABC site 1'}, {'id': '12', 'name': 'XYZ 123'}]}

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

response = client.execute_query(query=query, variables=variables)


```



## Documentation
---
To run the documentation locally, run the following commands in terminal:
```
cd docs
make html

cd docs/source
sphinx-build -b html . _build
open build/html/index.html
```

## Test Cases
---
To run the behaviour test cases, run the command:
```
aloe
```
To run the unit test cases, run the command:
```
pytest
```
