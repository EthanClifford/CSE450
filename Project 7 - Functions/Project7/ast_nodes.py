class TypeException(Exception): pass


class NumbrLiteral:
    """
    An expression that represents a Numbr (like 5).
    The string of the value is stored as its only child.
    """
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumbrLiteral({self.value})"

    def get_val(self,symbol_table):
        return self.value

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        output_var = symbol_table.get_new_location('s')
        result = f"VAL_COPY {self.value} {output_var}"
        compiled_output.append(result)
        return output_var

class TroofLiteral:
    def __init__(self, value):
        if value == "WIN":
            value = 1
        else:
            value = 0
        self.value = value

    def __repr__(self):
        return f"TroofLiteral({self.value})"

    def get_type(self,symbol_table):
        return ["TROOF"]

    def get_val(self,symbol_table):
        return self.value

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        output_var = symbol_table.get_new_location('s')
        result = f"VAL_COPY {self.value} {output_var}"
        compiled_output.append(result)
        return output_var


class LettrLiteral:
    """
    An expression that represents a Numbr (like 5).
    The string of the value is stored as its only child.
    """
    def __init__(self, value):
        temp = value
        if len(temp) > 1:
            if value[1] == ':':
                value = '\'\\'
                if temp[2] == ')':
                    value += 'n'
                    value += '\''
                elif temp[2] == '>':
                    value += 't'
                    value += '\''
                elif temp[2] == "'":
                    value += '\''
                    value += '\''
                elif temp[2] == ':':
                    value = '\':\''
        self.value = value

    def __repr__(self):
        return f"LETTR({self.value})"

    def get_val(self,symbol_table):
        return self.value

    def get_type(self,symbol_table):
        return ["LETTR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        output_var = symbol_table.get_new_location('s')
        result = f"VAL_COPY {self.value} {output_var}"
        compiled_output.append(result)
        return output_var


class YarnLiteral:
    def __init__(self, value, length=0):
        self.length = length
        i = 0
        temp = ""
        slash = False
        while i < len(value):
            if value[i] == ':' and not slash:
                slash = True
            elif slash:
                if value[i] == ')':
                    temp += '\\n'
                if value[i] == '>':
                    temp += '\\t'
                if value[i] == ':':
                    temp += ':'
                if value[i] == '"':
                    temp += '"'
                slash = False
            elif value[i] == "'":
                temp += '\\' + '\''
            else:
                temp += value[i]
            i += 1
        self.value = temp

    def __repr__(self):
        return f"YARN({self.value})"

    def get_val(self,symbol_table):
        return self.value

    def get_type(self,symbol_table):
        return ["YARN"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        i = 1
        string = []
        temp = ""
        while i < len(self.value)-1:
            if self.value[i] == "\\":
                temp += "\'"+self.value[i]
            elif temp:
                temp += self.value[i]+"\'"
                string.append(temp)
                temp = ""
            else:
                string.append("'"+self.value[i]+"'")
            i += 1
        arrnode = ArrayNode(string,len(string),"YARN")
        arr = arrnode.compile(compiled_output,symbol_table)
        return arr

class StatementsNode:
    def __init__(self, children):
        self.children = children

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.isfunc_call_node:
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        #print(self.children)
        for child in self.children:
            child.compile(compiled_output, symbol_table)


class ArrayNode:
    def __init__(self, values, len, type):
        self.values = values
        self.length = len
        self.type = type

    def get_type(self,symbol_table):
        return ["ARRAY"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self,compiled_output,symbol_table):
        length = len(self.values)
        i = 0
        arr = symbol_table.get_new_location("a")
        compiled_output.append(f"AR_SET_SIZE {arr} {length}")
        while i < length:
            compiled_output.append(f"AR_SET_IDX {arr} {i} {self.values[i]}")
            i += 1
        return arr

class GimmehNode:
    def __init__(self):
        self.value = 0

    def get_type(self,symbol_table):
        return ["LETTR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self,compiled_output, symbol_table):
        val_in_var = symbol_table.get_new_location('s')
        compiled_output.append(f"IN_CHAR {val_in_var}")
        return val_in_var


class ArDeclNode:
    def __init__(self, name, len, type):
        self.name = name
        self.len = len
        self.type = type

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        if type(self.len) is str:
            symbol_table.declare_variable(self.name, self.type, "ARRAY")
        else:
            len_var = self.len.compile(compiled_output,symbol_table)
            symbol_table.declare_variable(self.name, self.type, "ARRAY")
            outlen = symbol_table.get_new_location('s')
            output_var = symbol_table.get_loc(self.name)
            result = f"VAL_COPY {len_var} {outlen} \n"
            result += f"AR_SET_SIZE {output_var} {outlen}"
            compiled_output.append(result)
            return output_var


class DeclNode:
    def __init__(self, name, val, type):
        self.name = name
        self.value = val
        self.type = type

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):

        if type(self.value) is str:
            symbol_table.declare_variable(self.name, self.type, self.type)
        else:
            val_type = self.value.get_type(symbol_table)[0]
            if val_type != self.type:
                if val_type != "LETTR" or self.type != "YARN":
                    if val_type != "YARN" or self.type != "LETTR":
                        raise TypeException
            val_out_var = self.value.compile(compiled_output, symbol_table)
            symbol_table.declare_variable(self.name, self.type, self.type)
            output_var = symbol_table.get_loc(self.name)
            result = f"VAL_COPY {val_out_var} {output_var}"
            compiled_output.append(result)
            symbol_table.add_func_mem([val_out_var,output_var])
            return output_var


class Var_useNode:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_type(self, symbol_table):
        return symbol_table.use_variable(self.name)

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        out_var = symbol_table.get_loc(self.name)
        return out_var


class Ar_useNode:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def get_type(self, symbol_table):
        return symbol_table.use_variable(self.name)

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        return symbol_table.get_loc(self.name)


class Ar_indxNode:
    def __init__(self, name,indx,val,setting):
        self.name = name
        self.indx = indx
        self.value = val
        self.mode = setting

    def get_name(self):
        return self.name

    def get_type(self, symbol_table):
        if symbol_table.use_variable(self.name)[0] == "YARN":
            return ["LETTR"]
        return symbol_table.use_variable(self.name)

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        arr = symbol_table.get_loc(self.name)
        if arr[0] != 'a':
            raise TypeException
        indx_type = self.indx.get_type(symbol_table)[0]
        if indx_type != "NUMBR":
            raise TypeException
        if self.mode == 'r':
            arr = symbol_table.get_loc(self.name)
            indx_loc = symbol_table.get_new_location('s')
            out_loc = symbol_table.get_new_location("s")
            compiled_output.append(f"VAL_COPY {self.indx.compile(compiled_output,symbol_table)} {indx_loc}")
            compiled_output.append(f"AR_GET_IDX {arr} {indx_loc} {out_loc}")
            return out_loc
        if self.mode == 'w':
            val_type = self.value.get_type(symbol_table)[0]
            if val_type != symbol_table.use_variable(self.name)[0]:
                if val_type != "LETTR" or symbol_table.use_variable(self.name)[0] != "YARN":
                    raise TypeException
            arr = symbol_table.get_loc(self.name)
            val_loc = symbol_table.get_new_location('s')
            indx_loc = symbol_table.get_new_location('s')
            out_loc = symbol_table.get_new_location("s")
            compiled_output.append(f"VAL_COPY {self.value.compile(compiled_output, symbol_table)} {val_loc}")
            compiled_output.append(f"VAL_COPY {self.indx.compile(compiled_output,symbol_table)} {indx_loc}")
            compiled_output.append(f"AR_GET_IDX {arr} {indx_loc} {out_loc}")
            compiled_output.append(f"AR_SET_IDX {arr} {indx_loc} {val_loc}")
            compiled_output.append(f"VAL_COPY {val_loc} {out_loc}")
            return out_loc

class Var_assignNode:
    def __init__(self, name, val):
        self.name = name
        self.value = val

    def get_val(self, symbol_table):
        return symbol_table.use_variable(self.name)[0]

    def get_type(self,symbol_table):
        return self.value.get_type(symbol_table)

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        val_type = self.value.get_type(symbol_table)[0]
        if val_type != symbol_table.use_variable(self.name)[0]:
            if val_type != "YARN" and symbol_table.use_variable(self.name)[0] != "LETTR":
                if val_type != "LETTR" and symbol_table.use_variable(self.name)[0] != "LETTR":
                    raise TypeException
        symbol_table.update_variable(self.name)
        val_out_var = self.value.compile(compiled_output, symbol_table)
        output_var = symbol_table.get_loc(self.name)
        if val_out_var[0] == 'a':
            result = f"AR_COPY {val_out_var} {output_var}"
        else:
            result = f"VAL_COPY {val_out_var} {output_var}"
        compiled_output.append(result)
        symbol_table.add_func_mem([val_out_var,output_var])
        return output_var

class Var_Incr:
    def __init__(self, op, name, val):
        self.op = op
        self.name = name
        self.value = val

    def get_val(self, symbol_table):
        return symbol_table.use_variable(self.name)[0]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        val_type = self.value.get_type(symbol_table)[0]
        if val_type != "NUMBR":
            raise TypeException
        if val_type != symbol_table.use_variable(self.name)[0]:
            raise TypeException
        symbol_table.update_variable(self.name)
        val_out_var = self.value.compile(compiled_output, symbol_table)
        output_var = symbol_table.get_loc(self.name)
        temp = symbol_table.get_new_location('s')
        result = f"VAL_COPY {output_var} {temp}\n"
        if self.op == 'UPPIN':
            result += f"ADD {val_out_var} {temp} {temp}\n"
        if self.op == 'NERFIN':
            result += f"SUB {temp} {val_out_var} {temp}\n"
        result += f"VAL_COPY {temp} {output_var}"
        compiled_output.append(result)
        return output_var

class LengthNode:
    def __init__(self,name):
        self.name = name

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self,compiled_output,symbol_table):
        arr = symbol_table.get_loc(self.name)
        out = symbol_table.get_new_location('s')
        compiled_output.append(f"AR_GET_SIZE {arr} {out}")
        return out

class YarnLenNode:
    def __init__(self,yarn):
        self.yarn = yarn

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self,compiled_output,symbol_table):
        arr = self.yarn.compile(compiled_output,symbol_table)
        out = symbol_table.get_new_location('s')
        compiled_output.append(f"AR_GET_SIZE {arr} {out}")
        return out

