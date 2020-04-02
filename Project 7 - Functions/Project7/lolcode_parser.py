from . rply import ParserGenerator
from . symbol_table import SymbolTable
from . lolcode_lexer import build_lexer
from . ast_nodes import *



class ParseError(Exception): pass
class LexError(Exception): pass


def build_parser(possible_tokens):
    pg = ParserGenerator(possible_tokens)

    @pg.error
    def error_handler(token):
        raise Exception(f'{token} at position {token.source_pos} is unexpected.')

    @pg.production('start : optional_newlines HAI NUMBAR_LITERAL optional_newlines statements KTHXBYE optional_newlines')
    def start(p):
        return StatementsNode(p[4])

    @pg.production('statements : statement newlines statements')
    def statements(p):
        #print(len(p[2]))
        if len(p[2]) == 0:
            return [p[0]]
        else:
            return [p[0]]+p[2]

    @pg.production('statements : ')
    def statements_empty(p):
        return []

    @pg.production('lit_type : PRIMITIVE_TYPE')
    def primitive_type(p):
        return p[0]

    @pg.production('lit_type_declaration : ITZ A lit_type')
    def primitive_type_declaration(p):
        return p[2]

    @pg.production('statement : I HAS A IDENTIFIER lit_type_declaration optional_init')
    def declaration_or_intialization(p):
        #print(p[5])
        name = p[3].value
        if not p[5]:
            dnode = DeclNode(name, '', p[4].value)
        else:
            val = p[5]
            dnode = DeclNode(name, val, p[4].value)
        return dnode

    @pg.production('statement : I HAS A IDENTIFIER ITZ LOTZ A lit_s optional_len')
    def declaration_or_intialization(p):
        if not p[8]:
            arr = ArDeclNode(p[3].value,'',p[7])
        else:
            arr = ArDeclNode(p[3].value,p[8],p[7])
        return arr

    @pg.production('statement : I HAS A IDENTIFIER ITZ A YARN optional_len')
    def declaration_or_intialization(p):
        if not p[7]:
            arr = ArDeclNode(p[3].value,'',"YARN")
        else:
            arr = ArDeclNode(p[3].value,p[7],"YARN")
        return arr

    @pg.production('optional_len : AN THAR IZ expression')
    def optional_len(p):
        return p[3]

    @pg.production('lit_s : NUMBRS')
    def lits_numbr(p):
        return "NUMBR"

    @pg.production('lit_s : NUMBARS')
    def lits_numbar(p):
        return "NUMBAR"

    @pg.production('lit_s : LETTRS')
    def lits_lettr(p):
        return "LETTR"

    @pg.production('lit_s : TROOFS')
    def lits_troof(p):
        return "TROOF"

    @pg.production('expression : IDENT\'Z expression')
    def get_indx(p):
        identz = p[0].value
        ident = identz[0:len(identz) - 2]
        if "NumbrLiteral" in str(p[1]):
            node = Ar_indxNode(ident, p[1], 0, 'r')
        else:
            node = Ar_indxNode(ident, p[1], 0, 'r')
        return node

    @pg.production('expression : IN IDENT\'Z expression PUT expression')
    def get_indx(p):
        identz = p[1].value
        ident = identz[0:len(identz) - 2]
        node = Ar_indxNode(ident, p[2], p[4], 'w')
        return node

    @pg.production('statement : O RLY? expression NEWLINE ifstate OIC')
    def orly(p):
        return OrlyNode(p[2], p[4])

    @pg.production('ifstate : yastate nostate')
    def ifstate(p):
        if p[1]:
            return [p[0],p[1]]
        else:
            return [p[0]]

    @pg.production('yastate : YA RLY NEWLINE statements')
    def yastate(p):
        return ifNode(p[3])

    @pg.production('nostate : NO WAI NEWLINE statements')
    def nostate(p):
        return ifNode(p[3])

    @pg.production('nostate : ')
    def nostate_empty(p):
        pass

    #@pg.production('mebbestates : MEBBE expression statements')
    #@pg.production('mebbestates : ')
    #def mebbestate(p):
    #    pass

    @pg.production('statement : IM IN YR LOOP optional_assignment optional_til newlines statements NOW IM OUTTA YR LOOP')
    def loop(p):
        assign_expression = p[4]
        til_expression = p[5]
        code_block = p[7]
        return LoopNode(code_block,til_expression,assign_expression)


    @pg.production('optional_til :')
    @pg.production('optional_til : TIL expression')
    def optional_assignment_expression(p):
        if not p:
            return None
        return p[1]

    @pg.production('optional_assignment :')
    @pg.production('optional_assignment : assignment_operation')
    def optional_assignment_expression(p):
        if not p:
            return None
        return p[0]

    @pg.production('statement : case')
    def exprtocase(p):
        return p[0]
    #@pg.production('case : ')
    #def case(p):
    #    pass
    @pg.production('code_block : statements')
    def codeblock(p):
        return p[0]
    @pg.production('case : WTF? expression NEWLINE optional_omgs optional_omgwtf OIC')
    def case(p):
        if p[3] == None:
            return SwitchNode(p[1])
        lit = [p[3][2*i] for i in range(int(len(p[3])/2))]
        body = [p[3][2*i+1] for i in range(int(len(p[3])/2))]
        return SwitchNode(p[1],lit,body,p[4])
    @pg.production('optional_omgs : ')
    def emptyomg(p):
        return []
    @pg.production('optional_omgs : OMG literal NEWLINE code_block optional_omgs')
    def opomg(p):
        return [p[1],p[3]] + p[4]
    @pg.production('optional_omgwtf : ')
    def emptyomgwtf(p):
        return None
    @pg.production('optional_omgwtf : OMGWTF NEWLINE code_block')
    def omgwtf(p):
        return p[2]

    @pg.production('statement : GTFO')
    def brk(p):
        return BreakNode()

    @pg.production('optional_an : ')
    @pg.production('optional_an : AN')
    def optional_an(p):
        pass

    @pg.production('optional_init : ')
    def opinit(p):
        return []

    @pg.production('optional_init : optional_an ITZ expression')
    def intialization(p):
        return p[2]

    @pg.production('optional_bang : BANG')
    def bang(p):
        return 1
    @pg.production('optional_bang : ')
    def bang_empty(p):
        return 0

    @pg.production('statement : function')
    def statetofunc(p):
        return p[0]

    @pg.production('statement : found')
    def statetofound(p):
        return p[0]

    @pg.production('found : FOUND YR expression')
    def found(p):
        return FoundNode(p[2])

    @pg.production('return : IF U SAY SO ITZ A PRIMITIVE_TYPE')
    def return_(p):
        return [p[6].value]

    @pg.production('return : IF U SAY SO ITZ A YARN')
    def return_(p):
        return [p[6].value,"ARRAY"]

    @pg.production('return : IF U SAY SO ITZ LOTZ A lit_s')
    def return_(p):
        return [p[7],"ARRAY"]

    @pg.production('optional_params : ')
    def optional_params_empty(p):
        return None

    @pg.production('optional_params : optional_an YR IDENTIFIER ITZ A PRIMITIVE_TYPE optional_params')
    def optional_params(p):
        if p[6]:
            return [p[2].value,p[5].value]+p[6]
        return [p[2].value,p[5].value]

    @pg.production('optional_params : optional_an YR IDENTIFIER ITZ A YARN optional_params')
    def optional_params(p):
        if p[6]:
            return [p[2].value,p[5].value]+p[6]
        return [p[2].value,p[5].value]

    @pg.production('optional_params : optional_an YR IDENTIFIER ITZ LOTZ A lit_s optional_params')
    def optional_params(p):
        if p[7]:
            return [p[2].value,["ARRAY",p[6]]]+p[7]
        return [p[2].value,["ARRAY",p[6]]]

    @pg.production('function : HOW IZ I IDENTIFIER optional_params MKAY newlines statements return')
    def function(p):
        count = 0
        param_name = []
        param_type = []
        if p[4]:
            for i in p[4]:
                if i is None:
                    break
                if count % 2 == 0:
                    param_name.append(i)
                else:
                    param_type.append(i)
                count += 1
        if p[4]:
            return FuncNode(p[3].value, param_name,param_type,p[7],p[8])
        return FuncNode(p[3].value, p[4], p[4], p[7], p[8])

    @pg.production('expression : func_call')
    def exprtofunccall(p):
        return p[0]

    @pg.production('func_call : I IZ IDENTIFIER optional_args MKAY')
    def funccall(p):
        return FuncCallNode(p[2].value,p[3])

    @pg.production('optional_args : ')
    def args_empty(p):
        return None

    @pg.production('optional_args : optional_an YR expression optional_args')
    def args(p):
        if p[3]:
            return [p[2]]+p[3]
        return [p[2]]

    @pg.production('statement : VISIBLE expression an_expressions optional_bang')
    def visible(p):
        if p[3]:
            return VisibleNode([p[1]] + p[2], p[3])
        else:
            return VisibleNode([p[1]] + p[2], p[3])

    @pg.production('expression : LENGTHZ OF IDENTIFIER')
    def length(p):
        return LengthNode(p[2].value)

    @pg.production('expression : LENGTHZ OF YARN_LITERAL')
    def length(p):
        return YarnLenNode(YarnLiteral(p[2].value))

    @pg.production('expression : GIMMEH')
    def gimmeh(p):
        return GimmehNode()

    @pg.production('expression : WHATEVR')
    def whatevr(p):
        return RandomNode()

    @pg.production('literal : NUMBR_LITERAL')
    def numbr_literal(p):
        return NumbrLiteral(p[0].value)

    @pg.production('literal : TROOF_LITERAL')
    def troof_literal(p):
        return TroofLiteral(p[0].value)

    @pg.production('literal : LETTR_LITERAL')
    def troof_literal(p):
        return LettrLiteral(p[0].value)

    @pg.production('literal : YARN_LITERAL')
    def yarn_literal(p):
        return YarnLiteral(p[0].value)

    @pg.production('expression : literal')
    def literals_are_expressions(p):
        return p[0]

    @pg.production('var_use : IDENTIFIER')
    def variable_use(p):
        name = p[0].value
        node = Var_useNode(name)
        return node

    @pg.production('expression : var_use')
    def variable_use_is_expression(p):
        return p[0]

    @pg.production('expression : var_use R expression')
    def assignment(p):
        var = p[0].get_name()
        val = p[2]
        unode = Var_assignNode(var, val)
        return unode

    @pg.production('optional_by_clause :')
    def optional_by_clause_empty(p):
        return 'h'

    @pg.production('optional_by_clause : BY expression')
    def optional_by_clause(p):
        return p[1]

    @pg.production('expression : assignment_operation')
    def assignment_operator_is_expression(p):
        return p[0]

    @pg.production('assignment_operation : ASSIGNMENT_OPERATOR var_use optional_by_clause')
    def assignment_operation(p):
        name = p[1].get_name()
        if p[2] == 'h':
            node = Var_Incr(p[0].value, name, NumbrLiteral(1))
        else:
            node = Var_Incr(p[0].value, name, p[2])
        return node

    @pg.production('statement : expression')
    def expression_is_statement(p):
        return p[0]

    @pg.production('expression : MATH_BINARY_OPERATOR OF expression an_expression')
    def math_binary(p):
        operator = p[0].value
        lhs = p[2]
        rhs = p[3]
        return BinaryMathNode(operator, lhs, rhs)

    @pg.production('expression : MATH_UNARY_OPERATOR OF expression')
    def math_unary(p):
        operator = p[0].value
        lhs = p[2]
        return UnaryMathNode(operator, lhs)

    @pg.production('expression : LOGICAL_BINARY_OPERATOR OF expression an_expression')
    def logical_binary(p):
        operator = p[0].value
        lhs = p[2]
        rhs = p[3]
        return BinaryLogicNode(operator, lhs, rhs)

    @pg.production('expression : LOGICAL_UNARY_OPERATOR expression')
    def logical_unary(p):
        operator = p[0].value
        lhs = p[1]
        return UnaryLogicNode(operator, lhs)

    @pg.production('an_expression : optional_an expression')
    def an_expression(p):
        return p[1]

    @pg.production('an_expressions : ')
    def an_expressions_empty(p):
        return []

    @pg.production('an_expressions : an_expression an_expressions')
    def an_expressions(p):
        return [p[0]]+p[1]

    @pg.production('expression : LOGICAL_VARIABLE_OPERATOR OF an_expressions MKAY')
    def logical_variable_expression(p):
        operator = p[0].value
        operand = p[2]
        return ManyLogicNode(operator, operand)

    @pg.production('expression : COMPARISON_BINARY_OPERATOR expression an_expression')
    def logical_binary_expression(p):
        operator = p[0].value
        lhs = p[1]
        rhs = p[2]
        return BinaryCompNode(operator, lhs, rhs)

    @pg.production('optional_newlines : newlines')
    def optional_newlines(p):
        return p[0]

    @pg.production('optional_newlines : ')
    def optional_newlines_empty(p):
        return ""

    @pg.production('newlines : NEWLINE')
    def newlines(p):
        return "h"

    @pg.production('newlines : NEWLINE newlines')
    def optional_newlines(p):
        return "h"+p[1]

    return pg.build()


def parse_LOLcode(lolcode_str):
    lexer = build_lexer()
    #print([rule.re for rule in lexer.rules])


    possible_tokens = [rule.name for rule in lexer.rules]
    #print(possible_tokens)
    parser = build_parser(possible_tokens)
    if parser.lr_table.sr_conflicts:
        raise ParseError(f'Shift-reduce conflicts {parser.lr_table.sr_conflicts}')
    if parser.lr_table.rr_conflicts:
        raise ParseError(f'Reduce-reduce conflicts {parser.lr_table.rr_conflicts}')

    tokens = list(lexer.lex(lolcode_str))
    # check_for_lexing_errors(tokens)
    #print([(token, token.source_pos) for token in tokens])
    return parser.parse(iter(tokens))