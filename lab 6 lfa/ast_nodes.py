from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass
class ASTNode:
    """Base class for all AST nodes."""

    pass


@dataclass
class Expression(ASTNode):
    """Base class for all expressions."""

    pass


@dataclass
class Statement(ASTNode):
    """Base class for all statements."""

    pass


# Literals
@dataclass
class IntLiteral(Expression):
    value: int


@dataclass
class FloatLiteral(Expression):
    value: float


@dataclass
class StringLiteral(Expression):
    value: str


@dataclass
class BooleanLiteral(Expression):
    value: bool


@dataclass
class Identifier(Expression):
    name: str


# Collections
@dataclass
class ArrayLiteral(Expression):
    elements: List[Expression]


@dataclass
class MapLiteral(Expression):
    pairs: List[tuple]  # List of (key_expr, value_expr) tuples


# Binary operations
@dataclass
class BinaryOp(Expression):
    left: Expression
    operator: str
    right: Expression


# Unary operations
@dataclass
class UnaryOp(Expression):
    operator: str
    operand: Expression


# Function call
@dataclass
class FunctionCall(Expression):
    function: Expression
    arguments: List[Expression]


# Array/Map access
@dataclass
class IndexAccess(Expression):
    object: Expression
    index: Expression


# Statements
@dataclass
class VariableDeclaration(Statement):
    name: str
    value: Expression


@dataclass
class Assignment(Statement):
    target: str
    value: Expression


@dataclass
class IfStatement(Statement):
    condition: Expression
    then_body: List[Statement]
    else_body: Optional[List[Statement]] = None


@dataclass
class ReturnStatement(Statement):
    value: Optional[Expression] = None


@dataclass
class PrintStatement(Statement):
    arguments: List[Expression]


@dataclass
class ExpressionStatement(Statement):
    expression: Expression


# Function definition
@dataclass
class FunctionDef(Statement):
    name: str
    parameters: List[str]
    body: List[Statement]


# Program (root node)
@dataclass
class Program(ASTNode):
    statements: List[Statement]
