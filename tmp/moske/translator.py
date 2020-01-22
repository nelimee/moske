import os
import importlib
from moske.ast.translate import translate as translate_python2python
from moske.sharedlib.translate import translate as translate_sharedlib2python


def translate_package(
    pkgname: str,
    out_dir: str,
    parts_to_remove,
    use_black: bool,
    generate_sharedlib_interface: bool,
):
    pass
