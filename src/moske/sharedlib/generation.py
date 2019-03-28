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


def func_repr(data):
    return "def {funcname}({args}){ret}:\n\tpass\n\n".format(
        funcname=data["name"],
        args=", ".join(
            [
                "{name}{typehint}{default}".format(
                    name=p["name"],
                    typehint=(
                        ": {type}".format(type=p["annotation"].__name__)
                        if p["annotation"] is not None
                        else ""
                    ),
                    default=(
                        " = {val}".format(val=p["default"])
                        if p["default"] is not None
                        else ""
                    ),
                )
                for p in data["parameters"]
            ]
        )
        if "parameters" in data
        else "",
        ret=(
            " -> {rettype}".format(rettype=data["return_annotation"].__name__)
            if "return_annotation" in data and data["return_annotation"] is not None
            else ""
        ),
    )


def class_repr(data):
    return "class {classname}{classparents}:\n\n{methods}\n\n".format(
        classname=data["name"],
        classparents=(
            "({})".format(", ".join([parent.__name__ for parent in data["parents"]]))
            if data["parents"]
            else ""
        ),
        methods="\t"
        + "\n".join([func_repr(func_data) for func_data in data["routines"]]).replace(
            "\n", "\n\t"
        )
        if data["routines"]
        else "\tpass",
    )


def module_repr(data):
    return "\n".join(
        [class_repr(cls_data) for cls_data in data["classes"]]
        + [func_repr(func_data) for func_data in data["func"]]
    )


def generate(data, path: str):
    # We take only the modules, not the packages.
    for module in data:
        if module["ispkg"]:
            continue
        module_file = os.path.join(path, *(module["name"].split("."))) + ".py"
        module_dir = os.path.dirname(module_file)
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)
        with open(module_file, "w") as mf:
            mf.write(module_repr(module))
