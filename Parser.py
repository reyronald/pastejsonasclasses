""" TODO docstring """

import json
import collections
from queue import Queue
from dateutil.parser import parse
from ClassProperty import ClassProperty

#pp = pprint.PrettyPrinter(indent=4)


class Parser:
    """ TODO docstring """

    def get_classes(json_string):
        """ TODO docstring """

        try:
            json_dictionary = json.loads(json_string, object_pairs_hook=collections.OrderedDict)
        except json.JSONDecodeError as json_decode_error:
            error_message = ""
            error_message += "Paste JSON As Classes\r\n"
            error_message += "The content in the clipboard isn't a valid JSON instance. "
            error_message += "Please fix the issue and try again:\r\n"
            error_message += json_decode_error.args[0]
            print(error_message)
            raise ValueError(error_message)

        classes_to_properties = Parser.parse(json_dictionary)

        result = ''
        for class_name, class_properties in classes_to_properties.items():
            result += 'public class %s\n' % class_name
            result += '{\n'
            for class_property in class_properties:
                type_name = class_property.type_name + '?' if class_property.is_nullable else class_property.type_name
                if not class_property.is_array:
                    to_replace_tuple = (type_name, class_property.property_name)
                else:
                    to_replace_tuple = (type_name + '[]', class_property.property_name)
                result += "\tpublic %s %s { get; set; }\n" % to_replace_tuple
            result += '}\n\n'

        return result

    def parse(json_dictionary):
        """ TODO docstring """

        classes = Queue()
        classes.put(json_dictionary)

        classes_to_properties = collections.OrderedDict()
        current_class_name = 'Rootobject'

        get_first_or_none = lambda list: next((x for x in list if x is not None), None)

        while not classes.empty():
            current_class = classes.get()
            properties = []
            next_class_name = ''

            if isinstance(current_class, list):
                first_non_null = get_first_or_none(current_class)
                constructed_class_with_no_nulls = first_non_null
                is_property_nullable = {}
                current_class_without_nulls = [x for x in current_class if x is not None]
                for element_key, element_value in first_non_null.items():
                    plucked_element_values = list((x[element_key] for x in current_class_without_nulls))
                    constructed_class_with_no_nulls[element_key] = get_first_or_none(plucked_element_values)
                    is_property_nullable[ element_key ] = any(element is None for element in plucked_element_values)
                                 
                array_elements_class_properties = Parser.parse(constructed_class_with_no_nulls)['Rootobject']
                for y in array_elements_class_properties:
                    properties.append(ClassProperty(y.type_name, y.property_name, y.is_array, is_property_nullable[ y.property_name]))
                current_class_name = singular_key
            else:
                for key, value in current_class.items():

                    # Value is an object
                    if isinstance(value, collections.OrderedDict):
                        properties.append(ClassProperty(key, key, False, False))
                        classes.put(value)
                        next_class_name = key

                    # Value is an array
                    elif isinstance(value, list):
                        is_array = True
                        first_non_null = get_first_or_none(value)

                        # The array is an array of primitives
                        if not isinstance(first_non_null, collections.OrderedDict):
                            is_nullable = any(element is None for element in value) if first_non_null is not None else False
                            properties.append(Parser.get_primitive_class_property(first_non_null, key, is_array, is_nullable))

                        # The array is an array of objects
                        else:
                            singular_key = Parser.plural_to_singular(key)
                            properties.append(ClassProperty(singular_key, key, is_array, False))
                            classes.put(value)
                            next_class_name = singular_key

                    # Value is a primitive
                    else:
                        properties.append(Parser.get_primitive_class_property(value, key, False, False))

            classes_to_properties[current_class_name] = properties
            current_class_name = next_class_name

        return classes_to_properties

    def get_primitive_class_property(value, key, is_array, is_nullable):
        if not isinstance(value, str):
            class_property = ClassProperty(type(value).__name__, key, is_array, is_nullable)
        else:   
            try:
                date = parse(value)
                class_property = ClassProperty(type(date).__name__, key, is_array, is_nullable)
            except ValueError as e:
                class_property = ClassProperty(type(value).__name__, key, is_array, is_nullable)
        return class_property

    def plural_to_singular(word):
        """ Receives a plural word and returns its singular representation """
        if word == 'people':
            return 'person'
        elif word == 'elements':
            return 'element'

        return word
