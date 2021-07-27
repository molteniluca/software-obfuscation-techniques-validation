from elftools.common.py3compat import itervalues
from elftools.dwarf.descriptions import describe_DWARF_expr
from elftools.dwarf.locationlists import LocationParser, LocationExpr
from elftools.elf.elffile import ELFFile
from typing import Tuple, Dict, List

from sotv.EDG.exceptions import ELFWithoutSymbols
from sotv.EDG.exceptions import DumpWithoutSymbols


def offset_finder_from_dump(dump: list) -> Dict[str, int]:
    """
    Finds the variable offsets from an execution dump
    @param dump: The execution dump
    @return: A dictionary in which the keys are the variables name in gdb notation and the values are the offsets
    """
    for i in range(len(dump)):
        if "addi s0,sp," in dump[i]["next_instruction"]:
            return dump[i + 1]["FP_offsets"]
    raise DumpWithoutSymbols


def offset_finder(filename: str) -> Tuple[Dict[str, dict], Dict[str, int]]:
    """
    Finds variables offset from a elf file
    @param filename: path of the elf file
    @return: a tuple of two elements, the first is a dictionary in which the keys are the functions and the values are
            the lists of variables, the second is a list of global variables
    """

    with open(filename, "rb") as file:
        elf_file = ELFFile(file)

        if elf_file.has_dwarf_info():
            function_vars = {}
            global_vars = {}

            dwarf = elf_file.get_dwarf_info()
            location_parser = LocationParser(dwarf.location_lists())

            for CU in dwarf.iter_CUs():
                for DIE in CU.get_top_DIE().iter_children():
                    if DIE.tag == "DW_TAG_variable":
                        decoded = decode_variable(CU, dwarf, DIE, location_parser)
                        global_vars[decoded[0]] = decoded[1]
                    else:
                        for variable in DIE.iter_children():
                            decoded = decode_variable(CU, dwarf, variable, location_parser)
                            if decoded is not None:
                                try:
                                    function_vars[DIE.attributes["DW_AT_name"].value.decode()]
                                except KeyError:
                                    function_vars[DIE.attributes["DW_AT_name"].value.decode()] = {}
                                function_vars[DIE.attributes["DW_AT_name"].value.decode()][decoded[0]] = decoded[1]

            return function_vars, global_vars
        else:
            raise ELFWithoutSymbols


def decode_variable(cu, dwarf, variable, location_parser):
    for attr in itervalues(variable.attributes):
        if location_parser.attribute_has_location(attr, cu['version']):
            loc = location_parser.parse_from_attribute(attr, cu['version'])
            if isinstance(loc, LocationExpr):
                described = describe_DWARF_expr(loc.loc_expr, dwarf.structs, cu.cu_offset)
                if "DW_OP_fbreg" in described:
                    return variable.attributes["DW_AT_name"].value.decode(),\
                       int(described.split("(DW_OP_fbreg: ")[1][:-1], 16)
                elif "DW_OP_addr" in described:
                    return variable.attributes["DW_AT_name"].value.decode(),\
                       int(described.split("(DW_OP_addr: ")[1][:-1], 16)


def to_gdb_notation(function_vars, global_vars) -> List[str]:
    """
    This method transforms a set of variables in gdb notation variables
    @param function_vars: The variables inside a function
    @param global_vars: The global functions
    @return: The list containing the variables in gdb-like notation
    """
    gdb_symbols = []

    for fun in function_vars:
        for var in function_vars[fun]:
            gdb_symbols.append(fun+"::"+var)

    for var in global_vars:
        gdb_symbols.append(var)

    return gdb_symbols


if __name__ == "__main__":
    print(offset_finder("../a.out"))
    print(to_gdb_notation(*offset_finder("../a.out")))
