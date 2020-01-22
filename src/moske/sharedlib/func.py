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

import inspect

from moske.sharedlib.utils import empty_or_none as _empty_or_none


def extract_func_information(name: str, func) -> dict:
    data = dict()
    data["name"] = name
    if type(func).__name__ == "instancemethod":
        data["DOCUMENTATION"] = type(func).__doc__
    try:
        signature = inspect.signature(func)
    except ValueError:
        # No signature can be provided
        return data
    except TypeError:
        print(
            "Object of type {} is not supported by inspect.signature.".format(
                type(func)
            )
        )
        return data
    data["parameters"] = list()
    data["dependson"] = set()
    for name, parameter in signature.parameters.items():
        annotation = _empty_or_none(inspect.Parameter, parameter.annotation)
        data["parameters"].append(
            {
                "name": parameter.name,
                "default": _empty_or_none(inspect.Parameter, parameter.default),
                "annotation": annotation,
            }
        )
        if annotation is not None:
            data["dependson"].add(annotation)
    data["return_annotation"] = _empty_or_none(
        inspect.Signature, signature.return_annotation
    )
    return data
