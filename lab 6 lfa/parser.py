from dataclasses import dataclass
from typing import List, Optional
from token_types import TokenType, string_to_token_type
from ast_nodes import *


@dataclass
class Token:
    """Token data structure from lexer."""

    token_type: str
    value: str
    line: int
    column: int


class ParseError(Exception):
    pass


class Parser:
    """Recursive descent parser that builds an AST from tokens."""

    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.current = 0

    def parse(self) -> Program:
        """Parse a full program."""
        statements = []
        while not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return Program(statements)

    def _parse_statement(self) -> Optional[Statement]:
        """Parse a single statement."""
        if self._check("LET"):
            return self._parse_variable_declaration()
        elif self._check("IF"):
            return self._parse_if_statement()
        elif self._check("RETURN"):
            return self._parse_return_statement()
        elif self._check("PRINT"):
            return self._parse_print_statement()
        elif self._check("FUNCTION"):
            return self._parse_function_def()
        else:
            # Try to parse as expression statement
            expr = self._parse_expression()
            self._consume_semicolon_if_present()
            if expr:
                return ExpressionStatement(expr)
            return None

    def _parse_variable_declaration(self) -> VariableDeclaration:
        """Parse: let IDENTIFIER = EXPRESSION ;"""
        self._consume("LET", "Expected 'let'")
        name_token = self._consume_type("IDENTIFIER")
        self._consume("ASSIGN", "Expected '='")
        value = self._parse_expression()
        self._consume_semicolon_if_present()
        return VariableDeclaration(name_token.value, value)

    def _parse_if_statement(self) -> IfStatement:
        """Parse: if (EXPR) { STMTS } else { STMTS }"""
        self._consume("IF", "Expected 'if'")
        self._consume("LPAREN", "Expected '('")
        condition = self._parse_expression()
        self._consume("RPAREN", "Expected ')'")

        self._consume("LBRACE", "Expected '{'")
        then_body = self._parse_block()
        self._consume("RBRACE", "Expected '}'")

        else_body = None
        if self._check("ELSE"):
            self._advance()
            self._consume("LBRACE", "Expected '{'")
            else_body = self._parse_block()
            self._consume("RBRACE", "Expected '}'")

        return IfStatement(condition, then_body, else_body)

    def _parse_return_statement(self) -> ReturnStatement:
        """Parse: return EXPR? ;"""
        self._consume("RETURN", "Expected 'return'")
        value = None
        if not self._check("SEMICOLON"):
            value = self._parse_expression()
        self._consume_semicolon_if_present()
        return ReturnStatement(value)

    def _parse_print_statement(self) -> PrintStatement:
        """Parse: print ( EXPR, ... ) ;"""
        self._consume("PRINT", "Expected 'print'")
        self._consume("LPAREN", "Expected '('")
        arguments = []
        if not self._check("RPAREN"):
            arguments.append(self._parse_expression())
            while self._check("COMMA"):
                self._advance()
                arguments.append(self._parse_expression())
        self._consume("RPAREN", "Expected ')'")
        self._consume_semicolon_if_present()
        return PrintStatement(arguments)

    def _parse_function_def(self) -> FunctionDef:
        """Parse: fn NAME ( PARAMS ) { BODY }"""
        self._consume("FUNCTION", "Expected 'fn'")
        name_token = self._consume_type("IDENTIFIER")
        self._consume("LPAREN", "Expected '('")

        parameters = []
        if not self._check("RPAREN"):
            parameters.append(self._consume_type("IDENTIFIER").value)
            while self._check("COMMA"):
                self._advance()
                parameters.append(self._consume_type("IDENTIFIER").value)
        self._consume("RPAREN", "Expected ')'")

        self._consume("LBRACE", "Expected '{'")
        body = self._parse_block()
        self._consume("RBRACE", "Expected '}'")

        return FunctionDef(name_token.value, parameters, body)

    def _parse_block(self) -> List[Statement]:
        """Parse a block of statements inside { }."""
        statements = []
        while not self._check("RBRACE") and not self._is_at_end():
            stmt = self._parse_statement()
            if stmt:
                statements.append(stmt)
        return statements

    def _parse_expression(self) -> Expression:
        """Parse an expression (entry point for expression parsing)."""
        return self._parse_assignment()

    def _parse_assignment(self) -> Expression:
        """Parse assignment or lower precedence expression."""
        expr = self._parse_logical_or()

        if self._check("ASSIGN"):
            if isinstance(expr, Identifier):
                self._advance()
                value = self._parse_assignment()
                return Assignment(expr.name, value)
            else:
                raise ParseError("Invalid assignment target")

        return expr

    def _parse_logical_or(self) -> Expression:
        """Parse logical OR (|) - not implemented yet for simplicity."""
        return self._parse_equality()

    def _parse_equality(self) -> Expression:
        """Parse == or != operators."""
        expr = self._parse_comparison()

        while self._check_any("EQ", "NOT_EQ"):
            op = self._peek().value
            self._advance()
            right = self._parse_comparison()
            expr = BinaryOp(expr, op, right)

        return expr

    def _parse_comparison(self) -> Expression:
        """Parse < > <= >= operators."""
        expr = self._parse_additive()

        while self._check_any("LT", "GT"):
            op = self._peek().value
            self._advance()
            right = self._parse_additive()
            expr = BinaryOp(expr, op, right)

        return expr

    def _parse_additive(self) -> Expression:
        """Parse + - operators."""
        expr = self._parse_multiplicative()

        while self._check_any("PLUS", "MINUS"):
            op = self._peek().value
            self._advance()
            right = self._parse_multiplicative()
            expr = BinaryOp(expr, op, right)

        return expr

    def _parse_multiplicative(self) -> Expression:
        """Parse * / operators."""
        expr = self._parse_unary()

        while self._check_any("MULTIPLY", "DIVIDE"):
            op = self._peek().value
            self._advance()
            right = self._parse_unary()
            expr = BinaryOp(expr, op, right)

        return expr

    def _parse_unary(self) -> Expression:
        """Parse unary operators (! -)."""
        if self._check_any("BANG", "MINUS"):
            op = self._peek().value
            self._advance()
            expr = self._parse_unary()
            return UnaryOp(op, expr)

        return self._parse_postfix()

    def _parse_postfix(self) -> Expression:
        """Parse postfix operations (function calls, array access)."""
        expr = self._parse_primary()

        while True:
            if self._check("LPAREN"):
                self._advance()
                arguments = []
                if not self._check("RPAREN"):
                    arguments.append(self._parse_expression())
                    while self._check("COMMA"):
                        self._advance()
                        arguments.append(self._parse_expression())
                self._consume("RPAREN", "Expected ')'")
                expr = FunctionCall(expr, arguments)
            elif self._check("LBRACKET"):
                self._advance()
                index = self._parse_expression()
                self._consume("RBRACKET", "Expected ']'")
                expr = IndexAccess(expr, index)
            else:
                break

        return expr

    def _parse_primary(self) -> Expression:
        """Parse primary expressions (literals, identifiers, grouped expressions)."""
        if self._check("INT"):
            token = self._advance()
            return IntLiteral(int(token.value))

        if self._check("FLOAT"):
            token = self._advance()
            return FloatLiteral(float(token.value))

        if self._check("STRING"):
            token = self._advance()
            return StringLiteral(token.value)

        if self._check("TRUE"):
            self._advance()
            return BooleanLiteral(True)

        if self._check("FALSE"):
            self._advance()
            return BooleanLiteral(False)

        if self._check("IDENTIFIER"):
            token = self._advance()
            return Identifier(token.value)

        if self._check("SIN"):
            self._advance()
            self._consume("LPAREN", "Expected '('")
            arg = self._parse_expression()
            self._consume("RPAREN", "Expected ')'")
            return FunctionCall(Identifier("sin"), [arg])

        if self._check("COS"):
            self._advance()
            self._consume("LPAREN", "Expected '('")
            arg = self._parse_expression()
            self._consume("RPAREN", "Expected ')'")
            return FunctionCall(Identifier("cos"), [arg])

        if self._check("LPAREN"):
            self._advance()
            expr = self._parse_expression()
            self._consume("RPAREN", "Expected ')'")
            return expr

        if self._check("LBRACKET"):
            return self._parse_array_literal()

        if self._check("LBRACE"):
            return self._parse_map_literal()

        raise ParseError(f"Unexpected token: {self._peek()}")

    def _parse_array_literal(self) -> ArrayLiteral:
        """Parse [ EXPR, EXPR, ... ]"""
        self._consume("LBRACKET", "Expected '['")
        elements = []
        if not self._check("RBRACKET"):
            elements.append(self._parse_expression())
            while self._check("COMMA"):
                self._advance()
                if self._check("RBRACKET"):
                    break
                elements.append(self._parse_expression())
        self._consume("RBRACKET", "Expected ']'")
        return ArrayLiteral(elements)

    def _parse_map_literal(self) -> MapLiteral:
        """Parse { "key": value, "key": value, ... }"""
        self._consume("LBRACE", "Expected '{'")
        pairs = []
        if not self._check("RBRACE"):
            key = self._parse_expression()
            self._consume("COLON", "Expected ':'")
            value = self._parse_expression()
            pairs.append((key, value))
            while self._check("COMMA"):
                self._advance()
                if self._check("RBRACE"):
                    break
                key = self._parse_expression()
                self._consume("COLON", "Expected ':'")
                value = self._parse_expression()
                pairs.append((key, value))
        self._consume("RBRACE", "Expected '}'")
        return MapLiteral(pairs)

    # Helper methods
    def _check(self, token_type: str) -> bool:
        """Check if current token matches type."""
        if self._is_at_end():
            return False
        return self._peek().token_type == token_type

    def _check_any(self, *token_types: str) -> bool:
        """Check if current token matches any of the types."""
        return any(self._check(t) for t in token_types)

    def _peek(self) -> Token:
        """Get current token without advancing."""
        return self.tokens[self.current]

    def _advance(self) -> Token:
        """Get current token and move to next."""
        if not self._is_at_end():
            self.current += 1
        return self.tokens[self.current - 1]

    def _consume(self, token_type: str, message: str) -> Token:
        """Consume a specific token type or raise error."""
        if self._check(token_type):
            return self._advance()
        raise ParseError(f"{message} at {self._peek()}")

    def _consume_type(self, token_type: str) -> Token:
        """Consume a specific token type."""
        return self._consume(token_type, f"Expected {token_type}")

    def _consume_semicolon_if_present(self) -> None:
        """Optionally consume a semicolon."""
        if self._check("SEMICOLON"):
            self._advance()

    def _is_at_end(self) -> bool:
        """Check if we're at EOF."""
        return self._peek().token_type == "EOF"
