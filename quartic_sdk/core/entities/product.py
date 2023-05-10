"""
The given file contains the class to refer to the Product entity
"""
from requests import HTTPError
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants


class Product(Base):
    """
    The given class refers to the product entity which is created based upon the product response
    returned by the API
    """

    def __repr__(self):
        """
        Override the method to return the product name
        """
        return f"<{Constants.PRODUCT_ENTITY}: {self.name}>"

    def get_procedures(self, query_params={}):
        """
        This method id used for fetching all the procedures belongs to a product
        :param query_params: Dictionary of filter conditions
        :return: List of Procedure(Procedure Entity) objects
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory

        query_params["product"] = self.id
        return_json = self.api_helper.call_api(
            Constants.PROCEDURES, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.PROCEDURE_ENTITY, return_json, self.api_helper)
