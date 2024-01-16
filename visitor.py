from antlr4 import *
from parserpy.PythonLexer import PythonLexer
from parserpy.PythonParser import PythonParser
from parserpy.PythonVisitor import PythonVisitor
from antlr4.tree.Tree import TerminalNodeImpl
import re
from preprocess import pre_process
import time
import builtins
import json
from antlr4.error.ErrorListener import ErrorListener

NAME_TYPE = {
    "var_name",
    "class_name",
    "function_name",
    "param_name",
}


class ErrListener(ErrorListener):
    flag = False

    def __init__(self) -> None:
        super().__init__()

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        self.flag = True
        return super().syntaxError(recognizer, offendingSymbol, line, column, msg, e)

    def getFlag(self):
        return self.flag

    def setFlag(self, flag):
        self.flag = flag


class Visitor(PythonVisitor):

    indent_level = 0

    symbol_table = {}

    keywords_purple = {
        PythonLexer.ASYNC,
        PythonLexer.AWAIT,
        PythonLexer.BREAK,
        PythonLexer.CONTINUE,
        PythonLexer.RETURN,
        PythonLexer.RAISE,
        PythonLexer.YIELD,
        PythonLexer.IF,
        PythonLexer.ELIF,
        PythonLexer.ELSE,
        PythonLexer.FOR,
        PythonLexer.WHILE,
        PythonLexer.TRY,
        PythonLexer.EXCEPT,
        PythonLexer.FINALLY,
        PythonLexer.WITH,
        PythonLexer.ASSERT,
        PythonLexer.AS,
        PythonLexer.IMPORT,
        PythonLexer.FROM,
        PythonLexer.IN,
        PythonLexer.PASS,
    }

    keywords_blue = {
        PythonLexer.DEF,
        PythonLexer.CLASS,
        PythonLexer.LAMBDA,
        PythonLexer.GLOBAL,
        PythonLexer.DEL,
        PythonLexer.NOT,
        PythonLexer.IS,
        PythonLexer.NONE,
        PythonLexer.TRUE,
        PythonLexer.FALSE,
        PythonLexer.AND,
        PythonLexer.OR,
    }

    operators = {
        PythonLexer.T__0,
        PythonLexer.T__1,
        PythonLexer.T__2,
        PythonLexer.T__3,
        PythonLexer.T__4,
        PythonLexer.T__5,
        PythonLexer.T__6,
        PythonLexer.T__7,
        PythonLexer.T__8,
        PythonLexer.T__9,
        PythonLexer.T__10,
        PythonLexer.T__11,
        PythonLexer.T__12,
        PythonLexer.T__13,
        PythonLexer.ASSIGN,
        PythonLexer.AUGASSIGN,
        PythonLexer.COMPARISON_OPERATOR,
    }

    # 用于 NAME 的继承属性
    NAME_TABLE = {}

    def __init__(self):
        self.symbol_table = {
            "class": {},
            "function": {},
            "var": {},
        }
        builtin_exceptions = [obj for obj in dir(
            builtins) if isinstance(getattr(builtins, obj), type)]
        builtin_functions = [obj for obj in dir(
            builtins) if not isinstance(getattr(builtins, obj), type)]

        self.symbol_table["function"].update(
            {func: {} for func in builtin_functions})
        self.symbol_table["class"].update(
            {obj: {} for obj in builtin_exceptions})
        self.NAME_TABLE = {}
        super().__init__()

    def search_funcs(self, method_name, class_name=None):
        try:
            if not class_name:
                for key in self.symbol_table["function"].keys():
                    if key == method_name:
                        results = self.visit(
                            self.symbol_table["function"][key]["ctx"])
                        return f"<pre><code style='line-height: 1.2;'>{results}</code></pre>"
            else:
                for classes in self.symbol_table["class"].keys():
                    for key in self.symbol_table["class"][classes]["methods"].keys():
                        if key == method_name:
                            results = self.visit(
                                self.symbol_table["class"][classes]["methods"][key]["ctx"])
                            return f"<pre><code style='line-height: 1.2;'>{results}</code></pre>"
        except Exception:
            pass

        return ""

    def search_name(self, name):
        name_list = []
        for key in self.symbol_table["var"].keys():
            if key.startswith(name):
                name_list.append('\t'.join([key, "var"]))

        for key in self.symbol_table["class"].keys():
            if key.startswith(name):
                name_list.append('\t'.join([key, "class"]))

        for key in self.symbol_table["function"].keys():
            if key.startswith(name):
                name_list.append('\t'.join([key, "function"]))

        return name_list

    def generate_html(self, html_code):
        code = pre_process(html_code)
        lexer = PythonLexer(InputStream(code))
        stream = CommonTokenStream(lexer)
        stream.fill()

        stream.tokens = merge_hidden_tokens(stream.tokens)

        errListener = ErrListener()
        parser = PythonParser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(errListener)

        tree = parser.program()

        if errListener.getFlag():
            return (False, None)

        results = self.visit(tree)
        # 将所有\r\n换为\n
        results = re.sub(r'\r\n', '\n', results)
        with open('result.html', 'w', encoding='utf-8') as file:
            file.write(results)
        # print(json.dumps(visitor.symbol_table, indent=4))
        # print(json.dumps(self.symbol_table['var'], indent=4))
        return (True, results)

    def visitChildren(self, ctx):
        # 初始化一个列表来收集子节点的访问结果
        results = ""
        # 遍历所有子节点
        for i in range(ctx.getChildCount()):
            # 访问子节点并收集结果
            child = ctx.getChild(i)
            result = self.visit(child)

            if result is None:
                continue

            if isinstance(child, PythonParser.BlockContext):
                pass
                # print(ctx.start.line, ctx.start.column,
                #       ctx.stop.line, ctx.stop.column)

            if isinstance(child, PythonParser.DedentContext):
                if results[-2] == '\r':
                    results = results[:-2]
                else:
                    results = results[:-1]

            if isinstance(child, PythonParser.Fstring_content_doubleContext) or\
                    isinstance(child, PythonParser.Fstring_content_singleContext):
                result = re.sub(r'<.*?>', '', result)
            results += result
        # 返回收集到的结果
        return results

    def getNextSibling(self, ctx):
        parent = ctx.parentCtx
        for i in range(parent.getChildCount()):
            if parent.getChild(i) == ctx:
                return parent.getChild(i + 1)

    def getPreviousSibling(self, ctx):
        parent = ctx.parentCtx
        for i in range(parent.getChildCount()):
            if parent.getChild(i) == ctx:
                return parent.getChild(i - 1)

    def visitTerminal(self, node):
        match node.symbol.type:
            case -1:
                return ""
            case x if x in self.keywords_purple:
                return f'<span style="color: #BC53AE;">{node.symbol.text}</span>'
            case x if x in self.keywords_blue:
                return f'<span style="color: #3f6de0;">{node.symbol.text}</span>'
            case PythonLexer.COMMENT:
                return f'<span style="color: #b1b1b1;">{node.symbol.text}</span>'
            case x if x in self.operators:
                return f'<span style="color: #0088f8;">{node.symbol.text}</span>'
            case PythonLexer.INDENT | PythonLexer.DEDENT:
                return ""
            case PythonLexer.STRING:
                return f'<span style="color: #fd9729;">{node.symbol.text}</span>'
            case PythonLexer.NUMBER:
                return f'<span style="color: #6bdbb7;">{node.symbol.text}</span>'
            case PythonLexer.NAME:
                parent = node.parentCtx
                text = node.symbol.text.strip()

                if text in self.symbol_table["var"]:
                    return f'<span style="color: #00c8ff;">{node.symbol.text}</span>'
                elif text in self.symbol_table["class"]:
                    return f'<span style="color: #65c8af;">{node.symbol.text}</span>'
                elif text in self.symbol_table["function"]:
                    return f'<span style="color: #dbc900;">{node.symbol.text}</span>'

                if parent in self.NAME_TABLE:
                    if self.NAME_TABLE[parent] == "var_name":
                        # var_name的NAME节点

                        # 如果是赋值语句的左值
                        if isinstance(parent, PythonParser.Single_targetContext) and\
                           text not in self.symbol_table["var"]:
                            self.symbol_table["var"][text] = {
                                "name": text,
                            }
                            return f'<span style="color: #00c8ff;">{node.symbol.text}</span>'

                        return f'<span style="color: #00c8ff;">{node.symbol.text}</span>'

                    elif self.NAME_TABLE[parent] == "class_name":
                        # class_name的NAME节点
                        if isinstance(parent, PythonParser.Class_defContext) and\
                           text not in self.symbol_table["class"]:
                            self.symbol_table["class"][text] = {
                                "methods": {},
                            }
                        return f'<span style="color: #65c8af;">{node.symbol.text}</span>'

                    elif self.NAME_TABLE[parent] == "function_name":
                        # function_name的NAME节点
                        parent = parent.parentCtx
                        while not isinstance(parent, PythonParser.ProgramContext):
                            if isinstance(parent, PythonParser.Class_defContext):
                                if text not in self.symbol_table["class"][parent.NAME().symbol.text.strip()]["methods"]:
                                    self.symbol_table["class"][parent.NAME().symbol.text.strip()]["methods"][text] = {
                                        "ctx": parent,
                                        "name": text,
                                        "params": [],
                                    }
                                    return f'<span style="color: #dbc900;">{node.symbol.text}</span>'
                            parent = parent.parentCtx
                        parent = node.parentCtx
                        if isinstance(parent, PythonParser.Function_defContext) and\
                           text not in self.symbol_table["function"]:
                            self.symbol_table["function"][text] = {
                                "ctx": parent,
                                "name": text,
                                "params": [],
                            }
                        return f'<span style="color: #dbc900;">{node.symbol.text}</span>'

                    elif self.NAME_TABLE[parent] == "param_name":
                        # param_name的NAME节点
                        return f'<span style="color: #909090;">{node.symbol.text}</span>'

                return node.symbol.text
            case _:
                return node.symbol.text

    # Visit a parse tree produced by PythonParser#program.
    def visitProgram(self, ctx: PythonParser.ProgramContext):
        self.__init__()
        results = self.visitChildren(ctx)[:-1]
        return f"<strong><pre><code style='line-height: 1.2;'>{results}</code></pre></strong>"

    # Visit a parse tree produced by PythonParser#statement.
    def visitStatement(self, ctx: PythonParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#simple_stmts.
    def visitSimple_stmts(self, ctx: PythonParser.Simple_stmtsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#pass_stmt.
    def visitPass_stmt(self, ctx: PythonParser.Pass_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#break_stmt.
    def visitBreak_stmt(self, ctx: PythonParser.Break_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#continue_stmt.
    def visitContinue_stmt(self, ctx: PythonParser.Continue_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#compound_stmts.
    def visitCompound_stmts(self, ctx: PythonParser.Compound_stmtsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#assignment.
    def visitAssignment(self, ctx: PythonParser.AssignmentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#return_stmt.
    def visitReturn_stmt(self, ctx: PythonParser.Return_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#raise_stmt.
    def visitRaise_stmt(self, ctx: PythonParser.Raise_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#global_stmt.
    def visitGlobal_stmt(self, ctx: PythonParser.Global_stmtContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#comment.
    def visitComment(self, ctx: PythonParser.CommentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#del_stmt.
    def visitDel_stmt(self, ctx: PythonParser.Del_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#yield_stmt.
    def visitYield_stmt(self, ctx: PythonParser.Yield_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#assert_stmt.
    def visitAssert_stmt(self, ctx: PythonParser.Assert_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_stmt.
    def visitImport_stmt(self, ctx: PythonParser.Import_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_name.
    def visitImport_name(self, ctx: PythonParser.Import_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_from.
    def visitImport_from(self, ctx: PythonParser.Import_fromContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_from_targets.
    def visitImport_from_targets(self, ctx: PythonParser.Import_from_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_from_as_names.
    def visitImport_from_as_names(self, ctx: PythonParser.Import_from_as_namesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#import_from_as_name.
    def visitImport_from_as_name(self, ctx: PythonParser.Import_from_as_nameContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#dotted_as_names.
    def visitDotted_as_names(self, ctx: PythonParser.Dotted_as_namesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#dotted_name.
    def visitDotted_name(self, ctx: PythonParser.Dotted_nameContext):
        self.NAME_TABLE[ctx] = "class_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#block.
    def visitBlock(self, ctx: PythonParser.BlockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#indent.
    def visitIndent(self, ctx: PythonParser.IndentContext):
        results = self.visitChildren(ctx)
        return re.sub(r'(\r?\n)+', '', results)

    # Visit a parse tree produced by PythonParser#dedent.
    def visitDedent(self, ctx: PythonParser.DedentContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#decorators.
    def visitDecorators(self, ctx: PythonParser.DecoratorsContext):
        self.NAME_TABLE[ctx] = "function_name"
        return f"<span style='color: #dbc900;'>{self.visitChildren(ctx)}</span>"

    # Visit a parse tree produced by PythonParser#class_def.
    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        self.NAME_TABLE[ctx] = "class_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#function_def.
    def visitFunction_def(self, ctx: PythonParser.Function_defContext):
        self.NAME_TABLE[ctx] = "function_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#parameters.
    def visitParameters(self, ctx: PythonParser.ParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_etc.
    def visitStar_etc(self, ctx: PythonParser.Star_etcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#kwds.
    def visitKwds(self, ctx: PythonParser.KwdsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#param_no_default.
    def visitParam_no_default(self, ctx: PythonParser.Param_no_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#param_with_default.
    def visitParam_with_default(self, ctx: PythonParser.Param_with_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#param_maybe_default.
    def visitParam_maybe_default(self, ctx: PythonParser.Param_maybe_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#param.
    def visitParam(self, ctx: PythonParser.ParamContext):
        self.NAME_TABLE[ctx] = "param_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#annotation.
    def visitAnnotation(self, ctx: PythonParser.AnnotationContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#default.
    def visitDefault(self, ctx: PythonParser.DefaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#if_stmt.
    def visitIf_stmt(self, ctx: PythonParser.If_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#elif_stmt.
    def visitElif_stmt(self, ctx: PythonParser.Elif_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#else_block.
    def visitElse_block(self, ctx: PythonParser.Else_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#while_stmt.
    def visitWhile_stmt(self, ctx: PythonParser.While_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#for_stmt.
    def visitFor_stmt(self, ctx: PythonParser.For_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#with_stmt.
    def visitWith_stmt(self, ctx: PythonParser.With_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#with_item.
    def visitWith_item(self, ctx: PythonParser.With_itemContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#try_stmt.
    def visitTry_stmt(self, ctx: PythonParser.Try_stmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#except_block.
    def visitExcept_block(self, ctx: PythonParser.Except_blockContext):
        self.NAME_TABLE[ctx] = "class_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#except_star_block.
    def visitExcept_star_block(self, ctx: PythonParser.Except_star_blockContext):
        self.NAME_TABLE[ctx] = "class_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#except_var.
    def visitExcept_var(self, ctx: PythonParser.Except_varContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#finally_block.

    def visitFinally_block(self, ctx: PythonParser.Finally_blockContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#yield_expr.
    def visitYield_expr(self, ctx: PythonParser.Yield_exprContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_expression.
    def visitStar_expression(self, ctx: PythonParser.Star_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_named_expression.
    def visitStar_named_expression(self, ctx: PythonParser.Star_named_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#assignment_expression.
    def visitAssignment_expression(self, ctx: PythonParser.Assignment_expressionContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#named_expression.
    def visitNamed_expression(self, ctx: PythonParser.Named_expressionContext):
        self.NAME_TABLE[ctx] = self.NAME_TABLE.get(ctx.parentCtx, "var_name")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#expression.
    def visitExpression(self, ctx: PythonParser.ExpressionContext):
        self.NAME_TABLE[ctx] = self.NAME_TABLE.get(ctx.parentCtx, "var_name")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#comparison.
    def visitComparison(self, ctx: PythonParser.ComparisonContext):
        self.NAME_TABLE[ctx] = self.NAME_TABLE.get(ctx.parentCtx, "var_name")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#factor.
    def visitFactor(self, ctx: PythonParser.FactorContext):
        self.NAME_TABLE[ctx] = self.NAME_TABLE.get(ctx.parentCtx, "var_name")
        if isinstance(ctx.getChild(0), PythonParser.AtomContext):
            if ctx.getChildCount() == 2:
                ctx_child = ctx.getChild(1)
                if isinstance(ctx_child, PythonParser.PrimaryContext) and \
                   (isinstance(ctx_child.getChild(0), PythonParser.GenexpContext) or
                    (isinstance(ctx_child.getChild(0), TerminalNodeImpl) and
                     ctx_child.getChild(0).symbol.type == PythonLexer.LBAR)):
                    self.NAME_TABLE[ctx] = "function_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#primary.
    def visitPrimary(self, ctx: PythonParser.PrimaryContext):
        self.NAME_TABLE[ctx] = "var_name"
        if isinstance(ctx.getChild(0), TerminalNodeImpl) and \
                (ctx.getChild(0).symbol.type == PythonLexer.DOT):
            next_sibling = self.getNextSibling(ctx)
            if next_sibling is not None:
                if isinstance(next_sibling.getChild(0), PythonParser.GenexpContext) or\
                    (isinstance(next_sibling.getChild(0), TerminalNodeImpl) and
                     next_sibling.getChild(0).symbol.type == PythonLexer.LBAR):
                    self.NAME_TABLE[ctx] = "function_name"
                else:
                    self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#slices.
    def visitSlices(self, ctx: PythonParser.SlicesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#slice.
    def visitSlice(self, ctx: PythonParser.SliceContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#atom.
    def visitAtom(self, ctx: PythonParser.AtomContext):
        parent = ctx.parentCtx
        self.NAME_TABLE[ctx] = self.NAME_TABLE.get(parent, "var_name")
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#group.
    def visitGroup(self, ctx: PythonParser.GroupContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambdef.
    def visitLambdef(self, ctx: PythonParser.LambdefContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_params.
    def visitLambda_params(self, ctx: PythonParser.Lambda_paramsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_parameters.
    def visitLambda_parameters(self, ctx: PythonParser.Lambda_parametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_star_etc.
    def visitLambda_star_etc(self, ctx: PythonParser.Lambda_star_etcContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_kwds.
    def visitLambda_kwds(self, ctx: PythonParser.Lambda_kwdsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_no_default.
    def visitLambda_param_no_default(self, ctx: PythonParser.Lambda_param_no_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_with_default.
    def visitLambda_param_with_default(self, ctx: PythonParser.Lambda_param_with_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_maybe_default.
    def visitLambda_param_maybe_default(self, ctx: PythonParser.Lambda_param_maybe_defaultContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param.
    def visitLambda_param(self, ctx: PythonParser.Lambda_paramContext):
        self.NAME_TABLE[ctx] = "param_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#fstring_replacement_field.
    def visitFstring_replacement_field(self, ctx: PythonParser.Fstring_replacement_fieldContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#fstring_content_single.
    def visitFstring_content_single(self, ctx: PythonParser.Fstring_content_singleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#fstring_content_double.
    def visitFstring_content_double(self, ctx: PythonParser.Fstring_content_doubleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#fstring.
    def visitFstring(self, ctx: PythonParser.FstringContext):
        results = self.visitChildren(ctx)
        return f"<span style='color: #fd9729;'>{results}</span>"

    # Visit a parse tree produced by PythonParser#string.
    def visitString(self, ctx: PythonParser.StringContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#strings.
    def visitStrings(self, ctx: PythonParser.StringsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#dict.
    def visitDict(self, ctx: PythonParser.DictContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#list.
    def visitList(self, ctx: PythonParser.ListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#tuple.
    def visitTuple(self, ctx: PythonParser.TupleContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#set.
    def visitSet(self, ctx: PythonParser.SetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#double_starred_kvpairs.
    def visitDouble_starred_kvpairs(self, ctx: PythonParser.Double_starred_kvpairsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#double_starred_kvpair.
    def visitDouble_starred_kvpair(self, ctx: PythonParser.Double_starred_kvpairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#kvpair.
    def visitKvpair(self, ctx: PythonParser.KvpairContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#for_if_clauses.
    def visitFor_if_clauses(self, ctx: PythonParser.For_if_clausesContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#for_if_clause.
    def visitFor_if_clause(self, ctx: PythonParser.For_if_clauseContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#listcomp.
    def visitListcomp(self, ctx: PythonParser.ListcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#setcomp.
    def visitSetcomp(self, ctx: PythonParser.SetcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#genexp.
    def visitGenexp(self, ctx: PythonParser.GenexpContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#dictcomp.
    def visitDictcomp(self, ctx: PythonParser.DictcompContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#arguments.
    def visitArguments(self, ctx: PythonParser.ArgumentsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#args.
    def visitArgs(self, ctx: PythonParser.ArgsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#kwargs.
    def visitKwargs(self, ctx: PythonParser.KwargsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#starred_expression.
    def visitStarred_expression(self, ctx: PythonParser.Starred_expressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#kwarg_or_starred.
    def visitKwarg_or_starred(self, ctx: PythonParser.Kwarg_or_starredContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#kwarg_or_double_starred.
    def visitKwarg_or_double_starred(self, ctx: PythonParser.Kwarg_or_double_starredContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_targets.
    def visitStar_targets(self, ctx: PythonParser.Star_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_targets_list_seq.
    def visitStar_targets_list_seq(self, ctx: PythonParser.Star_targets_list_seqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_targets_tuple_seq.
    def visitStar_targets_tuple_seq(self, ctx: PythonParser.Star_targets_tuple_seqContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_target.
    def visitStar_target(self, ctx: PythonParser.Star_targetContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#target_with_star_atom.
    def visitTarget_with_star_atom(self, ctx: PythonParser.Target_with_star_atomContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#star_atom.
    def visitStar_atom(self, ctx: PythonParser.Star_atomContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#single_target.
    def visitSingle_target(self, ctx: PythonParser.Single_targetContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#single_subscript_attribute_target.
    def visitSingle_subscript_attribute_target(self, ctx: PythonParser.Single_subscript_attribute_targetContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#t_primary.
    def visitT_primary(self, ctx: PythonParser.T_primaryContext):
        self.NAME_TABLE[ctx] = "var_name"
        if isinstance(ctx.getChild(0), PythonParser.AtomContext):
            sibling = self.getNextSibling(ctx)
            if sibling is not None:
                if isinstance(sibling, PythonParser.GenexpContext) or\
                    (isinstance(sibling, TerminalNodeImpl) and
                     sibling.symbol.type == PythonLexer.LBAR):
                    self.NAME_TABLE[sibling] = "function_name"
                else:
                    self.NAME_TABLE[sibling] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#del_targets.
    def visitDel_targets(self, ctx: PythonParser.Del_targetsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#del_target.
    def visitDel_target(self, ctx: PythonParser.Del_targetContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)

    # Visit a parse tree produced by PythonParser#del_t_atom.
    def visitDel_t_atom(self, ctx: PythonParser.Del_t_atomContext):
        self.NAME_TABLE[ctx] = "var_name"
        return self.visitChildren(ctx)


def merge_hidden_tokens(tokens, hidden_channel=PythonLexer.HIDDEN):
    merged_tokens = []
    for token in tokens:
        if token.channel == hidden_channel:
            if merged_tokens:
                merged_tokens[-1].text += token.text
        else:
            merged_tokens.append(token)
    return merged_tokens


if __name__ == '__main__':
    html_code = """import math
import random
import sys
from functools import wraps
from parserpy.PythonLexer import PythonLexer


# 示例注释效果


class AnotherClass:
    def __init__(self, data: list, mapping: dict):
        self.data = data
        self.mapping = mapping

    def compute_sum(self) -> int:
        return sum(self.data)

    def compute_max(self) -> int:
        return max(self.data, default=0)

    @staticmethod
    def static_method_example():
        return "This is a static method"

    @classmethod
    def class_method_example(cls):
        return cls.__name__

    def get_mapping(self) -> dict[str, int]:
        return self.mapping


class MyClass:
    def __init__(self, x: int, y: int, another_object: AnotherClass):
        self.x = x
        self.y = y
        self.another_object = another_object

    def print_coordinates(self):
        print(f"Coordinates: ({self.x}, {self.y})")

    def perform_calculations(self):
        print(f"Sum of data: {self.another_object.compute_sum()}")
        print(f"Max of data: {self.another_object.compute_max()}")
        print(f"Mapping: {self.another_object.get_mapping()}")

    def update_coordinates(self, new_x: int, new_y: int):
        self.x = new_x
        self.y = new_y


def my_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Function {func.__name__} is being called")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} call finished")
        return result
    return wrapper


@my_decorator
def my_function(file_name: str):
    try:
        with open(file_name, "r") as file:
            for line in file:
                if random.randint(0, 1) == 0:
                    raise ValueError("Random error occurred")
                print(line.strip())
    except FileNotFoundError:
        print("File not found")
    except ValueError as e:
        print(f"ValueError: {e}")
    finally:
        print("Execution of my_function completed")
        return None


def complex_logic(n: int) -> list[int]:
    nested_result = [i ** 2 for i in range(n) if i % 3 != 0]
    return nested_result


# 测试嵌套循环和条件语句
for i in range(10):
    if i % 2 == 0:
        print(f"{i} is even")
        for j in range(i):
            if j % 3 == 0:
                print(f"{j} is a multiple of 3")
    else:
        print(f"{i} is odd")

# 创建对象和调用函数
another_object = AnotherClass([1, 2, 3, 4, 5], {"one": 1, "two": 2})
my_object = MyClass(3, 4, another_object)
my_object.print_coordinates()
my_object.perform_calculations()
my_function("test.txt")

# 测试lambda函数和列表解析
squared = lambda x: x**2
print([squared(x) for x in range(10)])

# 测试集合和生成器表达式
unique_squares = {x**2 for x in range(-5, 6)}
generator_example = (x**2 for x in range(10))

# 测试异步编程元素
import asyncio

async def async_example():
    await asyncio.sleep(1)
    print("Asynchronous execution")

asyncio.run(async_example())

"""
    visitor = Visitor()
    visitor.generate_html(html_code)
