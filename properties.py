
class Property:
    def __init__(self, name, value, base_tax, owner=None):
        self.__name = name
        self.__value = value
        self.__base_tax = base_tax
        self.owner = owner
        self.__rent_multipliers = [1, 5, 15, 45, 80, 125]
        self.rent_idx = 0
    
    def set_name(self, name):
        self.__name = name
    
    def get_name(self):
        return self.__name
    
    def set_value(self, value):
        self.__value = value
    
    def get_value(self):
        return self.__value
    
    def set_base_tax(self, base_tax):
        self.__base_tax = base_tax

    def get_base_tax(self):
        return self.__base_tax

    def get_tax_multiplier(self):
        return self.__rent_multipliers[self.rent_idx]
    
    def upgrade(self):
        self.rent_idx += 1