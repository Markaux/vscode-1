class Property:
    
    def __init__(self, var, string):
        ## initializing the attribute
        self.a = var
        self.b = string

    @property
    def a(self):
        return self.__a

    @property
    def b(self):
        return self.__b


    ## the attribute name and the method name must be same which is used to set the value for the attribute
    @a.setter
    def a(self, var):
        if var > 0 and var % 2 == 0:
            self.__a = var
        else:
            self.__a = 2

    @b.setter
    def b(self, string):
        if len(string) > 3:
            self.__b = "C'est cool"
        else:
            self.__b = "C'est pas cool"

## Main
obj = Property(100,"aa")
print(obj.a)
print(obj.b)