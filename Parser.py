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

        while not classes.empty():
            current_class = classes.get()
            properties = []
            next_class_name = ''
            for key, value in current_class.items():

                # Value is an object
                if isinstance(value, collections.OrderedDict):
                    properties.append(ClassProperty(key, key, False, False))
                    classes.put(value)
                    next_class_name = key

                # Value is an array
                elif isinstance(value, list):
                    # The array is an array of objects
                    if isinstance(value[0], collections.OrderedDict):
                        singular_key = Parser.plural_to_singular(key)
                        properties.append(ClassProperty(singular_key, key, True, False))
                        classes.put(value[0])
                        next_class_name = singular_key

                    # The array is an array of primitives
                    else:
                        first_non_null = next((x for x in value if x is not None), None)
                        is_nullable = any(element is None for element in value) if first_non_null is not None else False
                        properties.append(Parser.get_primitive_class_property(first_non_null, key, True, is_nullable))

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

        return word