class VisibleNode:

    def __init__(self, children, bang):
        self.children = children
        self.bang = bang

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        for child in self.children:
            if child:
                result_loc = child.compile(compiled_output, symbol_table)
                type_child = child.get_type(symbol_table)[0]
                if result_loc[0] == 's':
                    if type_child == "NUMBR" or type_child == "TROOF":
                        compiled_output.append(f"OUT_NUM {result_loc}")
                    elif type_child == "LETTR":
                        compiled_output.append(f"OUT_CHAR {result_loc}")
                elif result_loc[0] == 'a':
                    sz = symbol_table.get_new_location("s")
                    inc = symbol_table.get_new_location("s")
                    test_loc = symbol_table.get_new_location("s")
                    out = symbol_table.get_new_location("s")
                    loop_start = symbol_table.get_new_location("array_loop_start")
                    loop_end = symbol_table.get_new_location("array_loop_end")
                    compiled_output.append(f"AR_GET_SIZE {result_loc} {sz}")
                    compiled_output.append(f"VAL_COPY 0 {inc}")
                    compiled_output.append(f"{loop_start}:")
                    compiled_output.append(f"TEST_GTE {inc} {sz} {test_loc}")
                    compiled_output.append(f"JUMP_IF_N0 {test_loc} {loop_end}")
                    compiled_output.append(f"AR_GET_IDX {result_loc} {inc} {out}")
                    if type_child == "NUMBR" or type_child == "TROOF":
                        compiled_output.append(f"OUT_NUM {out}")
                    elif type_child == "LETTR" or type_child == "YARN":
                        compiled_output.append(f"OUT_CHAR {out}")
                    compiled_output.append(f"ADD 1 {inc} {inc}")
                    compiled_output.append(f"JUMP {loop_start}")
                    compiled_output.append(f"{loop_end}:")
        if not self.bang:
            compiled_output.append("OUT_CHAR '\\n\'")

    def __str__(self):
        return f"PrintNode({self.children})"


