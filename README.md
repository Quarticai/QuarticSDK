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
first_tag_data_iterator=first_tag.data(start_time=1000000,stop_time=2000000) # Returns the data present in the first tag for the time range of 1000000 to 2000000

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
