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


def extract_property_information(propname: str, prop):
    data = dict()
    data["name"] = propname
    data["func"] = {kind: None for kind in ("get", "set", "del")}
    for fname, func in inspect.getmembers(prop, predicate=inspect.isfunction):
        assert fname.startswith("f")
        fkind = fname[1:]
        signature = inspect.signature(func)
        data["func"][fkind] = {
            "return_annotation": _empty_or_none(
                inspect.Signature, signature.return_annotation
            ),
            "parameters": [
                {
                    "name": pname,
                    "default": _empty_or_none(inspect.Parameter, parameter.default),
                    "annotation": _empty_or_none(
                        inspect.Parameter, parameter.annotation
                    ),
                }
                for pname, parameter in signature.parameters.items()
            ],
        }

    return data
