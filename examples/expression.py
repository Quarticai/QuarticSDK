import pandas as pd
from quartic_sdk.model import BaseReckonExpression
from quartic_sdk import GraphqlClient

import pandas as pd


class ReckonExpression(BaseReckonExpression):
    def evaluate(self, input_df: pd.DataFrame) -> pd.Series:
        return input_df['5']*2
    



test_exp = ReckonExpression()

test_df = pd.DataFrame([{'5': 10}])

api_client = GraphqlClient(url="http://localhost:8070/graphql", username="Hari D", password="Hari1402")
test_exp.save(api_client,
 output_tag_name="softtag1_output",
  needs=["5"],
  asset=279,
  is_streaming=True,
  tag_category=1,
  test_df = test_df)
