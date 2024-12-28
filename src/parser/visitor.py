# Generated from src/parser/grammar/PythonParser.g4 by ANTLR 4.13.2
from typing import Union, cast
from antlr4 import InputStream, ParseTreeVisitor, ParserRuleContext, FileStream

from parser.ast import ast
from parser.grammar.PythonParser import PythonParser


class FeatureNotImplementedError(NotImplementedError):
    def __init__(self, ctx: ParserRuleContext):
        source = cast(InputStream, ctx.start.source[1])

        position = f":{ctx.start.line}:{ctx.start.column+1}"
        if isinstance(source, FileStream):
            position = f"{source.fileName}{position}"

        lines: list[str] = source.strdata.split("\n")
        lines = lines[ctx.start.line - 2 : ctx.stop.line]
        lines.insert(2, " " * ctx.start.column + "\033[1m\033[31m^ feature not implemented\033[0m")
        lines.insert(3, "")

        issue_lines = "\n".join(lines)

        super().__init__(
            f"\033[1m\033[31mError\033[0m\033[1m: feature not implemented\033[0m\n --> {position}:\n\n{issue_lines}",
        )


class Visitor(ParseTreeVisitor):
    import_paths = ["src/builtin"]

    # Visit a parse tree produced by PythonParser#file_input.
    def visitFile_input(self, ctx: PythonParser.File_inputContext) -> ast.ProgramAST:
        statements_ast = self.visitStatements(ctx.statements())
        return ast.ProgramAST(
            statements=statements_ast,
        )

    # Visit a parse tree produced by PythonParser#interactive.
    def visitInteractive(self, ctx: PythonParser.InteractiveContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#eval.
    def visitEval(self, ctx: PythonParser.EvalContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#func_type.
    def visitFunc_type(self, ctx: PythonParser.Func_typeContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_input.
    def visitFstring_input(self, ctx: PythonParser.Fstring_inputContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#statements.
    def visitStatements(
        self, ctx: PythonParser.StatementsContext
    ) -> list[ast.StatementAST]:
        asts = list[ast.StatementAST]()
        statements_ctx = cast(list[PythonParser.StatementContext], ctx.statement())

        for statement in statements_ctx:
            asts.extend(self.visitStatement(statement))

        return asts

    # Visit a parse tree produced by PythonParser#statement.
    def visitStatement(
        self, ctx: PythonParser.StatementContext
    ) -> list[ast.StatementAST]:
        if simple_stmts_ctx := cast(
            Union[PythonParser.Simple_stmtsContext, None], ctx.simple_stmts()
        ):
            return self.visitSimple_stmts(simple_stmts_ctx)

        if compound_stmt_ctx := cast(
            Union[PythonParser.Compound_stmtContext, None], ctx.compound_stmt()
        ):
            return [self.visitCompound_stmt(compound_stmt_ctx)]

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#statement_newline.
    def visitStatement_newline(self, ctx: PythonParser.Statement_newlineContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#simple_stmts.
    def visitSimple_stmts(
        self, ctx: PythonParser.Simple_stmtsContext
    ) -> list[ast.StatementAST]:
        asts = list[ast.StatementAST]()
        simple_stmt_ctx = cast(list[PythonParser.Simple_stmtContext], ctx.simple_stmt())

        for simple_stmt in simple_stmt_ctx:
            asts.append(self.visitSimple_stmt(simple_stmt))

        return asts

    # assignment
    # | type_alias
    # | star_expressions
    # | return_stmt
    # | import_stmt
    # | raise_stmt
    # | 'pass'
    # | del_stmt
    # | yield_stmt
    # | assert_stmt
    # | 'break'
    # | 'continue'
    # | global_stmt
    # | nonlocal_stmt;

    # Visit a parse tree produced by PythonParser#simple_stmt.
    def visitSimple_stmt(
        self, ctx: PythonParser.Simple_stmtContext
    ) -> ast.StatementAST:
        if assignment_ctx := cast(
            Union[PythonParser.AssignmentContext, None], ctx.assignment()
        ):
            return self.visitAssignment(assignment_ctx)

        if type_alias_ctx := cast(
            Union[PythonParser.Type_aliasContext, None], ctx.type_alias()
        ):
            return self.visitType_alias(type_alias_ctx)

        if star_expressions_ctx := cast(
            Union[PythonParser.Star_expressionsContext, None], ctx.star_expressions()
        ):
            return ast.ExpressionsStatementAST(
                expressions=self.visitStar_expressions(star_expressions_ctx),
            )

        if return_stmt_ctx := cast(
            Union[PythonParser.Return_stmtContext, None], ctx.return_stmt()
        ):
            return self.visitReturn_stmt(return_stmt_ctx)

        if import_stmt_ctx := cast(
            Union[PythonParser.Import_stmtContext, None], ctx.import_stmt()
        ):
            return self.visitImport_stmt(import_stmt_ctx)

        if raise_stmt_ctx := cast(
            Union[PythonParser.Raise_stmtContext, None], ctx.raise_stmt()
        ):
            return self.visitRaise_stmt(raise_stmt_ctx)

        if ctx.PASS():
            return ast.PassStatementAST()

        if del_stmt_ctx := cast(
            Union[PythonParser.Del_stmtContext, None], ctx.del_stmt()
        ):
            return self.visitDel_stmt(del_stmt_ctx)

        if yield_stmt_ctx := cast(
            Union[PythonParser.Yield_stmtContext, None], ctx.yield_stmt()
        ):
            return self.visitYield_stmt(yield_stmt_ctx)

        if assert_stmt_ctx := cast(
            Union[PythonParser.Assert_stmtContext, None], ctx.assert_stmt()
        ):
            return self.visitAssert_stmt(assert_stmt_ctx)

        if ctx.BREAK():
            return ast.BreakStatementAST()

        if ctx.CONTINUE():
            return ast.ContinueStatementAST()

        if global_stmt_ctx := cast(
            Union[PythonParser.Global_stmtContext, None], ctx.global_stmt()
        ):
            return self.visitGlobal_stmt(global_stmt_ctx)

        if nonlocal_stmt_ctx := cast(
            Union[PythonParser.Nonlocal_stmtContext, None], ctx.nonlocal_stmt()
        ):
            return self.visitNonlocal_stmt(nonlocal_stmt_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#compound_stmt.
    def visitCompound_stmt(
        self, ctx: PythonParser.Compound_stmtContext
    ) -> ast.StatementAST:
        if function_def_ctx := cast(
            Union[PythonParser.Function_defContext, None], ctx.function_def()
        ):
            return self.visitFunction_def(function_def_ctx)

        if if_stmt_ctx := cast(Union[PythonParser.If_stmtContext, None], ctx.if_stmt()):
            return self.visitIf_stmt(if_stmt_ctx)

        if class_def_ctx := cast(
            Union[PythonParser.Class_defContext, None], ctx.class_def()
        ):
            return self.visitClass_def(class_def_ctx)

        if with_stmt_ctx := cast(
            Union[PythonParser.With_stmtContext, None], ctx.with_stmt()
        ):
            return self.visitWith_stmt(with_stmt_ctx)

        if for_stmt_ctx := cast(
            Union[PythonParser.For_stmtContext, None], ctx.for_stmt()
        ):
            return self.visitFor_stmt(for_stmt_ctx)

        if try_stmt_ctx := cast(
            Union[PythonParser.Try_stmtContext, None], ctx.try_stmt()
        ):
            return self.visitTry_stmt(try_stmt_ctx)

        if while_stmt_ctx := cast(
            Union[PythonParser.While_stmtContext, None], ctx.while_stmt()
        ):
            return self.visitWhile_stmt(while_stmt_ctx)

        if match_stmt_ctx := cast(
            Union[PythonParser.Match_stmtContext, None], ctx.match_stmt()
        ):
            return self.visitMatch_stmt(match_stmt_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#assignment.
    def visitAssignment(self, ctx: PythonParser.AssignmentContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#annotated_rhs.
    def visitAnnotated_rhs(self, ctx: PythonParser.Annotated_rhsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#augassign.
    def visitAugassign(self, ctx: PythonParser.AugassignContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#return_stmt.
    def visitReturn_stmt(self, ctx: PythonParser.Return_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#raise_stmt.
    def visitRaise_stmt(self, ctx: PythonParser.Raise_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#global_stmt.
    def visitGlobal_stmt(self, ctx: PythonParser.Global_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#nonlocal_stmt.
    def visitNonlocal_stmt(self, ctx: PythonParser.Nonlocal_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#del_stmt.
    def visitDel_stmt(self, ctx: PythonParser.Del_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#yield_stmt.
    def visitYield_stmt(self, ctx: PythonParser.Yield_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#assert_stmt.
    def visitAssert_stmt(self, ctx: PythonParser.Assert_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#import_stmt.
    def visitImport_stmt(
        self, ctx: PythonParser.Import_stmtContext
    ) -> ast.MultipleStatementAST:
        if import_name_ctx := cast(
            Union[PythonParser.Import_nameContext, None], ctx.import_name()
        ):
            import_statement_asts = self.visitImport_name(import_name_ctx)
            return ast.MultipleStatementAST(statements=import_statement_asts)

        if import_from_ctx := cast(
            Union[PythonParser.Import_fromContext, None], ctx.import_from()
        ):
            import_statement_asts = self.visitImport_from(import_from_ctx)
            return ast.MultipleStatementAST(statements=import_statement_asts)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#import_name.
    def visitImport_name(
        self, ctx: PythonParser.Import_nameContext
    ) -> list[ast.ImportStatementAST]:
        return self.visitDotted_as_names(ctx.dotted_as_names())

    # Visit a parse tree produced by PythonParser#import_from.
    def visitImport_from(
        self, ctx: PythonParser.Import_fromContext
    ) -> list[ast.ImportStatementAST]:
        if ctx.DOT() or ctx.ELLIPSIS():
            raise FeatureNotImplementedError(ctx)

        dotted_name_ctx = cast(
            Union[PythonParser.Dotted_nameContext, None], ctx.dotted_name()
        )
        if dotted_name_ctx is None:
            raise FeatureNotImplementedError(ctx)

        import_statement_ast = self.visitDotted_name(dotted_name_ctx)

        import_statement_asts = list[ast.ImportStatementAST]()

        if import_from_targets_ctx := cast(
            Union[PythonParser.Import_from_targetsContext, None],
            ctx.import_from_targets(),
        ):
            for target_import_statement_ast in self.visitImport_from_targets(
                import_from_targets_ctx
            ):
                target_import_statement_ast.path = (
                    import_statement_ast.path + target_import_statement_ast.path
                )

                import_statement_asts.append(target_import_statement_ast)

            return import_statement_asts

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#import_from_targets.
    def visitImport_from_targets(self, ctx: PythonParser.Import_from_targetsContext):
        if ctx.STAR():
            raise FeatureNotImplementedError(ctx)

        return self.visitImport_from_as_names(ctx.import_from_as_names())

    # Visit a parse tree produced by PythonParser#import_from_as_names.
    def visitImport_from_as_names(self, ctx: PythonParser.Import_from_as_namesContext):
        import_statement_asts = list[ast.ImportStatementAST]()

        for import_from_as_name_ctx in ctx.import_from_as_name():
            import_statement_ast = self.visitImport_from_as_name(
                import_from_as_name_ctx
            )
            import_statement_asts.append(import_statement_ast)

        return import_statement_asts

    # Visit a parse tree produced by PythonParser#import_from_as_name.
    def visitImport_from_as_name(self, ctx: PythonParser.Import_from_as_nameContext):
        path = ctx.NAME(0).getText()
        import_statement_ast = ast.ImportStatementAST(path=[path])

        if alias := ctx.NAME(1):
            import_statement_ast.alias = alias.getText()

        return import_statement_ast

    # Visit a parse tree produced by PythonParser#dotted_as_names.
    def visitDotted_as_names(self, ctx: PythonParser.Dotted_as_namesContext):
        import_statement_asts = list[ast.ImportStatementAST]()

        for dotted_as_name_ctx in ctx.dotted_as_name():
            import_statement_asts.append(self.visitDotted_as_name(dotted_as_name_ctx))

        return import_statement_asts

    # Visit a parse tree produced by PythonParser#dotted_as_name.
    def visitDotted_as_name(
        self, ctx: PythonParser.Dotted_as_nameContext
    ) -> ast.ImportStatementAST:
        import_statement_ast = self.visitDotted_name(ctx.dotted_name())

        if alias := ctx.NAME():
            import_statement_ast.alias = alias.getText()

        return import_statement_ast

    # Visit a parse tree produced by PythonParser#dotted_name.
    def visitDotted_name(
        self, ctx: PythonParser.Dotted_nameContext
    ) -> ast.ImportStatementAST:
        name = ctx.NAME().getText()

        if dotted_name_ctx := cast(
            Union[PythonParser.Dotted_nameContext, None], ctx.dotted_name()
        ):
            import_statement_ast = self.visitDotted_name(dotted_name_ctx)
            import_statement_ast.path.append(name)

            return import_statement_ast

        return ast.ImportStatementAST(path=[name])

    # Visit a parse tree produced by PythonParser#block.
    def visitBlock(self, ctx: PythonParser.BlockContext):
        if statements_ctx := cast(
            Union[PythonParser.StatementsContext, None], ctx.statements()
        ):
            return self.visitStatements(statements_ctx)

        if simple_stmts_ctx := cast(
            Union[PythonParser.Simple_stmtsContext, None], ctx.simple_stmts()
        ):
            return self.visitSimple_stmts(simple_stmts_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#decorators.
    def visitDecorators(self, ctx: PythonParser.DecoratorsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#class_def.
    def visitClass_def(self, ctx: PythonParser.Class_defContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#class_def_raw.
    def visitClass_def_raw(self, ctx: PythonParser.Class_def_rawContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#function_def.
    def visitFunction_def(
        self, ctx: PythonParser.Function_defContext
    ) -> ast.FunctionDefinitionStatementAST:
        if ctx.decorators():
            raise FeatureNotImplementedError(ctx)

        return self.visitFunction_def_raw(ctx.function_def_raw())

    # Visit a parse tree produced by PythonParser#function_def_raw.
    def visitFunction_def_raw(
        self, ctx: PythonParser.Function_def_rawContext
    ) -> ast.FunctionDefinitionStatementAST:
        is_async = ctx.ASYNC() is not None
        name = ctx.NAME().getText()
        body = self.visitBlock(ctx.block())

        function_definition_statement_ast = ast.FunctionDefinitionStatementAST(
            is_async=is_async,
            name=name,
            body=body,
        )

        if type_params_ctx := cast(
            Union[PythonParser.Type_paramsContext, None], ctx.type_params()
        ):
            function_definition_statement_ast.type_parameters = self.visitType_params(
                type_params_ctx
            )

        if params_ctx := cast(Union[PythonParser.ParamsContext, None], ctx.params()):
            function_definition_statement_ast.parameters = self.visitParams(params_ctx)

        if expression_ctx := cast(
            Union[PythonParser.ExpressionContext, None], ctx.expression()
        ):
            function_definition_statement_ast.return_type = self.visitExpression(
                expression_ctx
            )

        if func_type_comment_ctx := cast(
            Union[PythonParser.Func_type_commentContext, None], ctx.func_type_comment()
        ):
            raise FeatureNotImplementedError(ctx)

        return function_definition_statement_ast

    # Visit a parse tree produced by PythonParser#params.
    def visitParams(self, ctx: PythonParser.ParamsContext):
        return self.visitParameters(ctx.parameters())

    # Visit a parse tree produced by PythonParser#parameters.
    def visitParameters(
        self, ctx: PythonParser.ParametersContext
    ) -> list[ast.FunctionDefinitionParameterAST]:
        parameters = list[ast.FunctionDefinitionParameterAST]()

        if slash_no_default_ctx := cast(
            Union[PythonParser.Slash_no_defaultContext, None], ctx.slash_no_default()
        ):
            parameters.append(self.visitSlash_no_default(slash_no_default_ctx))

        if slash_with_default_ctx := cast(
            Union[PythonParser.Slash_with_defaultContext, None],
            ctx.slash_with_default(),
        ):
            parameters.append(self.visitSlash_with_default(slash_with_default_ctx))

        for param_no_default_ctx in ctx.param_no_default():
            parameters.append(self.visitParam_no_default(param_no_default_ctx))

        for param_with_default_ctx in ctx.param_with_default():
            parameters.append(self.visitParam_with_default(param_with_default_ctx))

        if star_etc_ctx := cast(
            Union[PythonParser.Star_etcContext, None], ctx.star_etc()
        ):
            parameters.extend(self.visitStar_etc(star_etc_ctx))

        return parameters

    # Visit a parse tree produced by PythonParser#slash_no_default.
    def visitSlash_no_default(self, ctx: PythonParser.Slash_no_defaultContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#slash_with_default.
    def visitSlash_with_default(self, ctx: PythonParser.Slash_with_defaultContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_etc.
    def visitStar_etc(
        self, ctx: PythonParser.Star_etcContext
    ) -> list[ast.FunctionDefinitionParameterAST]:
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#kwds.
    def visitKwds(self, ctx: PythonParser.KwdsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param_no_default.
    def visitParam_no_default(self, ctx: PythonParser.Param_no_defaultContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param_no_default_star_annotation.
    def visitParam_no_default_star_annotation(
        self, ctx: PythonParser.Param_no_default_star_annotationContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param_with_default.
    def visitParam_with_default(self, ctx: PythonParser.Param_with_defaultContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param_maybe_default.
    def visitParam_maybe_default(self, ctx: PythonParser.Param_maybe_defaultContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param.
    def visitParam(self, ctx: PythonParser.ParamContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#param_star_annotation.
    def visitParam_star_annotation(
        self, ctx: PythonParser.Param_star_annotationContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#annotation.
    def visitAnnotation(self, ctx: PythonParser.AnnotationContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_annotation.
    def visitStar_annotation(self, ctx: PythonParser.Star_annotationContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#default_assignment.
    def visitDefault_assignment(self, ctx: PythonParser.Default_assignmentContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#if_stmt.
    def visitIf_stmt(self, ctx: PythonParser.If_stmtContext) -> ast.IfStatementAST:
        condition = self.visitNamed_expression(ctx.named_expression())
        body = self.visitBlock(ctx.block())

        if_statement_ast = ast.IfStatementAST(
            condition=condition,
            body=body,
        )

        if elifs_ctx := cast(
            Union[PythonParser.Elif_stmtContext, None], ctx.elif_stmt()
        ):
            if_statement_ast.else_body = [self.visitElif_stmt(elifs_ctx)]

        if else_block_ctx := cast(
            Union[PythonParser.Else_blockContext, None], ctx.else_block()
        ):
            if_statement_ast.else_body = self.visitElse_block(else_block_ctx)

        return if_statement_ast

    # Visit a parse tree produced by PythonParser#elif_stmt.
    def visitElif_stmt(self, ctx: PythonParser.Elif_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#else_block.
    def visitElse_block(self, ctx: PythonParser.Else_blockContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#while_stmt.
    def visitWhile_stmt(self, ctx: PythonParser.While_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#for_stmt.
    def visitFor_stmt(self, ctx: PythonParser.For_stmtContext):
        is_async = ctx.ASYNC() is not None
        targets = self.visitStar_targets(ctx.star_targets())
        iterators = self.visitStar_expressions(ctx.star_expressions())
        body = self.visitBlock(ctx.block())

        for_statement_ast = ast.ForStatementAST(
            is_async=is_async,
            targets=targets,
            iterators=iterators,
            body=body,
        )

        if else_block_ctx := cast(
            Union[PythonParser.Else_blockContext, None], ctx.else_block()
        ):
            for_statement_ast.else_body = self.visitBlock(else_block_ctx.block())

        return for_statement_ast

    # Visit a parse tree produced by PythonParser#with_stmt.
    def visitWith_stmt(self, ctx: PythonParser.With_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#with_item.
    def visitWith_item(self, ctx: PythonParser.With_itemContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#try_stmt.
    def visitTry_stmt(self, ctx: PythonParser.Try_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#except_block.
    def visitExcept_block(self, ctx: PythonParser.Except_blockContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#except_star_block.
    def visitExcept_star_block(self, ctx: PythonParser.Except_star_blockContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#finally_block.
    def visitFinally_block(self, ctx: PythonParser.Finally_blockContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#match_stmt.
    def visitMatch_stmt(self, ctx: PythonParser.Match_stmtContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#subject_expr.
    def visitSubject_expr(self, ctx: PythonParser.Subject_exprContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#case_block.
    def visitCase_block(self, ctx: PythonParser.Case_blockContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#guard.
    def visitGuard(self, ctx: PythonParser.GuardContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#patterns.
    def visitPatterns(self, ctx: PythonParser.PatternsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#pattern.
    def visitPattern(self, ctx: PythonParser.PatternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#as_pattern.
    def visitAs_pattern(self, ctx: PythonParser.As_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#or_pattern.
    def visitOr_pattern(self, ctx: PythonParser.Or_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#closed_pattern.
    def visitClosed_pattern(self, ctx: PythonParser.Closed_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#literal_pattern.
    def visitLiteral_pattern(self, ctx: PythonParser.Literal_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#literal_expr.
    def visitLiteral_expr(self, ctx: PythonParser.Literal_exprContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#complex_number.
    def visitComplex_number(self, ctx: PythonParser.Complex_numberContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#signed_number.
    def visitSigned_number(self, ctx: PythonParser.Signed_numberContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#signed_real_number.
    def visitSigned_real_number(self, ctx: PythonParser.Signed_real_numberContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#real_number.
    def visitReal_number(self, ctx: PythonParser.Real_numberContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#imaginary_number.
    def visitImaginary_number(self, ctx: PythonParser.Imaginary_numberContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#capture_pattern.
    def visitCapture_pattern(self, ctx: PythonParser.Capture_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#pattern_capture_target.
    def visitPattern_capture_target(
        self, ctx: PythonParser.Pattern_capture_targetContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#wildcard_pattern.
    def visitWildcard_pattern(self, ctx: PythonParser.Wildcard_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#value_pattern.
    def visitValue_pattern(self, ctx: PythonParser.Value_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#attr.
    def visitAttr(self, ctx: PythonParser.AttrContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#name_or_attr.
    def visitName_or_attr(self, ctx: PythonParser.Name_or_attrContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#group_pattern.
    def visitGroup_pattern(self, ctx: PythonParser.Group_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#sequence_pattern.
    def visitSequence_pattern(self, ctx: PythonParser.Sequence_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#open_sequence_pattern.
    def visitOpen_sequence_pattern(
        self, ctx: PythonParser.Open_sequence_patternContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#maybe_sequence_pattern.
    def visitMaybe_sequence_pattern(
        self, ctx: PythonParser.Maybe_sequence_patternContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#maybe_star_pattern.
    def visitMaybe_star_pattern(self, ctx: PythonParser.Maybe_star_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_pattern.
    def visitStar_pattern(self, ctx: PythonParser.Star_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#mapping_pattern.
    def visitMapping_pattern(self, ctx: PythonParser.Mapping_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#items_pattern.
    def visitItems_pattern(self, ctx: PythonParser.Items_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#key_value_pattern.
    def visitKey_value_pattern(self, ctx: PythonParser.Key_value_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#double_star_pattern.
    def visitDouble_star_pattern(self, ctx: PythonParser.Double_star_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#class_pattern.
    def visitClass_pattern(self, ctx: PythonParser.Class_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#positional_patterns.
    def visitPositional_patterns(self, ctx: PythonParser.Positional_patternsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#keyword_patterns.
    def visitKeyword_patterns(self, ctx: PythonParser.Keyword_patternsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#keyword_pattern.
    def visitKeyword_pattern(self, ctx: PythonParser.Keyword_patternContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_alias.
    def visitType_alias(self, ctx: PythonParser.Type_aliasContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_params.
    def visitType_params(self, ctx: PythonParser.Type_paramsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_param_seq.
    def visitType_param_seq(self, ctx: PythonParser.Type_param_seqContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_param.
    def visitType_param(self, ctx: PythonParser.Type_paramContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_param_bound.
    def visitType_param_bound(self, ctx: PythonParser.Type_param_boundContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#expressions.
    def visitExpressions(self, ctx: PythonParser.ExpressionsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#expression.
    def visitExpression(self, ctx: PythonParser.ExpressionContext):
        if lambdef_ctx := cast(Union[PythonParser.LambdefContext, None], ctx.lambdef()):
            return self.visitLambdef(lambdef_ctx)

        if disjunction_ctx := cast(
            Union[PythonParser.DisjunctionContext, None], ctx.disjunction(0)
        ):
            disjunction_ast = self.visitDisjunction(disjunction_ctx)

            if conditional_disjunction_ctx := cast(
                Union[PythonParser.DisjunctionContext, None], ctx.disjunction(1)
            ):
                return ast.ConditionalExpressionAST(
                    condition=self.visitDisjunction(conditional_disjunction_ctx),
                    then_expression=disjunction_ast,
                    else_expression=self.visitExpression(ctx.expression()),
                )

            return disjunction_ast

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#yield_expr.
    def visitYield_expr(self, ctx: PythonParser.Yield_exprContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_expressions.
    def visitStar_expressions(
        self, ctx: PythonParser.Star_expressionsContext
    ) -> list[ast.ExpressionAST]:
        asts = list[ast.ExpressionAST]()

        for star_expression in ctx.star_expression():
            asts.append(self.visitStar_expression(star_expression))

        return asts

    # Visit a parse tree produced by PythonParser#star_expression.
    def visitStar_expression(self, ctx: PythonParser.Star_expressionContext):
        if bitwise_or_ctx := cast(
            Union[PythonParser.Bitwise_orContext, None], ctx.bitwise_or()
        ):
            return self.visitBitwise_or(bitwise_or_ctx)

        if expression_ctx := cast(
            Union[PythonParser.ExpressionContext, None], ctx.expression()
        ):
            return self.visitExpression(expression_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_named_expressions.
    def visitStar_named_expressions(
        self, ctx: PythonParser.Star_named_expressionsContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_named_expression.
    def visitStar_named_expression(
        self, ctx: PythonParser.Star_named_expressionContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#assignment_expression.
    def visitAssignment_expression(
        self, ctx: PythonParser.Assignment_expressionContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#named_expression.
    def visitNamed_expression(self, ctx: PythonParser.Named_expressionContext):
        if assignment_expression_ctx := cast(
            Union[PythonParser.Assignment_expressionContext, None],
            ctx.assignment_expression(),
        ):
            return self.visitAssignment_expression(assignment_expression_ctx)

        if expression_ctx := cast(
            Union[PythonParser.ExpressionContext, None], ctx.expression()
        ):
            return self.visitExpression(expression_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#disjunction.
    def visitDisjunction(
        self, ctx: PythonParser.DisjunctionContext
    ) -> ast.ExpressionAST:
        expression_ast = self.visitConjunction(ctx.conjunction(0))

        if or_conjunction_ctx := cast(
            Union[PythonParser.ConjunctionContext, None], ctx.conjunction(1)
        ):
            or_expression_ast = self.visitConjunction(or_conjunction_ctx)

            return ast.BinaryExpressionAST(
                left=expression_ast,
                operator="or",
                right=or_expression_ast,
            )

        return expression_ast

    # Visit a parse tree produced by PythonParser#conjunction.
    def visitConjunction(
        self, ctx: PythonParser.ConjunctionContext
    ) -> ast.ExpressionAST:
        expression_ast = self.visitInversion(ctx.inversion(0))

        if or_inversion_ctx := cast(
            Union[PythonParser.InversionContext, None], ctx.inversion(1)
        ):
            and_expression_ast = self.visitInversion(or_inversion_ctx)

            return ast.BinaryExpressionAST(
                left=expression_ast,
                operator="and",
                right=and_expression_ast,
            )

        return expression_ast

    # Visit a parse tree produced by PythonParser#inversion.
    def visitInversion(self, ctx: PythonParser.InversionContext) -> ast.ExpressionAST:
        if inversion_ctx := cast(
            Union[PythonParser.InversionContext, None], ctx.inversion()
        ):
            expression_ast = self.visitInversion(inversion_ctx)

            return ast.UnaryExpressionAST(
                expression=expression_ast,
                operator="not",
            )

        if comparison_ctx := cast(
            Union[PythonParser.ComparisonContext, None], ctx.comparison()
        ):
            return self.visitComparison(comparison_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#comparison.
    def visitComparison(self, ctx: PythonParser.ComparisonContext) -> ast.ExpressionAST:
        expression_ast = self.visitBitwise_or(ctx.bitwise_or())

        for compare_op_bitwise_or_pair_ctx in ctx.compare_op_bitwise_or_pair():
            operator, right_expression_ast = self.visitCompare_op_bitwise_or_pair(
                compare_op_bitwise_or_pair_ctx
            )
            expression_ast = ast.BinaryExpressionAST(
                left=expression_ast,
                operator=operator,
                right=right_expression_ast,
            )

        return expression_ast

    # Visit a parse tree produced by PythonParser#compare_op_bitwise_or_pair.
    def visitCompare_op_bitwise_or_pair(
        self, ctx: PythonParser.Compare_op_bitwise_or_pairContext
    ) -> tuple[str, ast.ExpressionAST]:
        if eq_bitwise_or_ctx := cast(
            Union[PythonParser.Eq_bitwise_orContext, None], ctx.eq_bitwise_or()
        ):
            return self.visitEq_bitwise_or(eq_bitwise_or_ctx)

        if noteq_bitwise_or_ctx := cast(
            Union[PythonParser.Noteq_bitwise_orContext, None], ctx.noteq_bitwise_or()
        ):
            return self.visitNoteq_bitwise_or(noteq_bitwise_or_ctx)

        if lte_bitwise_or_ctx := cast(
            Union[PythonParser.Lte_bitwise_orContext, None], ctx.lte_bitwise_or()
        ):
            return self.visitLte_bitwise_or(lte_bitwise_or_ctx)

        if lt_bitwise_or_ctx := cast(
            Union[PythonParser.Lt_bitwise_orContext, None], ctx.lt_bitwise_or()
        ):
            return self.visitLt_bitwise_or(lt_bitwise_or_ctx)

        if gte_bitwise_or_ctx := cast(
            Union[PythonParser.Gte_bitwise_orContext, None], ctx.gte_bitwise_or()
        ):
            return self.visitGte_bitwise_or(gte_bitwise_or_ctx)

        if gt_bitwise_or_ctx := cast(
            Union[PythonParser.Gt_bitwise_orContext, None], ctx.gt_bitwise_or()
        ):
            return self.visitGt_bitwise_or(gt_bitwise_or_ctx)

        if notin_bitwise_or_ctx := cast(
            Union[PythonParser.Notin_bitwise_orContext, None], ctx.notin_bitwise_or()
        ):
            return self.visitNotin_bitwise_or(notin_bitwise_or_ctx)

        if in_bitwise_or_ctx := cast(
            Union[PythonParser.In_bitwise_orContext, None], ctx.in_bitwise_or()
        ):
            return self.visitIn_bitwise_or(in_bitwise_or_ctx)

        if isnot_bitwise_or_ctx := cast(
            Union[PythonParser.Isnot_bitwise_orContext, None], ctx.isnot_bitwise_or()
        ):
            return self.visitIsnot_bitwise_or(isnot_bitwise_or_ctx)

        if is_bitwise_or_ctx := cast(
            Union[PythonParser.Is_bitwise_orContext, None], ctx.is_bitwise_or()
        ):
            return self.visitIs_bitwise_or(is_bitwise_or_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#eq_bitwise_or.
    def visitEq_bitwise_or(self, ctx: PythonParser.Eq_bitwise_orContext):
        return "==", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#noteq_bitwise_or.
    def visitNoteq_bitwise_or(self, ctx: PythonParser.Noteq_bitwise_orContext):
        return "!=", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#lte_bitwise_or.
    def visitLte_bitwise_or(self, ctx: PythonParser.Lte_bitwise_orContext):
        return "<=", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#lt_bitwise_or.
    def visitLt_bitwise_or(self, ctx: PythonParser.Lt_bitwise_orContext):
        return "<", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#gte_bitwise_or.
    def visitGte_bitwise_or(self, ctx: PythonParser.Gte_bitwise_orContext):
        return ">=", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#gt_bitwise_or.
    def visitGt_bitwise_or(self, ctx: PythonParser.Gt_bitwise_orContext):
        return ">", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#notin_bitwise_or.
    def visitNotin_bitwise_or(self, ctx: PythonParser.Notin_bitwise_orContext):
        return "not in", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#in_bitwise_or.
    def visitIn_bitwise_or(self, ctx: PythonParser.In_bitwise_orContext):
        return "in", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#isnot_bitwise_or.
    def visitIsnot_bitwise_or(self, ctx: PythonParser.Isnot_bitwise_orContext):
        return "is not", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#is_bitwise_or.
    def visitIs_bitwise_or(self, ctx: PythonParser.Is_bitwise_orContext):
        return "is", self.visitBitwise_or(ctx.bitwise_or())

    # Visit a parse tree produced by PythonParser#bitwise_or.
    def visitBitwise_or(self, ctx: PythonParser.Bitwise_orContext) -> ast.ExpressionAST:
        if bitwise_or_ctx := cast(
            Union[PythonParser.Bitwise_orContext, None], ctx.bitwise_or()
        ):
            left_expression_ast = self.visitBitwise_or(bitwise_or_ctx)
            right_expression_ast = self.visitBitwise_xor(
                cast(PythonParser.Bitwise_xorContext, ctx.bitwise_xor())
            )

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator="|",
                right=right_expression_ast,
            )

        if bitwise_xor_ctx := cast(
            Union[PythonParser.Bitwise_xorContext, None], ctx.bitwise_xor()
        ):
            return self.visitBitwise_xor(bitwise_xor_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#bitwise_xor.
    def visitBitwise_xor(
        self, ctx: PythonParser.Bitwise_xorContext
    ) -> ast.ExpressionAST:
        if bitwise_xor_ctx := cast(
            Union[PythonParser.Bitwise_xorContext, None], ctx.bitwise_xor()
        ):
            left_expression_ast = self.visitBitwise_xor(bitwise_xor_ctx)
            right_expression_ast = self.visitBitwise_and(
                cast(PythonParser.Bitwise_andContext, ctx.bitwise_and())
            )

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator="^",
                right=right_expression_ast,
            )

        if bitwise_and_ctx := cast(
            Union[PythonParser.Bitwise_andContext, None], ctx.bitwise_and()
        ):
            return self.visitBitwise_and(bitwise_and_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#bitwise_and.
    def visitBitwise_and(
        self, ctx: PythonParser.Bitwise_andContext
    ) -> ast.ExpressionAST:
        if bitwise_and_ctx := cast(
            Union[PythonParser.Bitwise_andContext, None], ctx.bitwise_and()
        ):
            left_expression_ast = self.visitBitwise_and(bitwise_and_ctx)
            right_expression_ast = self.visitShift_expr(
                cast(PythonParser.Shift_exprContext, ctx.shift_expr())
            )

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator="&",
                right=right_expression_ast,
            )

        if shift_expr_ctx := cast(
            Union[PythonParser.Shift_exprContext, None], ctx.shift_expr()
        ):
            return self.visitShift_expr(shift_expr_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#shift_expr.
    def visitShift_expr(self, ctx: PythonParser.Shift_exprContext) -> ast.ExpressionAST:
        if shift_expr_ctx := cast(
            Union[PythonParser.Shift_exprContext, None], ctx.shift_expr()
        ):
            left_expression_ast = self.visitShift_expr(shift_expr_ctx)
            right_expression_ast = self.visitSum(
                cast(PythonParser.SumContext, ctx.sum_())
            )

            operator: str | None = None
            if ctx.LEFTSHIFT():
                operator = "<<"
            elif ctx.RIGHTSHIFT():
                operator = ">>"

            if operator is None:
                raise FeatureNotImplementedError(ctx)

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator=operator,
                right=right_expression_ast,
            )

        if sum_ctx := cast(Union[PythonParser.SumContext, None], ctx.sum_()):
            return self.visitSum(sum_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#sum.
    def visitSum(self, ctx: PythonParser.SumContext) -> ast.ExpressionAST:
        if sum_ctx := cast(Union[PythonParser.SumContext, None], ctx.sum_()):
            left_expression_ast = self.visitSum(sum_ctx)
            right_expression_ast = self.visitTerm(
                cast(PythonParser.TermContext, ctx.term())
            )

            operator: str | None = None
            if ctx.PLUS():
                operator = "+"
            elif ctx.MINUS():
                operator = "-"

            if operator is None:
                raise FeatureNotImplementedError(ctx)

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator=operator,
                right=right_expression_ast,
            )

        if term_ctx := cast(Union[PythonParser.TermContext, None], ctx.term()):
            return self.visitTerm(term_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#term.
    def visitTerm(self, ctx: PythonParser.TermContext) -> ast.ExpressionAST:
        if term_ctx := cast(Union[PythonParser.TermContext, None], ctx.term()):
            left_expression_ast = self.visitTerm(term_ctx)
            right_expression_ast = self.visitFactor(
                cast(PythonParser.FactorContext, ctx.factor())
            )

            operator: str | None = None
            if ctx.STAR():
                operator = "*"
            elif ctx.SLASH():
                operator = "/"
            elif ctx.DOUBLESLASH():
                operator = "//"
            elif ctx.PERCENT():
                operator = "%"
            elif ctx.AT():
                operator = "@"

            if operator is None:
                raise FeatureNotImplementedError(ctx)

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator=operator,
                right=right_expression_ast,
            )

        if factor_ctx := cast(Union[PythonParser.FactorContext, None], ctx.factor()):
            return self.visitFactor(factor_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#factor.
    def visitFactor(self, ctx: PythonParser.FactorContext) -> ast.ExpressionAST:
        if factor_ctx := cast(Union[PythonParser.FactorContext, None], ctx.factor()):
            expression_ast = self.visitFactor(factor_ctx)

            operator: str | None = None
            if ctx.PLUS():
                operator = "+"
            elif ctx.MINUS():
                operator = "-"
            elif ctx.TILDE():
                operator = "~"

            if operator is None:
                raise FeatureNotImplementedError(ctx)

            return ast.UnaryExpressionAST(
                expression=expression_ast,
                operator=operator,
            )

        if power_ctx := cast(Union[PythonParser.PowerContext, None], ctx.power()):
            return self.visitPower(power_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#power.
    def visitPower(self, ctx: PythonParser.PowerContext) -> ast.ExpressionAST:
        left_expression_ast = self.visitAwait_primary(ctx.await_primary())

        if factor_ctx := cast(Union[PythonParser.FactorContext, None], ctx.factor()):
            right_expression_ast = self.visitFactor(factor_ctx)

            return ast.BinaryExpressionAST(
                left=left_expression_ast,
                operator="**",
                right=right_expression_ast,
            )

        return left_expression_ast

    # Visit a parse tree produced by PythonParser#await_primary.
    def visitAwait_primary(
        self, ctx: PythonParser.Await_primaryContext
    ) -> ast.ExpressionAST:
        expression_ast = self.visitPrimary(ctx.primary())

        if ctx.AWAIT():
            return ast.AwaitExpressionAST(expression=expression_ast)

        return expression_ast

    # Visit a parse tree produced by PythonParser#primary.
    def visitPrimary(self, ctx: PythonParser.PrimaryContext):
        if primary_ctx := cast(Union[PythonParser.PrimaryContext, None], ctx.primary()):
            expression_ast = self.visitPrimary(primary_ctx)

            if name := ctx.NAME():
                return ast.NameExpressionAST(
                    expression=expression_ast,
                    name=name.getText(),
                )

            if genexp_ctx := cast(
                Union[PythonParser.GenexpContext, None], ctx.genexp()
            ):
                raise FeatureNotImplementedError(ctx)

            if ctx.LPAR() and ctx.RPAR():
                call_expression_ast = ast.CallExpressionAST(
                    expression=expression_ast,
                )

                if arguments_ctx := cast(
                    Union[PythonParser.ArgumentsContext, None], ctx.arguments()
                ):
                    call_expression_ast.arguments = self.visitArguments(arguments_ctx)

                return call_expression_ast

            if ctx.LSQB() and ctx.RSQB():
                return ast.SubscriptExpressionAST(
                    expression=expression_ast,
                    slices=self.visitSlices(ctx.slices()),
                )

            raise FeatureNotImplementedError(ctx)

        if atom_ctx := cast(Union[PythonParser.AtomContext, None], ctx.atom()):
            return self.visitAtom(atom_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#slices.
    def visitSlices(self, ctx: PythonParser.SlicesContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#slice.
    def visitSlice(self, ctx: PythonParser.SliceContext):
        raise FeatureNotImplementedError(ctx)

    # NAME
    # | 'True'
    # | 'False'
    # | 'None'
    # | strings
    # | NUMBER
    # | (tuple | group | genexp)
    # | (list | listcomp)
    # | (dict | set | dictcomp | setcomp)
    # | '...';
    # Visit a parse tree produced by PythonParser#atom.
    def visitAtom(self, ctx: PythonParser.AtomContext) -> ast.ExpressionAST:
        if name := ctx.NAME():
            return ast.NameLiteralExpressionAST(value=name.getText())

        if ctx.TRUE():
            return ast.BooleanLiteralExpressionAST(value=True)

        if ctx.FALSE():
            return ast.BooleanLiteralExpressionAST(value=False)

        if ctx.NONE():
            return ast.NoneLiteralExpressionAST()

        if strings_ctx := cast(Union[PythonParser.StringsContext, None], ctx.strings()):
            return self.visitStrings(strings_ctx)

        if number := ctx.NUMBER():
            raise FeatureNotImplementedError(ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#group.
    def visitGroup(self, ctx: PythonParser.GroupContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambdef.
    def visitLambdef(self, ctx: PythonParser.LambdefContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_params.
    def visitLambda_params(self, ctx: PythonParser.Lambda_paramsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_parameters.
    def visitLambda_parameters(self, ctx: PythonParser.Lambda_parametersContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_slash_no_default.
    def visitLambda_slash_no_default(
        self, ctx: PythonParser.Lambda_slash_no_defaultContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_slash_with_default.
    def visitLambda_slash_with_default(
        self, ctx: PythonParser.Lambda_slash_with_defaultContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_star_etc.
    def visitLambda_star_etc(self, ctx: PythonParser.Lambda_star_etcContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_kwds.
    def visitLambda_kwds(self, ctx: PythonParser.Lambda_kwdsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_no_default.
    def visitLambda_param_no_default(
        self, ctx: PythonParser.Lambda_param_no_defaultContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_with_default.
    def visitLambda_param_with_default(
        self, ctx: PythonParser.Lambda_param_with_defaultContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param_maybe_default.
    def visitLambda_param_maybe_default(
        self, ctx: PythonParser.Lambda_param_maybe_defaultContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#lambda_param.
    def visitLambda_param(self, ctx: PythonParser.Lambda_paramContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_middle.
    def visitFstring_middle(self, ctx: PythonParser.Fstring_middleContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_replacement_field.
    def visitFstring_replacement_field(
        self, ctx: PythonParser.Fstring_replacement_fieldContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_conversion.
    def visitFstring_conversion(self, ctx: PythonParser.Fstring_conversionContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_full_format_spec.
    def visitFstring_full_format_spec(
        self, ctx: PythonParser.Fstring_full_format_specContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring_format_spec.
    def visitFstring_format_spec(self, ctx: PythonParser.Fstring_format_specContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#fstring.
    def visitFstring(self, ctx: PythonParser.FstringContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#string.
    def visitString(self, ctx: PythonParser.StringContext):
        return ast.StringLiteralExpressionAST(value=ctx.STRING().getText()[1:-1])

    # Visit a parse tree produced by PythonParser#strings.
    def visitStrings(self, ctx: PythonParser.StringsContext) -> ast.ExpressionAST:
        combinatory_string_ast = ast.CombinatoryStringLiteralExpressionAST(values=[])

        for child_ctx in ctx.getChildren():
            if isinstance(child_ctx, PythonParser.StringContext):
                string_ast = self.visitString(child_ctx)
                combinatory_string_ast.values.append(string_ast)
                continue

            if isinstance(child_ctx, PythonParser.FstringContext):
                fstring_ast = self.visitFstring(child_ctx)
                combinatory_string_ast.values.append(fstring_ast)
                continue

            raise FeatureNotImplementedError(ctx)

        return combinatory_string_ast

    # Visit a parse tree produced by PythonParser#list.
    def visitList(self, ctx: PythonParser.ListContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#tuple.
    def visitTuple(self, ctx: PythonParser.TupleContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#set.
    def visitSet(self, ctx: PythonParser.SetContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#dict.
    def visitDict(self, ctx: PythonParser.DictContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#double_starred_kvpairs.
    def visitDouble_starred_kvpairs(
        self, ctx: PythonParser.Double_starred_kvpairsContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#double_starred_kvpair.
    def visitDouble_starred_kvpair(
        self, ctx: PythonParser.Double_starred_kvpairContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#kvpair.
    def visitKvpair(self, ctx: PythonParser.KvpairContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#for_if_clauses.
    def visitFor_if_clauses(self, ctx: PythonParser.For_if_clausesContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#for_if_clause.
    def visitFor_if_clause(self, ctx: PythonParser.For_if_clauseContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#listcomp.
    def visitListcomp(self, ctx: PythonParser.ListcompContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#setcomp.
    def visitSetcomp(self, ctx: PythonParser.SetcompContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#genexp.
    def visitGenexp(self, ctx: PythonParser.GenexpContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#dictcomp.
    def visitDictcomp(self, ctx: PythonParser.DictcompContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#arguments.
    def visitArguments(
        self, ctx: PythonParser.ArgumentsContext
    ) -> list[ast.CallExpressionArgumentAST]:
        return self.visitArgs(ctx.args())

    # Visit a parse tree produced by PythonParser#args.
    def visitArgs(
        self, ctx: PythonParser.ArgsContext
    ) -> list[ast.CallExpressionArgumentAST]:
        asts = list[ast.CallExpressionArgumentAST]()

        for arg in ctx.arg() or []:
            asts.append(self.visitArg(arg))

        for kwargs in ctx.kwargs() or []:
            asts.extend(self.visitKwargs(kwargs))

        return asts

    # Visit a parse tree produced by PythonParser#arg.
    def visitArg(self, ctx: PythonParser.ArgContext) -> ast.CallExpressionArgumentAST:
        if starred_expression_ctx := cast(
            Union[PythonParser.Starred_expressionContext, None],
            ctx.starred_expression(),
        ):
            return self.visitStarred_expression(starred_expression_ctx)

        if assignement_expression_ctx := cast(
            Union[PythonParser.Assignment_expressionContext, None],
            ctx.assignment_expression(),
        ):
            return self.visitAssignment_expression(assignement_expression_ctx)

        if expression_ctx := cast(
            Union[PythonParser.ExpressionContext, None], ctx.expression()
        ):
            return ast.CallExpressionArgumentAST(
                expression=self.visitExpression(expression_ctx)
            )

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#kwargs.
    def visitKwargs(self, ctx: PythonParser.KwargsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#starred_expression.
    def visitStarred_expression(self, ctx: PythonParser.Starred_expressionContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#kwarg_or_starred.
    def visitKwarg_or_starred(self, ctx: PythonParser.Kwarg_or_starredContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#kwarg_or_double_starred.
    def visitKwarg_or_double_starred(
        self, ctx: PythonParser.Kwarg_or_double_starredContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_targets.
    def visitStar_targets(
        self, ctx: PythonParser.Star_targetsContext
    ) -> list[ast.TargetAST]:
        target_asts = list[ast.TargetAST]()

        for start_target_ctx in ctx.star_target():
            target_asts.append(self.visitStar_target(start_target_ctx))

        return target_asts

    # Visit a parse tree produced by PythonParser#star_targets_list_seq.
    def visitStar_targets_list_seq(
        self, ctx: PythonParser.Star_targets_list_seqContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_targets_tuple_seq.
    def visitStar_targets_tuple_seq(
        self, ctx: PythonParser.Star_targets_tuple_seqContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_target.
    def visitStar_target(self, ctx: PythonParser.Star_targetContext) -> ast.TargetAST:
        if star_target_ctx := cast(
            Union[PythonParser.Star_targetContext, None], ctx.star_target()
        ):
            target_ast = self.visitStar_target(star_target_ctx)
            return ast.UnpackTargetAST(target=target_ast)

        if target_with_star_atom_ctx := cast(
            Union[PythonParser.Target_with_star_atomContext, None],
            ctx.target_with_star_atom(),
        ):
            return self.visitTarget_with_star_atom(target_with_star_atom_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#target_with_star_atom.
    def visitTarget_with_star_atom(
        self, ctx: PythonParser.Target_with_star_atomContext
    ):
        if star_atom_ctx := cast(
            Union[PythonParser.Star_atomContext, None], ctx.star_atom()
        ):
            return self.visitStar_atom(star_atom_ctx)

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#star_atom.
    def visitStar_atom(self, ctx: PythonParser.Star_atomContext):
        if name := ctx.NAME():
            return ast.NameTargetAST(name=name.getText())

        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#single_target.
    def visitSingle_target(self, ctx: PythonParser.Single_targetContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#single_subscript_attribute_target.
    def visitSingle_subscript_attribute_target(
        self, ctx: PythonParser.Single_subscript_attribute_targetContext
    ):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#t_primary.
    def visitT_primary(self, ctx: PythonParser.T_primaryContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#del_targets.
    def visitDel_targets(self, ctx: PythonParser.Del_targetsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#del_target.
    def visitDel_target(self, ctx: PythonParser.Del_targetContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#del_t_atom.
    def visitDel_t_atom(self, ctx: PythonParser.Del_t_atomContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#type_expressions.
    def visitType_expressions(self, ctx: PythonParser.Type_expressionsContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#func_type_comment.
    def visitFunc_type_comment(self, ctx: PythonParser.Func_type_commentContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#soft_kw_type.
    def visitSoft_kw_type(self, ctx: PythonParser.Soft_kw_typeContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#soft_kw_match.
    def visitSoft_kw_match(self, ctx: PythonParser.Soft_kw_matchContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#soft_kw_case.
    def visitSoft_kw_case(self, ctx: PythonParser.Soft_kw_caseContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#soft_kw_wildcard.
    def visitSoft_kw_wildcard(self, ctx: PythonParser.Soft_kw_wildcardContext):
        raise FeatureNotImplementedError(ctx)

    # Visit a parse tree produced by PythonParser#soft_kw__not__wildcard.
    def visitSoft_kw__not__wildcard(
        self, ctx: PythonParser.Soft_kw__not__wildcardContext
    ):
        raise FeatureNotImplementedError(ctx)
