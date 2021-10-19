Model Creation
==============

QuarticSDK allows the users to deploy two types of models via the
Quartic AI platform. It allows deployment of normal tag-based Machine
Learning models, that use the tags as the feature variables, as well
as the deployment of wavelength based models for spectral tags that use
spectral tag wavelengths as the feature variables.
This article explains how to create, wrap, and deploy both kinds of models to the
Quartic AI Platform.

BaseQuarticModel
----------------

BaseQuarticModel is a base class for all the ML models that can be deployed to
the Platform, which use the tags as features for the deployed ML model. Users
must extend this class and implement the predict method to make the ML model
compatible to deploy in the Quartic AI Platform.
The available methods are as follows:

__init__
~~~~~~~~

The method has following parameters for initialization:

-  **name (mandatory)**: Enter a unique name for the model
-  **description (optional)**: Describe the model. The default value for
   the field is ``''``
-  **log\_level (optional)**: Select one of the log level for the model:
   ``'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'``. The
   default value is ``INFO``.

.. raw:: html

   <div class="note">

Note: While implementing an instance of BaseQuarticModel, users must call
super().\ **init**\  with above parameters.

.. raw:: html

   </div>

.save
~~~~~

This is a private method used to save the model to the Quartic AI
Platform.

.. raw:: html

   <div class="note">

Note: While implementing an instance of BaseQuarticModel, users must call
super().\ **init**\  with above parameters.

.. raw:: html

   </div>

.. raw:: html

   <div class="note-warning">

Warning: Do not override this method.

.. raw:: html

   </div>

-  **client (mandatory)**: Refers to an instance of APIClient
-  **output\_tag\_name (mandatory)**: Refers to a unique name for the
   prediction results
-  **feature\_tags (mandatory)**: Refers to a list of tags that are used
   as features in the model
-  **target\_tag (mandatory)**: Refers to the tag that has been assigned to an asset the ML model will use this asset as a parent of the current
   prediction output
-  **test\_df (mandatory)**: Refers to the test dataframe that validates the model prediction
   results and ensures compatibility with the Quartic AI Platform
-  **ml\_node (optional)**: Refers to the Ml Node ID for deploying model
   to a particular node.

.. raw:: html

   <div class="note">

Note:  1. The Quartic AI Platform selects the best ML node depending on
CPU and memory utilization at the time of deployment (by default). To
deploy a model to a particular node, specify ml\_node={node\_id}; for
example, ml\_node=1 . 2. The save\_method takes a sample of test data
frame to validate the model.\_

.. raw:: html

   </div>

.predict
~~~~~~~~

The method has the following parameters for running the predictions of a
ML model:

-  **input\_df (mandatory)**: Refers to the dataframe on which the model is being evaluated

.. raw:: html

   <div class="note">

Note:  1. Users must override this method to transform and run
predictions for the model created. 2. input\_df is expected to have tag
IDs as the column names. If model is trained with tag names instead, a
transformation step must be added and used in predict method to
convert the tag IDs in input dataframe into tag names.\_

.. raw:: html

   </div>

Example
~~~~~~~

.. code:: python

    import pandas as pd
    from quartic_sdk.model import BaseQuarticModel
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

    class ExampleModel(BaseQuarticModel):
        def __init__(self):
            self.model = RandomForestRegressor()
            super().__init__("Sample Model", description='This is a simple model to give a quick introduction on creating and deploying models to the Quartic AI Platform.')

        def train(self, X, y):
            self.model.fit(X, y)

        def predict(self, input_df):
            predictions = self.model.predict(input_df)
            return pd.Series(predictions)

    quartic_model = ExampleModel()
    quartic_model.train(X_train, y_train) # Training data extracted from data loaded from the Quartic AI Platform
    quartic_model.save(client=api_client, output_tag_name="Prediction Result",
                       feature_tags=[1,2,3], # tags that are used in the X variable or features, for example 1,2,3
                       target_tag = 3, # tag that specifies a relationship for prediction, for example, 3
                       test_df = X_train
                       )

.. raw:: html

   <div class="note">

