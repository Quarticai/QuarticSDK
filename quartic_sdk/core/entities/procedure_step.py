"""
The given file contains the class to refer to the ProcedureStep entity
"""
from requests import HTTPError
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants


class ProcedureStep(Base):
    """
    The given class refers to the ProcedureStep entity which is created based upon the
    procedure step response returned by the API
    """

    def __repr__(self):
        """
        Override the method to return the ProcedureStep name
        """
        return f"<{Constants.PROCEDURE_STEP_ENTITY}: {self.name}>"

    def fetch_substep_details(self, query_params={}):
        """
        This method is used for fetching procedure substep details like Operation/Phase/PhaseStep
        :param query_params: Dictionary of filter conditions
        :return: List of ProcedureStep(ProcedureStep Entity) Objects
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory

        query_params['parent'] = self.id
        return_json = self.api_helper.call_api(
            Constants.PROCEDURE_STEPS, Constants.API_GET, query_params=query_params).json()
        return EntityFactory(Constants.PROCEDURE_STEP_ENTITY, return_json, self.api_helper)

    def create_procedure_step(
            self,
            name,
            start_batch_tag,
            stop_batch_tag,
            procedure,
            order,
            start_rule,
            stop_rule,
            asset_list
    ):
        """
        This method is used to create Procedure Step like Operation/Phase/PhaseStep
        :param name: ProcedureStep Name
        :param start_batch_tag: Tag Object
        :param stop_batch_tag: Tag Object
        :param procedure: Procedure Object
        :param order: Sequence in which we want to add child nodes inside parent(UnitProcedure/Operation/Phase) node
        :param start_rule: Rule (Util Class) Object
        :param stop_rule: Rule (Util Class) Object
        :param asset_list: List containing asset ids
        :return: ProcedureStep(ProcedureStep Entity) Object
        """
        from quartic_sdk.core.entity_helpers.entity_factory import EntityFactory
        try:
            start_rule.validate_rule_raw_json()
            stop_rule.validate_rule_raw_json()

            procedure_step_request_body = {
                "name": name,
                "start_batch_tag": start_batch_tag.id,
                "stop_batch_tag": stop_batch_tag.id,
                "step_type": self.step_type + 1,
                "procedure": procedure.id,
                "order": order,
                "start_rule": start_rule.rule_schema(),
                "stop_rule": stop_rule.rule_schema(),
                "assets": asset_list,
                "parent": self.id
            }

            unit_procedure_creation_response = self.api_helper.call_api(
                Constants.PROCEDURE_STEPS,
                method_type=Constants.API_POST,
                body=procedure_step_request_body
            ).json()

            return EntityFactory(Constants.PROCEDURE_STEP_ENTITY, unit_procedure_creation_response, self.api_helper)
        except HTTPError as exception:
            raise Exception(f'Exception in creating Unit Procedure: {exception.response.content.decode()}')
