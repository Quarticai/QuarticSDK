Expression Creation
==============

QuarticSDK allows the users to create softtags which allows doing certain operations on existing tags
This article explains how to create expressions using QuarticSDK

BaseReckonExpression
----------------

BaseReckonExpression is a base class for all the Reckon Expressions that can be deployed to
the Platform, which use the existing tags for new softtags output. Users
must extend this class and implement the evaluate method to make the expression
compatible to deploy in the Quartic AI Platform. BaseReckonExpression supports 
evaluating over longer time ranges with the use of with_window decorator.
The available methods are as follows:


.save
~~~~~

This is a private method used to save the model to the Quartic AI
Platform.




.. raw:: html

   <div class="note-warning">

Warning: Do not override this method.

.. raw:: html

   </div>

-  **client (mandatory)**: Refers to an instance of GraphqlClient
-  **output\_tag\_name (mandatory)**: Refers to a unique name for the
   evaluate results
-  **needs (mandatory)**: Refers to a list of tags that are used
   as inputs in evaluate method
-  **asset (mandatory)**: Asset id to be part saved in
-  **test\_df (mandatory)**: Refers to the test dataframe that validates the expression
   results and ensures compatibility with the Quartic AI Platform
-  **is\_streaming (mandatory)**: Refers to whether tag is streaming or not
-  **tag\_category (mandatory)**: Category of output tag

.. raw:: html



.evaluate
~~~~~~~~

The method has the following parameters for running the predictions of a
ML model:

-  **input\_df (mandatory)**: Refers to the dataframe on which the expression will run

.. raw:: html

   <div class="note">

Note:  1. Users must override this method to evaluate and run
on the dataframe. 2. input\_df is expected to have tag
IDs as the column names.

.. raw:: html

   </div>

Example
~~~~~~~

.. code:: python

   import pandas as pd
   from quartic_sdk.model import BaseReckonExpression
   from quartic_sdk import GraphqlClient

   import pandas as pd


   class ReckonExpression(BaseReckonExpression):
      def evaluate(self, input_df: pd.DataFrame) -> pd.Series:
         return input_df['5']*2
      



   test_exp = ReckonExpression()

   test_df = pd.DataFrame([{'5': 10}])

   api_client = GraphqlClient(url="serverUrl", username="user", password="password")
   test_exp.save(api_client,
   output_tag_name="softtag1_output",
   needs=["5"],
   asset=279,
   is_streaming=True,
   tag_category=1,
   test_df = test_df)

.. raw:: html


@BaseReckonExpression.with\_window
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The with\_window decorator enables evaluating expressions over longer time ranges.
Users can decorate evaluate method with the @BaseReckonExpression.with_window, passing the window duration,
once the expression is deployed the input\_df received by evaluate will contain the data for specified
duration.  

The decorator has the following parameters:

-  **duration (mandatory)**: Refers to the window duration in seconds for which the data is required

.. raw:: html

   <div class="note">


Example
~~~~~~~

.. code:: python

    import pandas as pd
   from quartic_sdk.model import BaseReckonExpression
   from quartic_sdk import GraphqlClient

   import pandas as pd


   class ReckonExpression(BaseReckonExpression):
      @BaseReckonExpression.with_window(duration=1800)
      def evaluate(self, input_df: pd.DataFrame) -> pd.Series:
         return input_df['5']*2
      



   test_exp = ReckonExpression()

   test_df = pd.DataFrame([{'5': 10}])

   api_client = GraphqlClient(url="serverUrl", username="user", password="password")
   test_exp.save(api_client,
   output_tag_name="softtag1_output",
   needs=["5"],
   asset=279,
   is_streaming=True,
   tag_category=1,
   test_df = test_df)
.. raw:: html


