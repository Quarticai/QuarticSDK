"""
The given file contains the class to refer to the tag entity
"""
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator


class Tag(Base):
    """
    The given class refers to the tag entity which is created based upon the
    tag object returned from the API
    """

    mapping = {
        "tag_type": Constants.TAG_TYPES,
        "tag_data_type": Constants.TAG_DATA_TYPES,
        "tag_value_type": Constants.TAG_VALUE_TYPES,
        "tag_process_type": Constants.PROCESS_VARIABLE_TYPES,
        "category": Constants.INTELLIGENCE_CATEGORIES
    }

    def __repr__(self):
        """
        Override the method to return the tag name with id
        """
        return f"<{Constants.TAG_ENTITY}: {self.name}_{self.id}>"

    def data(
            self,
            start_time,
            stop_time,
            granularity=0,
            return_type=Constants.RETURN_PANDAS,
            transformations=[]):
        """
        Get the data for the given tag between the start_time and the stop_time
        for the given granularity
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param granularity: Granularity of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"}
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        from quartic_sdk.core.entity_helpers.entity_list import EntityList
        return TagDataIterator.create_tag_data_iterator(
            EntityList(
                Constants.TAG_ENTITY,
                [self]),
            start_time,
            stop_time,
            self.api_helper,
            granularity,
            return_type,
            transformations)

    def __getattribute__(self, name):
        """
        This method overrides the python's object __getattribute__ method. This is used to
        map some constant value of an object to some meaningful string constants for better
        readability
        :param name: name of the object attribute we want to access for example tag.tag_type
        :return: Either mapped value or raw value with respect to the object attribute
        """
        tag_mapping = Tag.mapping
        if name in tag_mapping.keys() and tag_mapping[name].get(self.__dict__[name]):
            return tag_mapping[name][self.__dict__[name]]
        return object.__getattribute__(self, name)
