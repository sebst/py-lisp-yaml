from pylisp import *


class CookingParser(Parser):
    def __init__(self, data):
        self.data = data
        self._store = {}
        self._ingredients = []


    def exposed_ingredients(self, arg):
        print("IGR", arg)
        what = self.exec_line(arg)
        print("ING", what[0])
    
    def exposed_what(self, *args, **kwargs):
        return super().exposed_what(*args, **kwargs)

    exposed_qty = exposed_name = exposed_what



if __name__=="__main__":
    from tempfile import TemporaryFile
    from yaml import load, dump
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    data = load(open('recipe.yml', 'r'), Loader=Loader)

    parser = CookingParser(data)
    parser.run()