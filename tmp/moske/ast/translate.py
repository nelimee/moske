import ast
import astor
from moske.ast.transformers import DeleteFunctionParts


def translate(
    python_file_path: str, delete_function_body: bool, delete_docstring: bool
) -> str:
    pass
