from printutils import *

from tkinter import *
import tkinter.ttk as ttk

debug = False
class Interpreter():
    version = 1.0
    def __init__(self, code, compile, load_mode, debug):
        self.code = code
        self.debug = debug

        self.actions = {}
        self.stack = {"log": ERRORS}
        self.cursor_line = 0
        self.compile = compile
        self.cursor_word = 0
        self.split_code = []
        self.split_code__ = []
        self.inspected_actions = []
        self.imports = []
        self.current_action = ""
        self.imported = []

        GLOBAL["in"] = self
        if load_mode != False:
            self.load(load_mode)
        else:
            self.init_pharse()

    def init_pharse(self):
        if self.debug:
            print("inspecting script actions")
        self.inspect_actions(self.code)
        if self.debug:
            print("inspecting imports")
        self.inspect_import(self.code)
        if self.debug:
            print(f"{self.actions.keys() = }")
            print(f"{self.stack = }")

        if self.compile:
            print("compiling...")
            self.save("main.gpx")
            print("saved as 'main.gpx'")
            print("use 'gpy main.gpx -load' to execute")
        else:
            self.runaction("global")
            if self.debug:
                print(f"using stdlib version {self.stack['stdlib_version']}")
                print("ENTERING RUNTIME\n")
            self.std_lines = 0
            self.runaction("main")
            if self.debug:
                print("----------EXIT---------")
                print(f"{self.actions = }")
                print("\n")
                print(f"{self.stack = }")
                print("\n")
                print(f"{self.inspected_actions = }")

    def save(self, filename):
        save = {"version": self.version, "sp_code": self.split_code, "actions": self.actions, "stack": self.stack}
        f = open(filename, "w")
        f.write(str(save))
        f.close()

    def load(self, filename):
        f = open(filename, "r")
        d = f.read()
        exec(f"global save_; save_ = {d}")
        f.close()
        if save_["version"] != self.version:
            print("INTERPRETER ERROR: VERSION WRONG")
            print(f"SCRIPT_VERSION: {save_['version']}")
            print(f"INTERPRETER_VERSION: {self.version}\n")
            input(">PRESS RETURN TO TRY EXECUTING THE CODE")
        self.split_code = save_["sp_code"]
        self.actions = save_["actions"]
        self.stack = save_["stack"]
        self.runaction("global")
        self.runaction("main")

    def inspect_import(self, code):
        self.split_code_ = code.splitlines()

        self.split_code__ = []
        for i in self.split_code_:
            self.split_code__.append(i.split(" "))

        for index, line in enumerate(self.split_code__):
            for index2, word in enumerate(line):
                if word == "@import":
                    file = line[index2 + 1]
                    if file not in self.imported:
                        self.imported.append(file)
                        if self.debug:
                            print(f"importing '{file}'")
                        try:
                            f = open(file, "r")
                            c = f.read()
                            f.close()
                            if self.debug:
                                print(f"inspecting actions from {file}")
                            self.inspect_actions(c)
                            self.inspect_import(c)
                        except:
                            error(f"Could not import '{file}'", index, index2)


    def inspect_actions(self, code):
        self.split_code_ = code.splitlines()

        for i in self.split_code_:
            self.split_code.append(i.split(" "))

        # string preprocessor
        store = []
        string_start = -1111
        index3 = -1111
        for index, line in enumerate(self.split_code):
            line_ = []
            in_string = False
            for index2, word in enumerate(line):
                if len(word) > 0:
                    if word[0] == '"' and word[-1] != '"':
                        in_string = True
                        string_start = index2
                        string = ""
                        for index3, word3 in enumerate(line[index2:]):
                            if string == "":
                                # do not add space if first part
                                string = string + word3
                            else:
                                string = string + " " + word3
                            if word3[-1] == '"':
                                break
                        line_.append(string)

                if string_start + index3 - 2 > index2 and in_string:
                    in_string = False
                else:
                    if not in_string:
                        line_.append(word)

            store.append(line_)

        self.split_code = store




        for index, line in enumerate(self.split_code):
            for index2, word in enumerate(line):
                if word == "@action":
                    try:
                        action_name = line[index2+1]
                        self.actions[action_name] = [index, None, None]
                    except:
                        error(f"action identification error", index, 0)


    def runaction(self, action):
        self.caller_action = self.current_action
        self.current_action = action
        if self.inspect_action(action) != 0:
            print("error in runaction action inspector")
            return 1
        self.runcode(self.actions[action][2], self.actions[action][0], action)

    def action(self, action, args):
        # attribute getter
        for enum, w in enumerate(args):
            try:
                self.stack[f"arg[{enum}]"] = self.stack[w]
            except:
                self.stack[f"arg[{enum}]"] = w
        self.runaction(action)

    def runcode(self, code, line_index, action=None):

        in_if_clause = False
        index_end_if_clause = 10000000
        in_while = False
        index_end_while_clause = 10000000
        in_py = False
        index_end_py_clause = 10000000

        for index, line in enumerate(code):
            self.cursor_line = index + line_index + 1
            if action != "every_action":
                pass
                #self.runaction("every_action")
            for index2, word in enumerate(line):
                self.cursor_word = index2

                if not in_if_clause and not in_py and not in_while:
                    # variable declaration
                    if word == "=":
                        try:
                            if line[index2 + 2] not in ["+", "-", "/", "*"]:
                                # variable declaration
                                if line[index2 + 1] in self.actions:
                                    # attribute getter
                                    for enum, w in enumerate(line[index2 + 2:]):
                                        try:
                                            self.stack[f"arg[{enum}]"] = self.stack[w]
                                        except:
                                            self.stack[f"arg[{enum}]"] = self.check_attribute(w)

                                    self.runaction(line[index2 + 1])
                                    #print("r2", line[index2 + 1])
                                    self.stack[line[index2 - 1]] = self.stack[f"return"]
                                else:
                                    self.stack[line[index2 - 1]] = self.check_attribute(line[index2 + 1])
                            else:
                                try:
                                    # variable declaration with calc
                                    self.stack[line[index2 - 1]] = make_math(line[index2 + 2], self.check_attribute(
                                        line[index2 + 1]), self.check_attribute(line[index2 + 3]))
                                except Exception as e:
                                    error(f"calc can only be done with floats: {e}", self.cursor_line + 1, self.cursor_word)
                        except Exception as e:
                            # variable declaration
                            try:
                                if line[index2 + 1] in self.actions:
                                    # attribute getter
                                    for enum, w in enumerate(line[index2 + 2:]):
                                        try:
                                            self.stack[f"arg[{enum}]"] = self.stack[w]
                                        except:
                                            self.stack[f"arg[{enum}]"] = self.check_attribute(w)
                                    self.runaction(line[index2 + 1])
                                    self.stack[line[index2 - 1]] = self.stack[f"return"]
                                else:
                                    self.stack[line[index2 - 1]] = self.check_attribute(line[index2 + 1])
                            except Exception as e:
                                error(f"cant create variable: {e}", self.cursor_line, self.cursor_word)

                    elif word == "py":
                        stack = self.stack
                        actions = self.actions
                        in_py = True


                        # find if end
                        py_code = []
                        indent = 1
                        for amount, line_ in enumerate(code[index + 1:]):
                            if "{" in line_:
                                indent += 1
                            if "}" in line_:
                                indent -= 1
                            if indent == 0:
                                break
                            py_code.append(line_)
                        index_end_py_clause = amount + index + 1
                        c = ""
                        try:
                            indent_layer = 4*int(self.check_attribute(line[index2 + 1]))
                            for j in py_code:
                                for i in j[indent_layer:]:
                                    if i == '':
                                        c += " "
                                    else:
                                        c += i
                                    c += " "

                                c += "\n"
                        except Exception as e:
                            error(f"missing int attribute for py block: {e}", self.cursor_line, self.cursor_word)
                        try:
                            exec(c)
                        except Exception as e:
                            error(f"python error: {e}", self.cursor_line, self.cursor_word)

                    elif word == "if":
                        in_if_clause = True

                        var1 = self.check_attribute(line[index2 + 1])
                        var2 = self.check_attribute(line[index2 + 3])

                        # find if end
                        if_code = []
                        indent = 1
                        for amount, line_ in enumerate(code[index + 1:]):
                            if "}" in line_:
                                indent -= 1
                            if indent == 0:
                                break
                            if "{" in line_:
                                indent += 1
                            if indent == 0:
                                break
                            if_code.append(line_)
                        #print("if",if_code)
                        index_end_if_clause = amount + index + 1

                        if "else" in code[index_end_if_clause]:  # else keyword line
                            else_code = []
                            indent = 1
                            for amount, line_ in enumerate(code[index_end_if_clause + 1:]):
                                if "{" and "}" in line_:
                                    break
                                if "{" in line_:
                                    indent += 1
                                elif "}" in line_:
                                    indent -= 1
                                if indent == 0:
                                    break
                                else_code.append(line_)
                            index_end_if_clause = amount + index_end_if_clause + 1
                            #print("else", else_code)

                        else:
                            else_code = [[""]]

                        if check_operator(line[index2 + 2], var1, var2):
                            self.runcode(if_code, index + line_index + 1)
                        else:

                                #print("else cond")
                                #print(index_end_if_clause)
                                #print(else_code)
                            self.runcode(else_code, index_end_if_clause + line_index + 1)

                    elif word == "while":
                        in_while = True

                        var1 = self.check_attribute(line[index2 + 1])
                        var2 = self.check_attribute(line[index2 + 3])

                        # find if end
                        while_code = []
                        indent = 1
                        for amount, line_ in enumerate(code[index + 1:]):
                            if "{" in line_:
                                indent += 1
                            if "}" in line_:
                                indent -= 1
                            if indent == 0:
                                break
                            while_code.append(line_)
                        index_end_while_clause = amount + index + 1

                        while check_operator(line[index2 + 2], var1, var2):
                            var1 = self.check_attribute(line[index2 + 1])
                            var2 = self.check_attribute(line[index2 + 3])
                            self.runcode(while_code, index)


                    elif word == "windisplay":
                        import tkinter as tk
                        self.var = line[index2 + 2][1:]
                        def upd_label():
                            self.label.config(text=self.stack[self.var])
                            self.win.after(1, upd_label)
                        self.win = tk.Tk()
                        self.win.title(line[index2 + 1])
                        try:
                            self.label = tk.Label(self.win, text=self.stack[self.var], justify=tk.LEFT)
                            self.label.pack()
                            upd_label()
                        except:
                            error(f"variable '{self.var}' not defined", self.cursor_line, self.cursor_word)



                    # function run
                    elif word in self.actions and line[index2 - 1] != "=":
                        # attribute getter
                        for enum, w in enumerate(line[index2 + 1:]):
                            try:
                                self.stack[f"arg[{enum}]"] = self.stack[w]
                            except:
                                self.stack[f"arg[{enum}]"] = self.check_attribute(w)
                        self.runaction(word)
                else:
                    # in if clause or py
                    if index > index_end_if_clause:
                        in_if_clause = False
                    if index > index_end_while_clause:
                        in_while = False
                    if index > index_end_py_clause:
                        in_py = False

    def inspect_action(self, action):
        try:
            action_start_index = self.actions[action][0]
        except:
            error(f"action '{action}' not found", 0, 0)
            return 1
        action_end_index = 0
        self.inspected_actions.append(action)

        # find action end
        indent = 0
        for amount, line in enumerate(self.split_code[action_start_index:]):
            if "{" in line:
                indent += 1
            if "}" in line:
                indent -= 1
            if indent == 0:
                action_end_index = action_start_index + amount
                break
        action_code = self.split_code[action_start_index + 1:action_end_index]
        if debug:
            print(f"\naction '{action}' inspection:")
            print(f"start: {action_start_index}")
            print(f"end: {action_end_index}")
            print(f"code: {action_code}")
        self.actions[action][1] = action_end_index
        self.actions[action][2] = action_code
        return 0

    def check_attribute(self, attribute):
        if attribute[0] == "*":
            return attribute
        if attribute[0] == '"' and attribute[-1] == '"':
            # is string

            attribute = attribute[1:-1]
            return attribute
        else:
            try:
                attribute = float(attribute)
                # is int
                return attribute
            except:
                pass
            try:
                attr = self.stack[attribute]
                try:
                    if attr[0] == '"' and attr[-1] == '"':
                        # is string
                        attr = attr[1:-1]
                        return attr
                except:
                    pass
                try:
                    attr = float(attr)
                    # is int
                    return attr
                except:
                    pass
                return attr
            except Exception as e:
                error(f"variable '{attribute}' not defined : check_attribute:{e}", self.cursor_line, self.cursor_word)



