class ClassProperty(object):
    """ TODO docstring """

    def __init__(self, type_name, property_name, is_array, is_nullable):
        """ TODO docstring """
        self.type_name = type_name
        self.property_name = property_name
        self.is_array = is_array
        self.is_nullable = is_nullable