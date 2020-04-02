from . lolcode_parser import build_parser, parse_LOLcode
from . symbol_table import SymbolTable


def generate_LMAOcode_from_LOLcode(lolcode_str):
    ast = parse_LOLcode(lolcode_str)

    compiled_output = []
    symbol_table = SymbolTable()
    print(f"AST = {ast}")
    ast.compile(compiled_output, symbol_table)

    # print(compiled_output)
    lmao_code = "\n".join(compiled_output) + "\n"
    # output = interpreter.interpret(lmao_code, language="LMAOcode")
    # print(f"Output = {output}")
    return lmao_code


def generate_ROFLcode_from_LOLcode(lolcode_str):
    lmaocode_str = generate_LMAOcode_from_LOLcode(lolcode_str)
    rofl = []
    rofl.append(f"STORE 10000 0")
    rofl.append(f"VAL_COPY 20000 regH")
    split_lmao = lmaocode_str.split('\n')
    count = 0
    for i in split_lmao:
        i_str = i.split(" ")
        if len(i_str) > 3:
            if "'" == i_str[3]:
                i_str[3] = "' '"


        if len(i_str) > 2:
            if i_str[1] == "'" and i_str[2] == "'":
                i_str[1] = "' '"
                i_str[2] = i_str[3]
                i_str.pop(-1)

        count = 1
        #if i_str[0]:
        #    if i_str[1][0] == "'" and '\\' not in i_str[1]:
        #        i_str[1] = i_str[1][1:-1]
        if "VAL_COPY" in i:
            if i_str[1][0] == 's':
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            rofl.append(f"VAL_COPY regA regB")
            rofl.append(f"STORE regB {i_str[2][1:]}")
        elif "OUT_NUM" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
                rofl.append(f"OUT_NUM regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
                rofl.append(f"OUT_NUM regA")
        elif "OUT_CHAR" in i:
            if len(i_str[1]) > 1:
                if i_str[1][0] == "s":
                    rofl.append(f"LOAD {i_str[1][1:]} regA")
                    rofl.append(f"OUT_CHAR regA")
                else:
                    rofl.append(f"VAL_COPY {i_str[1]} regA")
                    rofl.append(f"OUT_CHAR regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
                rofl.append(f"OUT_CHAR regA")
        elif "RANDOM" in i:
            rofl.append(f"RANDOM regA")
            rofl.append(f"STORE regA {i_str[1][1:]}")
        elif "IN_CHAR" in i:
            rofl.append(f"IN_CHAR regA")
            rofl.append(f"STORE regA {i_str[1][1:]}")
        elif "ADD" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"ADD regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "SUB" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"SUB regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "MULT" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"MULT regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "DIV" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"DIV regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_NEQU" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_NEQU regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_EQU" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_EQU regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_LESS" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_LESS regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_GTR" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_GTR regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_GTE" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_GTE regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "TEST_LTE" in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            if i_str[2][0] == "s":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"TEST_LTE regA regB regC")
            rofl.append(f"STORE regC {i_str[3][1:]}")
        elif "JUMP_IF_0" in i:
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"JUMP_IF_0 regA regB")
        elif "JUMP_IF_N0" in i:
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"JUMP_IF_N0 regA regB")
        elif "JUMP " in i:
            if i_str[1][0] == "s":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            rofl.append(f"JUMP regA")
        elif ":" in i_str[0]:
            rofl.append(i)
        elif "AR_SET_SIZE" in i:
            if i_str[2][0] == "s" or i_str[2][0] == "a":
                rofl.append(f"LOAD {i_str[2][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regA")
            rofl.append(f"LOAD 0 regB")
            rofl.append(f"STORE regB {i_str[1][1:]}")
            rofl.append(f"STORE regA regB")
            rofl.append(f"ADD regA regB regC")
            rofl.append(f"ADD 1 regC regC")
            rofl.append(f"STORE regC 0")
        elif "AR_GET_SIZE" in i:
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            rofl.append(f"LOAD regA regB")
            rofl.append(f"STORE regB {i_str[2][1:]}")
        elif "AR_GET_IDX" in i:
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            if i_str[2][0] == "s" or i_str[2][0] == "a":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            rofl.append(f"ADD regA 1 regC")
            rofl.append(f"ADD regC regB regC")
            rofl.append(f"LOAD regC regD")
            rofl.append(f"STORE regD {i_str[3][1:]}")
        elif "AR_SET_IDX" in i:
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            if i_str[2][0] == "s" or i_str[2][0] == "a":
                rofl.append(f"LOAD {i_str[2][1:]} regB")
            else:
                rofl.append(f"VAL_COPY {i_str[2]} regB")
            if i_str[3][0] == "s" or i_str[3][0] == "a":
                rofl.append(f"LOAD {i_str[3][1:]} regC")
            else:
                rofl.append(f"VAL_COPY {i_str[3]} regC")
            rofl.append(f"ADD regA 1 regD")
            rofl.append(f"ADD regD regB regD")
            rofl.append(f"STORE regC regD")
        elif "AR_COPY" in i:
            #set size
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            rofl.append(f"LOAD regA regB")
            rofl.append(f"LOAD 0 regC")
            rofl.append(f"STORE regC {i_str[2][1:]}")
            rofl.append(f"STORE regB regC")
            rofl.append(f"ADD regB regC regD")
            rofl.append(f"ADD 1 regD regD")
            rofl.append(f"STORE regD 0")
            rofl.append(f"STORE regB 10000000000")
            #set index loop
            rofl.append(f"VAL_COPY ar_copy_loop_end_{count+1} regC")
            rofl.append(f"VAL_COPY 0 regF")
            rofl.append(f"ar_copy_loop_start_{count}:")
            rofl.append(f"LOAD 10000000000 regB")
            rofl.append(f"TEST_LTE regF regB regG")
            rofl.append(f"JUMP_IF_0 regG regC")
            #get index
            rofl.append(f"LOAD {i_str[1][1:]} regA")
            rofl.append(f"ADD regA 1 regB")
            rofl.append(f"ADD regB regF regB")
            rofl.append(f"LOAD regB regD")
            #set index
            rofl.append(f"LOAD {i_str[2][1:]} regA")
            rofl.append(f"VAL_COPY regD regB")
            rofl.append(f"ADD regA 1 regE")
            rofl.append(f"ADD regE regF regE")
            rofl.append(f"STORE regB regE")
            #end loop
            rofl.append(f"ADD 1 regF regF")
            rofl.append(f"JUMP ar_copy_loop_start_{count}")
            rofl.append(f"ar_copy_loop_end_{count+1}:")
        elif "POP" in i:
            rofl.append(f"SUB regH 1 regH")
            rofl.append(f"LOAD regH regA")
            rofl.append(f"STORE regA {i_str[1][1:]}")
        elif "PUSH" in i:
            if i_str[1][0] == "s" or i_str[1][0] == "a":
                rofl.append(f"LOAD {i_str[1][1:]} regA")
            else:
                rofl.append(f"VAL_COPY {i_str[1]} regA")
            rofl.append(f"STORE regA regH")
            rofl.append(f"ADD 1 regH regH")
    count += 2
    return "\n".join(rofl)+"\n"


