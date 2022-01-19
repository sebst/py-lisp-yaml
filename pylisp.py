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
        # print("EXEC LINE", line)
        if type(line) == str or type(line) == int:
            return self.str_or_func(line)
        name = list(line.keys())[0]
        fn = self.__getattribute__("exp_"+name)
        return fn(line[name])


    def str_or_func(self, x):
        # print("aaaaa", x)
        try:
            fn = self.__getattribute__("exp_"+x)
            return fn()
        except Exception as e:
            if isinstance(e, ControlException):
                raise e
            return x


    def exp_break(self, *args):
        raise BreakException


    def exp_get_store(self, *args, **kwargs):
        fr = args[0][0]
        s = self.exp_what(fr)
        try:
            return self._store.get(s)
        except:
            print("ERR", s)


    def exp_store(self, *args, **kwargs):
        kwargs = (args[0][0] | args[0][1])
        self._store[kwargs['to']] = self.exp_what(kwargs['what'])


    def exp_input(self):
        return input("Please enter some value:")


    def exp_what(self, *args, **kwargs):
        # print("what", args)
        assert len(args) == 1
        arg = args[0]
        if type(arg) == dict:
            return self.exec_line(arg)
        if type(arg) == list:
            res = [self.exec_line(code) for code in arg]
            return res[0] if len(res) == 1 else res
        else:
            res = arg
        # return self.str_or_func(res)
        return self.exec_line(res)
        # try:
        #     return self.exec_line(res)
        # except AttributeError:
        #     print("LLLLLLL", res)
        #     return self.str_or_func(res)


    exp_from = exp_else = exp_then = exp_val1 = exp_val2 = exp_what


    def exp_helloworld(self, *args):
        print("Hello World")


    def exp_say(self, *args, **kwargs):
        for arg in args:
            for code in arg:
                what = self.exec_line(code)
        print(what)


    def exp_ifeq(self, arg):
        # val1, val2, then = [self.exec_line(i) for i in arg[0]]
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


    def exp_repeat(self, arg):
        n = arg[0]
        # print("rre", arg[1:])
        for code in arg[1:]:
            for i in range(int(n)):
                # print("code", code)
                try:
                    self.exec_line(code)
                except BreakException:
                    break


    def exp_concat(self, arg):
        s  = ""
        for code in arg:
            s += str(self.exp_what(code))
        return s


    def exp_plus(self, arg):
        return sum(int(self.exp_what(code)) for code in arg)


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