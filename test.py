""" TODO docstring """

import unittest
from Parser import Parser

class Test(unittest.TestCase):
    """ TODO docstirng """

    def run_tests(self):
        """ TODO docstring """

        #self.string_type()
        #self.int_type()
        #self.float_type()
        #self.bool_type()
        #self.datetime_type()
        #self.string_array_type()
        #self.custom_type()
        self.datetime_type()

    def compare(self, input_json_string, expected_output):
        """ TODO docstring """

        output = Parser.get_classes(input_json_string)
        self.assertEqual(expected_output.strip(), output.strip())

    """
    String type
    """
    def string_type(self):
        """ String type """

        input_json_string = """{ "name": "John Doe" }"""
        expected_output = """public class Rootobject
{
	public str name { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    Int type
    """
    def int_type(self):
        """ Int type """

        input_json_string = """{ "amount": 10 }"""
        expected_output = """public class Rootobject
{
	public int amount { get; set; }
}"""
        self.compare(input_json_string, expected_output)
        
    """
    Float type
    """
    def float_type(self):
        """ Float type """

        input_json_string = """{ "price": 499.99 }"""
        expected_output = """public class Rootobject
{
	public float price { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    Bool type
    """
    def bool_type(self):
        """ Bool type """

        input_json_string = """{ "active": true }"""
        expected_output = """public class Rootobject
{
	public bool active { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    Null (object) type
    """
    def null_type(self):
        """Null (object) type"""

        input_json_string = """{ "name": null }"""
        expected_output = """public class Rootobject
{
	public NoneType name { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    DateTime type
    """
    def datetime_type(self):
        """ DateTime type """

        input_json_string = """{ "createdDate": "2012-05-03T00:06:00.638Z" }"""
        expected_output = """public class Rootobject
{
	public NoneType name { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    String[] type
    """
    def string_array_type(self):
        """ String[] type """
        input_json_string = """{
    "names": ["ronald","rey"]
}"""
        expected_output = """public class Rootobject
{
	public str[] names { get; set; }
}"""
        self.compare(input_json_string, expected_output)

    """
    Custom type
    """
    def custom_type(self):
        """ Custom type """
        input_json_string = """
        {
            "glossary": {
                "title": "example glossary",
                "GlossDiv": {
                    "title": "S",
                    "GlossList": {
                        "GlossEntry": {
                            "ID": "SGML",
                            "SortAs": "SGML",
                            "GlossTerm": "Standard Generalized Markup Language",
                            "Acronym": "SGML",
                            "Abbrev": "ISO 8879:1986",
                            "GlossDef": {
                                "para": "A meta-markup language, used to create markup languages such as DocBook."
                            },
                            "GlossSee": "markup"
                        }
                    }
                }
            }
        }
        """
        expected_output = """public class Rootobject
{
	public glossary glossary { get; set; }
}

public class glossary
{
	public str title { get; set; }
	public GlossDiv GlossDiv { get; set; }
}

public class GlossDiv
{
	public str title { get; set; }
	public GlossList GlossList { get; set; }
}

public class GlossList
{
	public GlossEntry GlossEntry { get; set; }
}

public class GlossEntry
{
	public str ID { get; set; }
	public str SortAs { get; set; }
	public str GlossTerm { get; set; }
	public str Acronym { get; set; }
	public str Abbrev { get; set; }
	public GlossDef GlossDef { get; set; }
	public str GlossSee { get; set; }
}

public class GlossDef
{
	public str para { get; set; }
}
"""
        self.compare(input_json_string, expected_output)

    """
    Custom[] type
    """
    def custom_array_type(self):
        """ Custom[] type """

        input_json_string = """{ "people": [ {"name": "Ronald"} ] }"""
        expected_output = """public class Rootobject
{
	public person[] people { get; set; }
}

public class person
{
	public str name { get; set; }
}"""
        self.compare(input_json_string, expected_output)

if __name__ == '__main__':
    unittest.main()