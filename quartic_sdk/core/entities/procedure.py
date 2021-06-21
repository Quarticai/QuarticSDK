"""
The given file contains the class to refer to the Procedure entity
"""
from requests import HTTPError
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants


class Procedure(Base):
    """
    The given class refers to the Procedure entity which is created based upon the procedure response
    returned by the API
    """
    UNIT_PROCEDURE = 1

    def __repr__(self):
        """
        Override the method to return the Procedure name
        """
        return f"<{Constants.PROCEDURE_ENTITY}: {self.name}>"

    def fetch_unit_procedures(self, query_params={}):
        """
        This method is used for fetching all the UnitProcedures belongs to a particular procedure
        in PH hierarchy
        :param query_params: Dictionary of filter conditions
        :return: List of UnitProcedure(ProcedureStep Entity) Objects
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory

        query_params.update({
            "procedure": self.id,
            "step_type": self.UNIT_PROCEDURE
        })
        return_json = self.api_helper.call_api(
            Constants.PROCEDURE_STEPS, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.PROCEDURE_STEP_ENTITY, return_json, self.api_helper)

    def create_unit_procedure(
            self,
            name,
            start_batch_tag,
            stop_batch_tag,
            order,
            start_rule,
            stop_rule,
            asset_list
    ):
        """
        This method is used to create UnitProcedure inside a particular Procedure
        :param name: UnitProcedure Name
        :param start_batch_tag: Tag Object
        :param stop_batch_tag: Tag Object
        :param order: sequence in which we want to add child nodes inside parent(procedure) node
        :param start_rule: Rule (Util Class) Object
        :param stop_rule: Rule (Util Class) Object
        :param asset_list: List containing asset ids
        :return: UnitProcedure(ProcedureStep Entity) Object
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        try:
            start_rule.validate_rule_raw_json()
            stop_rule.validate_rule_raw_json()

            unit_procedure_request_body = {
                "name": name,
                "start_batch_tag": start_batch_tag.id,
                "stop_batch_tag": stop_batch_tag.id,
                "step_type": self.UNIT_PROCEDURE,
                "procedure": self.id,
                "order": order,
                "start_rule": start_rule.rule_schema(),
                "stop_rule": stop_rule.rule_schema(),
                "assets": asset_list
            }

            unit_procedure_creation_response = self.api_helper.call_api(
                Constants.PROCEDURE_STEPS,
                method_type=Constants.API_POST,
                body=unit_procedure_request_body
            ).json()

            return EntityFactory(Constants.PROCEDURE_STEP_ENTITY, unit_procedure_creation_response, self.api_helper)
        except HTTPError as exception:
            raise Exception(f'Exception in creating Unit Procedure: {exception.response.content.decode()}')
