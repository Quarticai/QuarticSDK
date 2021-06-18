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

    def create_procedure(
            self,
            name,
            site,
            start_batch_tag,
            stop_batch_tag,
            additional_attributes,
            start_rule,
            stop_rule
    ):
        """
        This method is used for creating procedure of PH hierarchy inside particular product
        :param name: Procedure Name
        :param site: Site Object
        :param start_batch_tag: Tag Object
        :param stop_batch_tag: Tag Object
        :param additional_attributes: Additional attributes required to create procedure in the dictionary format
        and contains fields of Procedure like receipe_type, formula and receipe_version
        :param start_rule: Rule Class Object
        :param stop_rule: Rule Class Object
        :return: Procedure(Procedure Entity) Object
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        try:
            start_rule.validate_rule_raw_json()
            stop_rule.validate_rule_raw_json()

            procedure_post_request_body = {
                "name": name,
                "site": site.id,
                "start_batch_tag": start_batch_tag.id,
                "stop_batch_tag": stop_batch_tag.id,
                "additional_attributes": additional_attributes,
                "product": self.id,
                "start_rule": start_rule.rule_schema(),
                "stop_rule": stop_rule.rule_schema()
            }

            procedure_creation_response = self.api_helper.call_api(
                Constants.PROCEDURES,
                method_type=Constants.API_POST,
                body=procedure_post_request_body
            ).json()
            return EntityFactory(Constants.PROCEDURE_ENTITY, procedure_creation_response, self.api_helper)

        except HTTPError as exception:
            raise Exception(f'Exception in creating Procedure: {exception.response.content.decode()}')
