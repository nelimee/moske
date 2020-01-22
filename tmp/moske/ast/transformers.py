import ast
from moske.ast.docstring import get_docstring_node, delete_docstring


class DeleteFunctionParts(ast.NodeTransformer):
    def __init__(self, delete_function_body: bool, delete_docstring: bool):
        pass

    def visit_FunctionDef(self, node):
        pass
