""" TODO docstring """

import json
import collections
from queue import Queue
from dateutil.parser import parse

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
                if not class_property['isArray']:
                    to_replace_tuple = (class_property['typeName'], class_property['propertyName'])
                else:
                    to_replace_tuple = (class_property['typeName'] + '[]', class_property['propertyName'])
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
                if isinstance(value, collections.OrderedDict):
                    properties.append({'typeName': key, 'propertyName': key, 'isArray': False})
                    classes.put(value)
                    next_class_name = key
                elif isinstance(value, list):
                    if isinstance(value[0], collections.OrderedDict):
                        singular_key = Parser.plural_to_singular(key)
                        properties.append({'typeName': singular_key, 'propertyName': key, 'isArray': True})
                        classes.put(value[0])
                        next_class_name = singular_key
                    else:
                        properties.append({'typeName': type(value[0]).__name__, 'propertyName': key, 'isArray': True})
                else:
                    if not isinstance(value, str):
                        properties.append({'typeName': type(value).__name__, 'propertyName': key, 'isArray': False})
                    else:   
                        try:
                            date = parse(value)
                            properties.append({'typeName': type(date).__name__, 'propertyName': key, 'isArray': False})
                        except ValueError as e:
                            properties.append({'typeName': type(value).__name__, 'propertyName': key, 'isArray': False})

            classes_to_properties[current_class_name] = properties
            current_class_name = next_class_name

        return classes_to_properties

    def plural_to_singular(word):
        """ Receives a plural word and returns its singular representation """
        if word == 'people':
            return 'person'

        return word