Note: Any intermediate steps that are used for model training outside
the wrapper must be included in wrapper for applying similar set of
transformations during prediction.

.. raw:: html

   </div>


BaseSpectralModel
----------------

BaseSpectralModel is a base class for all the ML models that can be deployed to
the Platform, which use the spectral tag wavelengths as features for the deployed
ML model. Users must extend this class and implement the predict method to make
the ML model compatible to deploy in the Quartic AI Platform.
The available methods are as follows:

__init__
~~~~~~~~

The method has following parameters for initialization:

-  **name (mandatory)**: Enter a unique name for the model
-  **description (optional)**: Describe the model. The default value for
   the field is ``''``
-  **log\_level (optional)**: Select one of the log level for the model:
   ``'CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET'``. The
   default value is ``INFO``.

.. raw:: html

   <div class="note">

Note: While implementing an instance of BaseSpectralModel, users must call
super().\ **init**\  with above parameters.

.. raw:: html

   </div>

.save
~~~~~

This is a private method used to save the model to the Quartic AI
Platform.

.. raw:: html

   <div class="note">

Note: While implementing an instance of BaseSpectralModel, users must call
super().\ **init**\  with above parameters.

.. raw:: html

   </div>

.. raw:: html

   <div class="note-warning">

Warning: Do not override this method.

.. raw:: html

   </div>

-  **client (mandatory)**: Refers to an instance of APIClient
-  **output\_tag\_name (mandatory)**: Refers to a unique name for the
   prediction results
-  **feature\_wavelengths (mandatory)**: Refers to a list of spectral tag wavelengths that are
   as features in the model
-  **spectral\_tag (mandatory)**: Refers to the spectral tag whose wavelengths are used for deploying the model
-  **target\_tag (mandatory)**: Refers to the tag that has been assigned to an asset the ML model will use this asset as a parent of the current
   prediction output
-  **test\_df (mandatory)**: Refers to the test dataframe that validates the model prediction
   results and ensures compatibility with the Quartic AI Platform
-  **ml\_node (optional)**: Refers to the Ml Node ID for deploying model
   to a particular node.

.. raw:: html

   <div class="note">

Note:  1. The Quartic AI Platform selects the best ML node depending on
CPU and memory utilization at the time of deployment (by default). To
deploy a model to a particular node, specify ml\_node={node\_id}; for
example, ml\_node=1 . 2. The save\_method takes a sample of test data
frame to validate the model.\_

.. raw:: html

   </div>

.predict
~~~~~~~~

The method has the following parameters for running the predictions of a
ML model:

-  **input\_df (mandatory)**: Refers to the dataframe on which the model is being evaluated

.. raw:: html

   <div class="note">

Note:  1. Users must override this method to transform and run
predictions for the model created. 2. input\_df is expected to have tag
IDs as the column names. If model is trained with tag names instead, a
transformation step must be added and used in predict method to
convert the tag IDs in input dataframe into tag names.\_

.. raw:: html

   </div>

Example
~~~~~~~

.. code:: python

    import pandas as pd
    from quartic_sdk.model import BaseSpectralModel
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

    class ExampleModel(BaseSpectralModel):
        def __init__(self):
            self.model = RandomForestRegressor()
            super().__init__("Sample Model", description='This is a simple model to give a quick introduction on creating and deploying models to the Quartic AI Platform.')

        def train(self, X, y):
            self.model.fit(X, y)

        def predict(self, input_df):
            predictions = self.model.predict(input_df)
            return pd.Series(predictions)

    quartic_model = ExampleModel()
    quartic_model.train(X_train, y_train) # Training data extracted from data loaded from the Quartic AI Platform
    quartic_model.save(client=api_client, output_tag_name="Prediction Result",
                       feature_tags=[1,2,3], # tags that are used in the X variable or features, for example 1,2,3
                       target_tag = 3, # tag that specifies a relationship for prediction, for example, 3
                       test_df = X_train
                       )

.. raw:: html

   <div class="note">

Note: Any intermediate steps that are used for model training outside
the wrapper must be included in wrapper for applying similar set of
transformations during prediction.

.. raw:: html

   </div>

