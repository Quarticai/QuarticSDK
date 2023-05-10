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
