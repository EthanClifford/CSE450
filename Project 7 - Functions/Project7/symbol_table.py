class RedeclarationError(Exception): pass


class UndeclaredError(Exception): pass


class ScopeError(Exception): pass


class SymbolTable:
    def __init__(self):
        self.scope_declared_variables = [{}]
        self.scope_var_loc = [{}]
        self.s_count = 0
        self.loop_out_tag = []
        self.function_table = [{}]
        self.func_mem = []
        self.in_func_call = False
        self.in_found = False

    def __repr__(self):
        return str(self.scope_declared_variables[-1])

    def declare_variable(self, name, declaration_type,storage_type):
        if name in self.scope_declared_variables[-1]:
            raise RedeclarationError(f'{name} has already been declared!')
        if storage_type == "ARRAY":
            loc = self.get_new_location('a')
        else:
            loc = self.get_new_location('s')
        self.scope_declared_variables[-1][name] = declaration_type
        self.scope_var_loc[-1][name] = loc

    def declare_function(self,name,return_type,args_type):
        if len(self.scope_declared_variables) > 1:
            raise ScopeError
        self.function_table[len(self.function_table)-2][name] = [return_type,args_type]

    def function_type(self,name):
        return self.function_table[len(self.function_table)-2][name][0]

    def function_name(self):
        name = ""
        for i in self.function_table[len(self.function_table)-2].keys():
            name = i
        return name

    def function_args_type(self,name):
        return self.function_table[len(self.function_table) - 2][name][1]

    def add_func_mem(self,var):
        infunc = False
        for i in self.function_table:
            if i:
                infunc = True
        if infunc:
            self.func_mem += var
            i = 0
            while i < len(self.func_mem):
                j = i+1
                while j < len(self.func_mem):
                    if self.func_mem[i] == self.func_mem[j]:
                        del self.func_mem[j]
                    j += 1
                i += 1

    def get_func_mem(self):
        return self.func_mem

    def in_func(self):
        infunc = False
        for i in self.function_table:
            if i:
                infunc = True
        return infunc

    def use_variable(self, name):
        i = len(self.scope_declared_variables) - 1
        while i >= 0:
            if name in self.scope_declared_variables[i]:
                break
            i -= 1
        if i == len(self.scope_declared_variables):
            raise UndeclaredError(f'{name} has not been declared!')
        if self.scope_var_loc[i][name][0] == 'a':
            return [self.scope_declared_variables[i][name],'ARRAY']
        return [self.scope_declared_variables[i][name]]

    def update_variable(self, name):
        i = len(self.scope_declared_variables) - 1
        while i >= 0:
            if name in self.scope_declared_variables[i]:
                break
            i -= 1
        if i == len(self.scope_declared_variables):
            raise UndeclaredError(f'{name} has not been declared!')

    def get_new_location(self, type_):
        self.s_count += 1
        return f"{type_}{self.s_count}"

    def get_loc(self, name):
        i = len(self.scope_var_loc)-1
        while i >= 0:
            if name in self.scope_var_loc[i]:
                break
            i -= 1
        if i < 0:
            raise UndeclaredError(f'{name} has not been declared!')
        return self.scope_var_loc[i][name]

    def add_exit_tag(self,tag):
        self.loop_out_tag.append(tag)

    def get_exit_tag(self):
        return self.loop_out_tag[-1]

    def end_loop(self):
        self.loop_out_tag.pop(-1)

    def incr_func_scope(self):
        self.scope_declared_variables.append({})
        self.scope_var_loc.append({})
        self.function_table.append({})

    def incr_scope(self):
        self.scope_declared_variables.append({})
        self.scope_var_loc.append({})

    def decr_scope(self):
        if len(self.scope_declared_variables) == 1:
            return
        self.scope_declared_variables.pop(-1)
        self.scope_var_loc.pop(-1)

    def decr_func_scope(self):
        if len(self.scope_declared_variables) == 1:
            return
        self.scope_declared_variables.pop(-1)
        self.scope_var_loc.pop(-1)
        self.function_table.pop(-1)
        self.func_mem = []