class BinaryMathNode:
    def __init__(self, op, lhs, rhs):
        self.children = [op, lhs, rhs]

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        val_type = self.children[1].get_type(symbol_table)[0]
        if val_type != "NUMBR":
            raise TypeException
        if val_type != self.children[2].get_type(symbol_table)[0]:
            raise TypeException
        symbol_to_command = {
            'SUM ': "ADD",
            'DIFF ': "SUB",
            'PRODUKT ': "MULT",
            'QUOSHUNT ': "DIV",
            'BIGGR ': "TEST_GTR",
            'SMALLR ':"TEST_LESS"
        }
        op_command = symbol_to_command[self.children[0]]

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)
        rhs_compiled = self.children[2].compile(compiled_output, symbol_table)

        output_var = symbol_table.get_new_location('s')

        result = f"{op_command} {lhs_compiled} {rhs_compiled} {output_var}"
        compiled_output.append(result)
        if symbol_table.in_func_call:
            symbol_table.add_func_mem([output_var])
        else:
            symbol_table.add_func_mem([lhs_compiled,rhs_compiled,output_var])

        return output_var


class UnaryMathNode:
    def __init__(self, op, lhs):
        self.children = [op, lhs]

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        val_type = self.children[1].get_type(symbol_table)[0]
        if val_type != "NUMBR":
            raise TypeException
        symbol_to_command = {
            'FLIP ': "DIV",
            'SQUAR ': "MULT"
        }
        op_command = symbol_to_command[self.children[0]]

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)

        output_var = symbol_table.get_new_location('s')

        if op_command == "DIV":
            result = f"{op_command} 1 {lhs_compiled} {output_var}"
        elif op_command == "MULT":
            result = f"{op_command} {lhs_compiled} {lhs_compiled} {output_var}"

        compiled_output.append(result)

        return output_var

