class ControlException(Exception): pass
class BreakException(ControlException): pass


class Parser:
    def __init__(self, data):
        self.data = data
        self._store = {}


    def run(self):
        for line in self.data:
            self.exec_line(line)


    def exec_line(self, line):
        if type(line) == str or type(line) == int:
            return self.str_or_func(line)
        name = list(line.keys())[0]
        fn = self.__getattribute__("exposed_"+name)
        return fn(line[name])


    def str_or_func(self, x):
        try:
            fn = self.__getattribute__("exposed_"+x)
            return fn()
        except Exception as e:
            if isinstance(e, ControlException):
                raise e
            return x


    def exposed_break(self, *args):
        raise BreakException


    def exposed_get_store(self, *args, **kwargs):
        fr = args[0][0]
        s = self.exposed_what(fr)
        try:
            return self._store.get(s)
        except:
            print("ERR", s)


    def exposed_store(self, *args, **kwargs):
        kwargs = (args[0][0] | args[0][1])
        self._store[kwargs['to']] = self.exposed_what(kwargs['what'])


    def exposed_input(self):
        return input("> ")


    def exposed_what(self, *args, **kwargs):
        assert len(args) == 1
        arg = args[0]
        if type(arg) == dict:
            return self.exec_line(arg)
        if type(arg) == list:
            res = [self.exec_line(code) for code in arg]
            return res[0] if len(res) == 1 else res
        else:
            res = arg
        return self.exec_line(res)


    exposed_from = exposed_else = exposed_then = exposed_val1 = exposed_val2 = exposed_what


    def exposed_helloworld(self, *args):
        print("Hello World")


    def exposed_say(self, *args, **kwargs):
        for arg in args:
            for code in arg:
                what = self.exec_line(code)
        print(what)


    def exposed_ifeq(self, arg):
        val1 = self.exec_line(arg[0])
        val2 = self.exec_line(arg[1])
        if str(val1) == str(val2):
            then = self.exec_line(arg[2])
            return then
        else:
            try:
                otherwise = self.exec_line(arg[3])
            except IndexError:
                pass
            except:
                raise


    def exposed_repeat(self, arg):
        n = arg[0]
        for code in arg[1:]:
            for _ in range(int(n)):
                try:
                    self.exec_line(code)
                except BreakException:
                    break


    def exposed_concat(self, arg):
        s  = ""
        for code in arg:
            s += str(self.exposed_what(code))
        return s


    def exposed_plus(self, arg):
        return sum(int(self.exposed_what(code)) for code in arg)


if __name__=="__main__":
    from tempfile import TemporaryFile
    from yaml import load, dump
    try:
        from yaml import CLoader as Loader, CDumper as Dumper
    except ImportError:
        from yaml import Loader, Dumper

    data = load(open('first_app.yml', 'r'), Loader=Loader)

    parser = Parser(data)
    parser.run()
