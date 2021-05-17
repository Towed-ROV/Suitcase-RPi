from unittest.test.testmock.testpatch import function


class nmea_sensor:
    def __init__(self, id:str, name:str, structure:list,condition:function = None):

        """
        future desing for nmea structure, not implemented.
        Args:
            id:
            name:
            structure:
        """
        self.id = id
        self.name = name
        self.structure = structure

        self.has_condition = False
        if condition:
            self.has_condition = True
            self.condition = condition
        else:
            self.condition = lambda x:x