class BinaryCompNode:
    def __init__(self, op, lhs, rhs):
        self.children = [op, lhs, rhs]

    def get_type(self,symbol_table):
        return ["TROOF"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):

        symbol_to_command = {
            'SAEM ': "TEST_EQU",
            'DIFFRINT ': "TEST_NEQU",
            'FURSTSMALLR ': "TEST_LESS",
            'FURSTBIGGR ': "TEST_GTR"
        }
        op_command = symbol_to_command[self.children[0]]

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)
        rhs_compiled = self.children[2].compile(compiled_output, symbol_table)

        output_var = symbol_table.get_new_location('s')
        if self.children[1].get_type(symbol_table)[0] != self.children[2].get_type(symbol_table)[0]:
            result = f"VAL_COPY 0 {output_var}"
        else:
            result = f"{op_command} {lhs_compiled} {rhs_compiled} {output_var}"
        compiled_output.append(result)
        symbol_table.add_func_mem([lhs_compiled,rhs_compiled,output_var])
        return output_var


class BinaryLogicNode:
    def __init__(self, op, lhs, rhs):
        self.children = [op, lhs, rhs]

    def get_type(self,symbol_table):
        return ["TROOF"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        if self.children[1].get_type(symbol_table)[0] != self.children[2].get_type(symbol_table)[0]:
            raise TypeException
        op_command = self.children[0]

        output_var = symbol_table.get_new_location('s')
        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)
        jump_if = symbol_table.get_new_location("logical_jump")
        jump = symbol_table.get_new_location("logical_end")
        if op_command == 'BOTH ':
            compiled_output.append(f"JUMP_IF_0 {lhs_compiled} {jump_if}")
        elif op_command == 'EITHER ':
            compiled_output.append(f"JUMP_IF_N0 {lhs_compiled} {jump_if}")
        rhs_compiled = self.children[2].compile(compiled_output, symbol_table)
        if op_command == 'BOTH ':
            compiled_output.append(f"JUMP_IF_0 {rhs_compiled} {jump_if}")
            compiled_output.append(f"VAL_COPY {rhs_compiled} {output_var}")
            compiled_output.append(f"JUMP {jump}")
            compiled_output.append(f"{jump_if}:")
            compiled_output.append(f"VAL_COPY 0 {output_var}")
            compiled_output.append(f"{jump}:")
        elif op_command == 'EITHER ':
            compiled_output.append(f"JUMP_IF_N0 {rhs_compiled} {jump_if}")
            compiled_output.append(f"VAL_COPY {rhs_compiled} {output_var}")
            compiled_output.append(f"JUMP {jump}")
            compiled_output.append(f"{jump_if}:")
            compiled_output.append(f"VAL_COPY 1 {output_var}")
            compiled_output.append(f"{jump}:")

        temp_var = symbol_table.get_new_location('s')

        if op_command == 'WON ':
            compiled_output.append(f"ADD {lhs_compiled} {rhs_compiled} {temp_var}")
            compiled_output.append(f"TEST_EQU {temp_var} 1 {output_var}")

        return output_var


