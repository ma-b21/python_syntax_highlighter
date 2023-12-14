// Generated from Python.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link PythonParser}.
 */
public interface PythonListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link PythonParser#pythonFile}.
	 * @param ctx the parse tree
	 */
	void enterPythonFile(PythonParser.PythonFileContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#pythonFile}.
	 * @param ctx the parse tree
	 */
	void exitPythonFile(PythonParser.PythonFileContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#importStatement}.
	 * @param ctx the parse tree
	 */
	void enterImportStatement(PythonParser.ImportStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#importStatement}.
	 * @param ctx the parse tree
	 */
	void exitImportStatement(PythonParser.ImportStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#classDefinition}.
	 * @param ctx the parse tree
	 */
	void enterClassDefinition(PythonParser.ClassDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#classDefinition}.
	 * @param ctx the parse tree
	 */
	void exitClassDefinition(PythonParser.ClassDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#functionDefinition}.
	 * @param ctx the parse tree
	 */
	void enterFunctionDefinition(PythonParser.FunctionDefinitionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#functionDefinition}.
	 * @param ctx the parse tree
	 */
	void exitFunctionDefinition(PythonParser.FunctionDefinitionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#otherStatements}.
	 * @param ctx the parse tree
	 */
	void enterOtherStatements(PythonParser.OtherStatementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#otherStatements}.
	 * @param ctx the parse tree
	 */
	void exitOtherStatements(PythonParser.OtherStatementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#simpleStatement}.
	 * @param ctx the parse tree
	 */
	void enterSimpleStatement(PythonParser.SimpleStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#simpleStatement}.
	 * @param ctx the parse tree
	 */
	void exitSimpleStatement(PythonParser.SimpleStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(PythonParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(PythonParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(PythonParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(PythonParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#logicalExpression}.
	 * @param ctx the parse tree
	 */
	void enterLogicalExpression(PythonParser.LogicalExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#logicalExpression}.
	 * @param ctx the parse tree
	 */
	void exitLogicalExpression(PythonParser.LogicalExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#logicalTerm}.
	 * @param ctx the parse tree
	 */
	void enterLogicalTerm(PythonParser.LogicalTermContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#logicalTerm}.
	 * @param ctx the parse tree
	 */
	void exitLogicalTerm(PythonParser.LogicalTermContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(PythonParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(PythonParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void enterArithmeticExpression(PythonParser.ArithmeticExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#arithmeticExpression}.
	 * @param ctx the parse tree
	 */
	void exitArithmeticExpression(PythonParser.ArithmeticExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#term}.
	 * @param ctx the parse tree
	 */
	void enterTerm(PythonParser.TermContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#term}.
	 * @param ctx the parse tree
	 */
	void exitTerm(PythonParser.TermContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#factor}.
	 * @param ctx the parse tree
	 */
	void enterFactor(PythonParser.FactorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#factor}.
	 * @param ctx the parse tree
	 */
	void exitFactor(PythonParser.FactorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(PythonParser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(PythonParser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#compOperator}.
	 * @param ctx the parse tree
	 */
	void enterCompOperator(PythonParser.CompOperatorContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#compOperator}.
	 * @param ctx the parse tree
	 */
	void exitCompOperator(PythonParser.CompOperatorContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#constant}.
	 * @param ctx the parse tree
	 */
	void enterConstant(PythonParser.ConstantContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#constant}.
	 * @param ctx the parse tree
	 */
	void exitConstant(PythonParser.ConstantContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void enterIfStatement(PythonParser.IfStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void exitIfStatement(PythonParser.IfStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void enterWhileStatement(PythonParser.WhileStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void exitWhileStatement(PythonParser.WhileStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#importFrom}.
	 * @param ctx the parse tree
	 */
	void enterImportFrom(PythonParser.ImportFromContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#importFrom}.
	 * @param ctx the parse tree
	 */
	void exitImportFrom(PythonParser.ImportFromContext ctx);
	/**
	 * Enter a parse tree produced by {@link PythonParser#importSimple}.
	 * @param ctx the parse tree
	 */
	void enterImportSimple(PythonParser.ImportSimpleContext ctx);
	/**
	 * Exit a parse tree produced by {@link PythonParser#importSimple}.
	 * @param ctx the parse tree
	 */
	void exitImportSimple(PythonParser.ImportSimpleContext ctx);
}