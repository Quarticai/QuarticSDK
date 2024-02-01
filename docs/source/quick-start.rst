Quick start
===========

The steps to fetch data points of one or more tags, train a model, or save it on
the Quartic AI Platform are as follows:

Step 1
---------

Initialize the ``APIClient`` with the authentication details. Currently,
Quartic SDK supports two kinds of authentication: Basic Authentication
and OAuth2.0. In Basic Authentication, the user must pass the parameters
of username and password; and in OAuth2.0, the client token.

For our example, if the authentication used is Basic Authentication, the
Quartic host is ``https://test.quartic.ai``, and the username and
password is ``username`` and ``password``, then the APIClient will look
like this:

::

    from quartic_sdk import APIClient

    client = APIClient("https://test.quartic.ai", username="username", password="password")

Step 2
---------

Fetch primitive objects. These objects do not require any extra
parameters and can be fetched directly from the ``client`` object. The
list returned will contain the class object ``EntityList``, which
consists of the methods required for getting instances and depends on
the given parameters.

::

    assets = client.assets()
    context_frames = client.context_frame_definitions()

Step 3
---------

Fetch a tag of an asset, which will be further used to fetch data
points. Pass the start\_time and the stop\_time of the query in epoch.
For example, for a duration of 1 day, from 1 Jan 2021 to 2 Jan 2021, the
corresponding time in epoch would be 1609439400000 and 1609525800000.

::

    asset = assets.first()
    asset_tags = asset.get_tags()
    feature_tags = [tag.id for tag in asset_tags[:5]]
    target_tag = asset_tags.last().id
    asset_data = asset.data(start_time=1609439400000, stop_time=1609525800000) # This will get downsampled data

Step 4
---------

Save the tag data in the data frame.

::

    import pandas as pd
    combined_data_frame = pd.DataFrame(columns=feature_tags)
    for data in asset_data:
        combined_data_frame = combined_data_frame.append(data)

Step 5
---------

Once the client is initialized and data fetched, models can now be
trained, tested and deployed to Quartic AI Platform using below:

.. code:: python

    from quartic_sdk.model import BaseQuarticModel
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split


    class ExampleModel(BaseQuarticModel):
        def __init__(self, model):
            self.model = model
            super().__init__("My Sample Model", description='This is a simple model to give a quick start for user')

        def predict(self, input_df):
            return self.model.predict(input_df)

    model = linear_model.LinearRegression()
    X_train, X_test, y_train, y_test = train_test_split(combined_data_frame[feature_tags],
                    df[[feature_tags[-1]]].values.ravel(), random_state=42)

    model.fit(X_train, y_train)
    model.predict(X_test)
    example_model = ExampleModel(model)
    example_model.predict(X_test)

    example_model.save(client, output_tag_name='Prediction Tag Name',
                       feature_tags=feature_tags, target_tag=target_tag,
                       test_df=X_test)