class ManyLogicNode:
    def __init__(self, op, operands):
        self.children = [op, operands]

    def get_type(self,symbol_table):
        return ["TROOF"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        op_command = self.children[0]
        operands = self.children[1]
        lhs_compiled = []
        count = 0
        output_var = symbol_table.get_new_location('s')
        jump_if = symbol_table.get_new_location("logical_jump")
        jump = symbol_table.get_new_location("logical_end")
        for i in operands:
            lhs_compiled.append(i.compile(compiled_output,symbol_table))
            if op_command == 'ALL ':
                compiled_output.append(f"JUMP_IF_0 {lhs_compiled[count]} {jump_if}")
            if op_command == 'ANY ':
                compiled_output.append(f"JUMP_IF_N0 {lhs_compiled[count]} {jump_if}")
            count += 1
        if op_command == 'ALL ':
            compiled_output.append(f"VAL_COPY {lhs_compiled[-1]} {output_var}")
            compiled_output.append(f"JUMP {jump}")
            compiled_output.append(f"{jump_if}:")
            compiled_output.append(f"VAL_COPY 0 {output_var}")
            compiled_output.append(f"{jump}:")
        if op_command == 'ANY ':
            compiled_output.append(f"VAL_COPY {lhs_compiled[-1]} {output_var}")
            compiled_output.append(f"JUMP {jump}")
            compiled_output.append(f"{jump_if}:")
            compiled_output.append(f"VAL_COPY 1 {output_var}")
            compiled_output.append(f"{jump}:")

        return output_var


class UnaryLogicNode:
    def __init__(self, op, lhs):
        self.children = [op, lhs]

    def get_type(self,symbol_table):
        return ["TROOF"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        op_command = self.children[0]

        lhs_compiled = self.children[1].compile(compiled_output, symbol_table)

        output_var = symbol_table.get_new_location('s')

        if op_command == 'NOT ':
            result = f"TEST_EQU {lhs_compiled} 0 {output_var}"
        compiled_output.append(result)

        return output_var


class RandomNode:
    def __init__(self):
        self.val = 0

    def get_type(self,symbol_table):
        return ["NUMBR"]

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        output_var = symbol_table.get_new_location('s')
        result = f"RANDOM {output_var}"
        compiled_output.append(result)
        return output_var

class OrlyNode:
    def __init__(self, expr, children):
        self.expr = expr
        self.children = children

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self,compiled_output,symbol_table):
        s = []
        if self.expr.get_type(symbol_table)[0] != "TROOF":
            raise TypeException

        test_var = self.expr.compile(compiled_output,symbol_table)
        s.append(test_var)
        jump_if = symbol_table.get_new_location("jump_after_true")
        true_jump = symbol_table.get_new_location("oic_jump")
        compiled_output.append(f"JUMP_IF_0 {test_var} {jump_if}")
        yesnode = self.children[0].compile(compiled_output,symbol_table)
        s += yesnode
        compiled_output.append(f"JUMP {true_jump}")
        compiled_output.append(f"{jump_if}:")
        if len(self.children) == 2:
            nowainode = self.children[1].compile(compiled_output,symbol_table)
            s += nowainode
        compiled_output.append(f"{true_jump}:")
        return s

class ifNode:
    def __init__(self,children):
        self.children = children

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        s = []
        symbol_table.incr_scope()
        for i in self.children:
            if type(i) is not str:
                temp = i.compile(compiled_output,symbol_table)
                s.append(temp)
        symbol_table.decr_scope()
        return s


class LoopNode:
    def __init__(self, children, condition, last=None):
        self.children = children
        self.condition = condition
        self.last = last

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        for i in self.children:
            if i.is_func_call_node():
                return True
            elif i.check_func_call():
                return True
        return False

    def compile(self, compiled_output, symbol_table):
        symbol_table.incr_scope()
        loop_start = symbol_table.get_new_location("loop_start_")
        loop_end = symbol_table.get_new_location("loop_end_")
        symbol_table.add_exit_tag(loop_end)
        compiled_output.append(f"{loop_start}:")
        if self.condition:
            if self.condition.get_type(symbol_table)[0] != "TROOF":
                raise TypeException
            test = self.condition.compile(compiled_output, symbol_table)
            compiled_output.append(f"JUMP_IF_N0 {test} {loop_end}")
        for i in self.children:
            i.compile(compiled_output, symbol_table)
        if self.last:
            self.last.compile(compiled_output, symbol_table)
        compiled_output.append(f"JUMP {loop_start}")
        compiled_output.append(f"{loop_end}:")
        symbol_table.end_loop()
        symbol_table.decr_scope()


class BreakNode:
    def __init__(self):
        self.exit = ""

    def is_func_call_node(self):
        return False

    def check_func_call(self):
        return False

    def compile(self, compiled_output, symbol_table):
        self.exit = symbol_table.get_exit_tag()
        compiled_output.append(f"JUMP {self.exit}")

class SwitchNode:
    def __init__(self,expr,lit=None,children=None,default=None):
        self.expr = expr
        self.lit = lit
        self.children = children
        self.default = default

    def is_func_call_node(self):
        return False

    def compile(self, compiled_output, symbol_table):
        counter = symbol_table.get_new_location("s")
        gtfo = symbol_table.get_new_location("s")
        run = symbol_table.get_new_location("s")
        end_case = symbol_table.get_new_location("end_switch_")
        compiled_output.append(f"VAL_COPY 0 {counter}")
        compiled_output.append(f"VAL_COPY 0 {gtfo}")
        compiled_output.append(f"VAL_COPY 0 {run}")
        if self.lit is not None and self.children is not None:
            i = 0
            while i < len(self.lit):
                expr_type = self.expr.get_type(symbol_table)[0]
                lit_type = self.lit[i].get_type(symbol_table)[0]
                if expr_type != lit_type:
                    if expr_type != "LETTR" or expr_type != "YARN":
                        if lit_type != "LETTR" or lit_type != "YARN":
                            raise TypeException

                exprloc = self.expr.compile(compiled_output,symbol_table)
                litloc = self.lit[i].compile(compiled_output,symbol_table)
                testloc = symbol_table.get_new_location("s")
                temp2 = symbol_table.get_new_location("s")
                gtfotemp = symbol_table.get_new_location("s")
                runtemp = symbol_table.get_new_location("s")
                casejump = symbol_table.get_new_location("case_jump_")
                fall_through = symbol_table.get_new_location("fall_through_jump")
                if exprloc[0] == "a":
                    switch_ar_loop = symbol_table.get_new_location("switch_array_loop_start_")
                    switch_ar_loop_end = symbol_table.get_new_location("switch_array_loop_end_")
                    equcount = symbol_table.get_new_location("s")
                    index = symbol_table.get_new_location("s")
                    ar1idx = symbol_table.get_new_location("s")
                    ar2idx = symbol_table.get_new_location("s")
                    temp = symbol_table.get_new_location("s")
                    loop_test = symbol_table.get_new_location("s")
                    ar1len = symbol_table.get_new_location("s")
                    ar2len = symbol_table.get_new_location("s")
                    temp1 = symbol_table.get_new_location("s")
                    compiled_output.append(f"VAL_COPY 0 {index}")
                    compiled_output.append(f"VAL_COPY 0 {equcount}")
                    compiled_output.append(f"AR_GET_SIZE {exprloc} {ar1len}")
                    compiled_output.append(f"AR_GET_SIZE {litloc} {ar2len}")
                    compiled_output.append(f"TEST_EQU {ar1len} {ar2len} {loop_test}")
                    compiled_output.append(f"{switch_ar_loop}:")
                    compiled_output.append(f"TEST_LESS {index} {ar1len} {temp1}")
                    compiled_output.append(f"ADD {temp1} {loop_test} {loop_test}")
                    compiled_output.append(f"TEST_EQU {loop_test} 2 {loop_test}")
                    compiled_output.append(f"JUMP_IF_0 {loop_test} {switch_ar_loop_end}")
                    compiled_output.append(f"AR_GET_IDX {exprloc} {index} {ar1idx}")
                    compiled_output.append(f"AR_GET_IDX {litloc} {index} {ar2idx}")
                    compiled_output.append(f"TEST_EQU {ar1idx} {ar2idx} {temp}")
                    compiled_output.append(f"ADD {equcount} {temp} {equcount}")
                    compiled_output.append(f"ADD {index} 1 {index}")
                    compiled_output.append(f"JUMP {switch_ar_loop}")
                    compiled_output.append(f"{switch_ar_loop_end}:")
                    compiled_output.append(f"TEST_EQU {ar1len} {equcount} {equcount}")
                    compiled_output.append(f"JUMP_IF_0 {equcount} {casejump}")
                else:
                    compiled_output.append(f"TEST_EQU {exprloc} {litloc} {testloc}")
                    compiled_output.append(f"TEST_EQU 1 {gtfo} {gtfotemp}")
                    compiled_output.append(f"TEST_EQU 1 {run} {runtemp}")
                    compiled_output.append(f"ADD {runtemp} {gtfotemp} {temp2}")
                    compiled_output.append(f"ADD {testloc} {temp2} {testloc}")
                    compiled_output.append(f"JUMP_IF_0 {testloc} {casejump}")

                compiled_output.append(f"ADD 1 {counter} {counter}")
                compiled_output.append(f"VAL_COPY 1 {run}")
                compiled_output.append(f"VAL_COPY 1 {gtfo}")
                symbol_table.incr_scope()
                symbol_table.add_exit_tag(end_case)
                for j in self.children[i]:
                    j.compile(compiled_output, symbol_table)
                compiled_output.append(f"VAL_COPY 1 {gtfo}")
                compiled_output.append(f"VAL_COPY 0 {counter}")
                compiled_output.append(f"{casejump}:")
                i += 1
                symbol_table.end_loop()
                symbol_table.decr_scope()
        if self.default is not None:
            compiled_output.append(f"JUMP_IF_N0 {counter} {end_case}")
            for i in self.default:
                i.compile(compiled_output,symbol_table)
        compiled_output.append(f"{end_case}:")

class FuncNode:
    def __init__(self,name,params, params_type,body,return_type):
        self.name = name
        self.children = body
        self.return_type = return_type
        self.params = params
        self.params_type = params_type
        self.Func_call = False

    def get_type(self,symbol_table):
        return self.return_type.get_type(symbol_table)

    def is_func_call_node(self):
        return False

    def compile(self,compiled_output,symbol_table):
        symbol_table.declare_function(self.name,self.return_type,self.params_type)
        symbol_table.incr_func_scope()
        end_label = symbol_table.get_new_location(f"end_of_{self.name}_")
        compiled_output.append(f"JUMP {end_label}")
        compiled_output.append(f"func_{self.name}:")
        param_loc = []
        count = 0
        if self.params:
            for i in self.params:
                if self.params_type[count][0] == "ARRAY":
                    symbol_table.declare_variable(i,self.params_type[count][1],"ARRAY")
                elif self.params_type[count] == "YARN":
                    symbol_table.declare_variable(i,self.params_type[count],"ARRAY")
                else:
                    symbol_table.declare_variable(i,self.params_type[count],self.params_type[count])
                param_loc.append(symbol_table.get_loc(i))
                compiled_output.append(f"POP {param_loc[-1]}")
                count += 1
                symbol_table.add_func_mem(param_loc)
        if self.children:
            for i in self.children:
                temp = i.compile(compiled_output,symbol_table)
                if temp:
                    symbol_table.add_func_mem(temp)
        compiled_output.append(f"{end_label}:")
        symbol_table.decr_func_scope()

class FuncCallNode:
    def __init__(self,func_name,args=None):
        self.func_name = func_name
        self.args = args

    def is_func_call_node(self):
        return True

    def check_func_call(self):
        return True

    def get_type(self,symbol_table):
        return [symbol_table.function_type(self.func_name)[0]]

    def compile(self,compiled_output,symbol_table):
        symbol_table.in_func_call = True
        params = symbol_table.function_args_type(self.func_name)
        #print(params)
        if self.args and params:
            count = 0
            if symbol_table.function_args_type(self.func_name):
                if len(params) == len(self.args):
                    for i in self.args:
                        itype = i.get_type(symbol_table)[0]
                        param_type = params[count]
                        #print(i)
                        #print("i get type: ",i.get_type(symbol_table))
                        #print("param_type: ",param_type)

                        if len(i.get_type(symbol_table))>1:
                            #print("run")
                            temp = i.get_type(symbol_table)[0]
                            itype = [i.get_type(symbol_table)[1],temp]
                            if type(param_type) is list:
                                param_type = params[count]
                        elif type(param_type) is list:
                            #print("run")
                            raise TypeException
                        #print("i: ",itype)
                        #print("param_type: ",param_type)
                        if itype != param_type:
                            raise TypeException
                        count += 1
                else:
                    raise TypeException
            else:
                raise TypeException
        elif not self.args and params:
            raise TypeException
        elif self.args and not params:
            raise TypeException
        func_call_start = symbol_table.get_new_location(f"func_call_{self.func_name}_")
        func_return_type = symbol_table.function_type(self.func_name)
        if len(func_return_type) > 1:
            pop_loc = symbol_table.get_new_location('a')
        else:
            pop_loc = symbol_table.get_new_location('s')
        if self.args:
            self.args.append(func_call_start)
        else:
            self.args = [func_call_start]
        func_mem = symbol_table.get_func_mem()
        if func_mem:
            for i in func_mem:
                compiled_output.append(f"PUSH {i}")
        if self.args:
            i = len(self.args)-1
            while i >= 0:
                if type(self.args[i]) != str:
                    arg_loc = self.args[i].compile(compiled_output,symbol_table)
                    compiled_output.append(f"PUSH {arg_loc}")
                else:
                    compiled_output.append(f"PUSH {self.args[i]}")
                i -= 1
        compiled_output.append(f"JUMP func_{self.func_name}")
        compiled_output.append(f"{func_call_start}:")
        compiled_output.append(f"POP {pop_loc}")
        num_args = len(self.args)-1
        #print(num_args)
        if func_mem:
            if symbol_table.in_found or num_args == 0:
                i = len(func_mem)-num_args-1
            else:
                i = len(func_mem)-num_args
            while i >= 0:
                compiled_output.append(f"POP {func_mem[i]}")
                i -= 1
        symbol_table.in_func_call = False
        if func_mem:
            func_mem[-1] = pop_loc
        return pop_loc

class FoundNode:
    def __init__(self, return_expr):
        self.return_expr = return_expr

    def is_func_call_node(self):
        return False

    def compile(self,compiled_output,symbol_table):
        symbol_table.in_found = True
        func_name = symbol_table.function_name()
        func_type = symbol_table.function_type(func_name)
        if len(func_type) == 1:
            func_type = func_type[0]
        elif len(func_type) > 1:
            if func_type[0] == 'LETTR' and func_type[1] == 'ARRAY':
                func_type = 'YARN'
            else:
                func_type = func_type[0]
        if func_type != self.return_expr.get_type(symbol_table)[0]:
            raise TypeException
        pop_loc = symbol_table.get_new_location('s')
        return_loc = self.return_expr.compile(compiled_output, symbol_table)
        compiled_output.append(f"POP {pop_loc}")
        compiled_output.append(f"PUSH {return_loc}")
        compiled_output.append(f"JUMP {pop_loc}")
        symbol_table.in_found = False
        return return_loc
