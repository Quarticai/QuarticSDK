"""
The given file contains the class to refer to the tag entity
"""
from quartic_sdk.core.entities.base import Base
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.iterators.tag_data_iterator import TagDataIterator
from quartic_sdk.utilities.exceptions import IncorrectTagParameterException,IncorrectWavelengthParamException


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
    @staticmethod
    def raise_exception_for_wavelegths(wavelengths):
        """
        Validate wavelengths passed for a spectral tag. Schema as following
        {"wavelengths" : ['1460000.0','1460001.0]}
        :param wavelengths: dict containing key as 'wavelengths' and value as list of wavelengths
        """
        assert isinstance(wavelengths, dict), "Wavelengths must be a dict"
        
        if not wavelengths.get('wavelengths'):
            raise IncorrectWavelengthParamException(
                'Invalid Wavelengths: "wavelengths" key required in dict'
            )
        elif not isinstance(wavelengths.get("wavelengths"), list):
            raise IncorrectWavelengthParamException(
                'Invalid Wavelengths: Wavelength values must be passed in a list '
            )


    def __repr__(self):
        """
        Override the method to return the tag name
        """
        return f"<{Constants.TAG_ENTITY}: {self.name}>"

    def data(
            self,
            start_time,
            stop_time,
            sampling_ratio=1,
            return_type=Constants.RETURN_PANDAS,
            batch_size=Constants.DEFAULT_PAGE_LIMIT_ROWS,
            wavelengths = {},
            transformations=[]):
        """
        Get the data for the given tag between the start_time and the stop_time
        for the given sampling_ratio
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param sampling_ratio: sampling_ratio of the data
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
        :param wavelengths: dict containing list of wavelengths(string) as value with key "wavelengths"
            Used for getting data for a spectral tag for specified wavelengths. 
            An example value here is:
            {"wavelengths:['1460000.0','1460001.0']}   
        :param transformations: Refers to the list of transformations. It supports either
            interpolation or aggregation, depending upon which, we pass the value of this
            dictionary. If `transformation_type` is "aggregation", an optional key can be
            passed called `aggregation_timestamp`, which determines how the timestamp information
            will be retained after aggregation. Valid options are "first", "last" or "discard". By
            default, the last timestamp in each group will be retained.
            An example value here is:
            [{
                "transformation_type": "interpolation",
                "column": "3",
                "method": "linear"
            }, {
                "transformation_type": "aggregation",
                "aggregation_column": "4",
                "aggregation_dict": {"3": "max"},
                "aggregation_timestamp": "last",
            }]
        :return: (DataIterator) DataIterator object which can be iterated to get the data
            between the given duration
        """
        from quartic_sdk.core.entity_helpers.entity_list import EntityList       
        if wavelengths and self.tag_data_type !=  Constants.TAG_DATA_TYPES[6]:
            raise IncorrectTagParameterException( "Invalid parameters : Wavelengths are only supported with spectral tag type")                    
        if wavelengths:
            Tag.raise_exception_for_wavelegths(wavelengths)
        return TagDataIterator.create_tag_data_iterator(
            EntityList(
                Constants.TAG_ENTITY,
                [self]),
            start_time,
            stop_time,
            self.api_helper,
            sampling_ratio,
            return_type,
            batch_size,
            wavelengths,
            transformations)

    def wavelengths(self, graphql_client, start_time=None, stop_time=None):
        """
        This method is used to get the list of wavelengths of a spectral tag within
        the provided start and stop times. if start, stop times are not provided, by 
        default it will fetch all available wavelengths.
        :param: graphql_client: instance of GraphqlClient
        :param: start_time(epoch): Optional 
        :param: stop_time(epoch): Optional
        :return: dict containing list of wavelengths or error message and status from server
        """
        request_body = {"tagId" : self.id}
        if start_time:
            request_body["startTime"] = start_time
        if stop_time:
            request_body["stopTime"] = stop_time

        return graphql_client.execute_query(Constants.GET_TAG_WAVELENGTHS,request_body)

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
