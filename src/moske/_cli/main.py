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
import argparse

from moske.translator import translate_package


def main():

    POSSIBLE_TO_DELETE = ["body", "docstring"]

    parser = argparse.ArgumentParser(description="MOdule SKEleton generator")
    parser.add_argument("pkgname", help="name of the module to process")
    parser.add_argument(
        "--out",
        "-o",
        help="path where the skeleton will be generated",
        type=os.path.abspath,
        default=os.getcwd(),
    )
    parser.add_argument(
        "-r",
        "--remove",
        help=(
            "portions of code to remove from the original package. "
            "\nNote: the generated output will not include comments."
        ),
        choices=POSSIBLE_TO_DELETE,
        nargs="*",
        default=POSSIBLE_TO_DELETE,
    )
    parser.add_argument(
        "-b",
        "--use-black",
        help="if set, the output will be formatted with Black.",
        action="store_true",
    )
    parser.add_argument(
        "--generate-sharedlib-interface",
        help=(
            "if set, moske will try to generate an equivalent Python file for each "
            "'C extension for CPython' found."
        ),
        action="store_true",
    )
    # parser.add_argument(
    #     "-g", "--debug", help="activate debug mode.", action="store_false"
    # )
    args = parser.parse_args()

    translate_package(
        args.pkgname,
        args.out,
        args.remove,
        args.use_black,
        args.generate_sharedlib_interface,
    )
