
import quartic_sdk.utilities.constants as Constants
from quartic_sdk.core.entities.type_mapping import ENTITY_DICTIONARY
from quartic_sdk.core.iterators.entity_list_iterator import EntityListIterator
from quartic_sdk.utilities.tag_data import TagData
import operator


class EntityList:
    """
    The given class refers to the list of specific `class_type` of entity
    """

    def __init__(self, class_type, entities_list=[]):
        """
        We initialize the `BaseEntityList` based upon the class_type and the
        entities_list as passed by the user
        """
        self._class_type = class_type
        self._entities = []
        for entity_obj in entities_list:
            if self._validate_type(entity_obj):
                self._entities.append(entity_obj)

    def __repr__(self):
        """
        Return the representation of the entitylist
        """
        str_repr = "<EntityList: ["
        for entity_obj in self._entities:
            str_repr = str_repr + str(entity_obj) + ", "
        str_repr += "]>"
        return str_repr

    def __str__(self):
        """
        Return the stringified representation of the entitylist
        """
        return self.__repr__()

    def _validate_type(self, instance):
        """
        We validate that the type of the object is the same as defined for the
        class definition
        """
        return isinstance(instance, ENTITY_DICTIONARY[self._class_type])

    def get(self, name, value):
        """
        We return the entity with the given value for the name of the attribute
        """
        return [
            entity for entity in self._entities if getattr(
                entity, name) == value][0]

    def all(self):
        """
        We return the list of all entities for the given object
        """
        return self._entities

    def first(self):
        """
        Return the first element of the list
        """
        return self._entities[0]

    def last(self):
        """
        Return the last element of the list
        """
        return self._entities[-1]

    def count(self):
        """
        Returns the length of all entities
        """
        return len(self._entities)

    def filter(self, **kwargs):
        """
        We filter the entities based upon the given conditions
        There might be multiple conditions
        :param kwargs: Dict which maps `filter_key` to filter_value
                       The `filter_key` can be decomposed into two parts: (attribute, operator)
                       For instance, if `filter_key` is `created_at__lt` then ('created_at', 'lt')
                       It might also be a simple query where we check for equality, then `filter_key` is simply the attribute name
        """
        filtered_entities = self._entities
        negate = kwargs.pop('_negate') if '_negate' in kwargs else False
        for filter_key in kwargs:
            filter_attribute, filter_operator = filter_key.split('__') if '__' in filter_key else (filter_key, 'eq')
            filter_func = lambda x, y: not getattr(operator, filter_operator)(x, y) if negate else getattr(operator, filter_operator)(x, y)
            filtered_entities = list(filter(lambda entity: filter_func(getattr(entity, filter_attribute), kwargs[filter_key]), filtered_entities))
        return EntityList(self._class_type, filtered_entities)

    def check_object_in_list(self, instance):
        """
        We check whether the instance is already in the list
        :param instance: Object that is to be added to the list
        """
        if not self._validate_type(instance):
            raise Exception(
                "Object data type is not present in the entity list")
        return instance.id in [entity.id for entity in self._entities]

    def add(self, instance):
        """
        We add the given object instance to the entities list of the class
        """
        if not self.check_object_in_list(instance):
            self._entities.append(instance)
        else:
            raise AssertionError(
                f"Can not add object, since it is not of {self._class_type} type")

    def exclude(self, **kwargs):
        """
        We return the EntityList after removing the entities with the attributes having the given values
        :param kwargs: Dict which maps `filter_key` to filter_value
        """
        return self.filter(**kwargs, _negate=True)

    def __iter__(self):
        """
        We override the iterator to allow the user to iterate on the class
        """
        return EntityListIterator(self)

    def __getitem__(self, key):
        """
        Override the method to get the entity list value at the given index
        """
        return self._entities[key]

    def __eq__(self, other):
        """
        Check equality of two entity list objects
        """
        assert isinstance(other, EntityList)
        assert other._class_type == self._class_type
        return self.count() == other.count() and all(
            self[index] in other.all() for index in range(self.count()))

    def __bool__(self):
        """
        Override to get the bool value of the class if required
        """
        return self.count() > 0

    def data(self, start_time, stop_time, interval_min=1, aggregation_type="last", wide_df=True, return_type=Constants.RETURN_PANDAS,
             transformations=[]):
        """
        Get the data of all tags in the list between the given start_time and
        stop_time for the given interval duration
        :param start_time: (epoch) Start_time for getting data
        :param stop_time: (epoch) Stop_time for getting data
        :param interval_min: (int) The interval duration in minutes for downsampling the data
        :param aggregation_type: (str) The aggregation function to be used for the query. (Valid values: first, last)
        :param wide_df: (bool) If the response is needed in wide or long format. Defaults to True.
        :param return_type: The param decides whether the data after querying will be
            json(when value is "json") or pandas dataframe(when value is "pd"). By default,
            it takes the value as "json"
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
        assert self._class_type == Constants.TAG_ENTITY
        return TagData.get_tag_data(tags=self, start_time=start_time, stop_time=stop_time,
                                    interval_min=interval_min, aggregation_type=aggregation_type,
                                    api_helper=self.first().api_helper, wide_df=wide_df, 
                                    return_type=return_type, transformations=transformations)
