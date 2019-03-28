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


from moske.sharedlib.func import extract_func_information as _extract_func_information
from moske.sharedlib.property import (
    extract_property_information as _extract_property_information,
)


def extract_class_information(name: str, cls):
    data = dict()
    data["name"] = name
    data["parents"] = cls.__bases__
    data["routines"] = [
        _extract_func_information(routname, rout)
        for routname, rout in inspect.getmembers(cls, predicate=inspect.isroutine)
    ]
    data["properties"] = [
        _extract_property_information(propname, prop)
        for propname, prop in inspect.getmembers(
            cls, predicate=lambda o: isinstance(o, property)
        )
    ]
    return data
