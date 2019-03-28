# ======================================================================
# Copyright CERFACS (March 2019)
# Contributor: Adrien Suau (adrien.suau@cerfacs.fr)
#
# This software is governed by the CeCILL-B license under French law and
# abiding  by the  rules of  distribution of free software. You can use,
# modify  and/or  redistribute  the  software  under  the  terms  of the
# CeCILL-B license as circulated by CEA, CNRS and INRIA at the following
# URL "http://www.cecill.info".
#
# As a counterpart to the access to  the source code and rights to copy,
# modify and  redistribute granted  by the  license, users  are provided
# only with a limited warranty and  the software's author, the holder of
# the economic rights,  and the  successive licensors  have only limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using, modifying and/or  developing or reproducing  the
# software by the user in light of its specific status of free software,
# that  may mean  that it  is complicated  to manipulate,  and that also
# therefore  means that  it is reserved for  developers and  experienced
# professionals having in-depth  computer knowledge. Users are therefore
# encouraged  to load and  test  the software's  suitability as  regards
# their  requirements  in  conditions  enabling  the  security  of their
# systems  and/or  data to be  ensured and,  more generally,  to use and
# operate it in the same conditions as regards security.
#
# The fact that you  are presently reading this  means that you have had
# knowledge of the CeCILL-B license and that you accept its terms.
# ======================================================================

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
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    delete_function_body = "body" in parts_to_remove
    delete_docstring = "docstring" in parts_to_remove

    pkg = importlib.import_module(pkgname)
    pkg_dir = pkg.__path__[0]
    parent_pkg_dir = os.path.dirname(pkg_dir)

    for root, dirs, files in os.walk(pkg_dir):
        for file in files:
            python_code = None
            file_path = os.path.join(root, file)
            if file.endswith(".py"):
                python_code = translate_python2python(
                    file_path,
                    delete_function_body=delete_function_body,
                    delete_docstring=delete_docstring,
                )
            elif generate_sharedlib_interface and (
                file.endswith(".so") or file.endswith(".pyd")
            ):
                sharedlib_relative_path = file_path[len(parent_pkg_dir) + 1 :]
                sharedlib_relative_path_noext = os.path.splitext(
                    sharedlib_relative_path
                )[0]
                modname = ".".join(sharedlib_relative_path_noext.split(os.path.sep))
                python_code = translate_sharedlib2python(modname)

            if python_code is not None:
                full_out_path = file_path.replace(parent_pkg_dir, out_dir)
                full_out_path = os.path.splitext(full_out_path)[0] + os.extsep + "py"
                full_out_dir = os.path.dirname(full_out_path)
                if not os.path.exists(full_out_dir):
                    os.makedirs(full_out_dir)

                if use_black:
                    import black

                    python_code = black.format_str(
                        python_code,
                        mode=black.FileMode(
                            target_versions={black.TargetVersion.PY34},
                            line_length=black.DEFAULT_LINE_LENGTH,
                            is_pyi=False,
                            string_normalization=True,
                        ),
                    )

                with open(full_out_path, "w") as out:
                    out.write(python_code)
