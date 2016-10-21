import json
import collections
from queue import *

#pp = pprint.PrettyPrinter(indent=4)

class Parser:
    def get_classes(jsonString):
        classesToProperties = Parser.parse(jsonString)

        result = ''
        for className, classProperties in classesToProperties.items():
            result += 'public class %s\r\n' % className
            result += '{\r\n'
            for classProperty in classProperties:
                result += "\tpublic %s %s { get; set; }\r\n" % classProperty
            result += '}\r\n'

        return result

    def parse(jsonString):
        try:
            input = json.loads(jsonString, object_pairs_hook=collections.OrderedDict)
        except json.JSONDecodeError as e:
            error_message = ""
            error_message += "Paste JSON As Classes\r\n"
            error_message += "The content in the clipboard isn't a valid JSON instance. Please fix the issue and try again:\r\n"
            error_message += e.args[0]
            print(error_message)
            raise ValueError(error_message)

        classes = Queue()
        classes.put(input)

        classesToProperties = collections.OrderedDict()
        currentClassName = 'Rootobject'

        while (not classes.empty()):
            currentClass = classes.get()
            properties = []
            nextClassName = ''
            for key, value in currentClass.items():
                if (type(value) is collections.OrderedDict):
                    properties.append((key, key))
                    classes.put(value)
                    nextClassName = key
                else:
                    properties.append((type(value).__name__, key))
            classesToProperties[currentClassName] = properties
            currentClassName = nextClassName

        return classesToProperties

