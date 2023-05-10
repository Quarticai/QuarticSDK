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
