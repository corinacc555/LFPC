def print_ast(node, indent: int = 0) -> None:
    """Pretty-print an AST node."""
    prefix = "  " * indent
    node_type = type(node).__name__

    if node_type == "Program":
        print(f"{prefix}Program")
        for stmt in node.statements:
            print_ast(stmt, indent + 1)

    elif node_type == "VariableDeclaration":
        print(f"{prefix}VariableDeclaration: {node.name} =")
        print_ast(node.value, indent + 1)

    elif node_type == "Assignment":
        print(f"{prefix}Assignment: {node.target} =")
        print_ast(node.value, indent + 1)

    elif node_type == "IfStatement":
        print(f"{prefix}IfStatement (condition)")
        print_ast(node.condition, indent + 1)
        print(f"{prefix}  then:")
        for stmt in node.then_body:
            print_ast(stmt, indent + 2)
        if node.else_body:
            print(f"{prefix}  else:")
            for stmt in node.else_body:
                print_ast(stmt, indent + 2)

    elif node_type == "ReturnStatement":
        print(f"{prefix}ReturnStatement")
        if node.value:
            print_ast(node.value, indent + 1)

    elif node_type == "PrintStatement":
        print(f"{prefix}PrintStatement")
        for arg in node.arguments:
            print_ast(arg, indent + 1)

    elif node_type == "FunctionDef":
        print(f"{prefix}FunctionDef: {node.name}({', '.join(node.parameters)})")
        for stmt in node.body:
            print_ast(stmt, indent + 1)

    elif node_type == "ExpressionStatement":
        print_ast(node.expression, indent)

    elif node_type == "IntLiteral":
        print(f"{prefix}IntLiteral: {node.value}")

    elif node_type == "FloatLiteral":
        print(f"{prefix}FloatLiteral: {node.value}")

    elif node_type == "StringLiteral":
        print(f"{prefix}StringLiteral: {node.value!r}")

    elif node_type == "BooleanLiteral":
        print(f"{prefix}BooleanLiteral: {node.value}")

    elif node_type == "Identifier":
        print(f"{prefix}Identifier: {node.name}")

    elif node_type == "BinaryOp":
        print(f"{prefix}BinaryOp: {node.operator}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

    elif node_type == "UnaryOp":
        print(f"{prefix}UnaryOp: {node.operator}")
        print_ast(node.operand, indent + 1)

    elif node_type == "FunctionCall":
        print(f"{prefix}FunctionCall")
        print(f"{prefix}  function:")
        print_ast(node.function, indent + 2)
        print(f"{prefix}  arguments:")
        for arg in node.arguments:
            print_ast(arg, indent + 2)

    elif node_type == "ArrayLiteral":
        print(f"{prefix}ArrayLiteral")
        for elem in node.elements:
            print_ast(elem, indent + 1)

    elif node_type == "MapLiteral":
        print(f"{prefix}MapLiteral")
        for key, value in node.pairs:
            print(f"{prefix}  key:")
            print_ast(key, indent + 2)
            print(f"{prefix}  value:")
            print_ast(value, indent + 2)

    else:
        print(f"{prefix}{node_type}: {node}")
