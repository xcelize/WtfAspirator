class Base:

    def __init__(self, json_object):
        self.mapping_attr = {}
        self.mapping_nested = {}

    def _assign_attr(self, json_object):
        for attribut in json_object:
            for map_attribut in self.mapping_attr:
                if attribut == self.mapping_attr[map_attribut]:
                    setattr(self, map_attribut, json_object[attribut])

    def _assign_nested(self, json_object):
        for attribut in json_object:
            for map_attribut in self.mapping_nested:
                if attribut == self.mapping_nested[map_attribut]['json_attr']:
                    for obj in json_object[attribut]:
                        nested_object = self.mapping_nested[map_attribut]['model'](obj)
                        self.mapping_nested[map_attribut]['object_attr'].append(nested_object)

    def Pk(self):
        raise NotImplementedError()