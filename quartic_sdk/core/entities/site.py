"""
The given file contains the class to refer to the Site entity
"""
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants


class Site(Base):
    """
    The given class refers to the site entity which is created based upon the site response
    returned by the API
    """

    def __repr__(self):
        """
        Override the method to return the site name
        """
        return f"<{Constants.SITE_ENTITY}: {self.name}>"

    def assets(self):
        """
        Get the assets belongs to a site
        """
        raise NotImplementedError

    def edge_connectors(self):
        """
        Get the edge_connectors belongs to a site
        """
        raise NotImplementedError
