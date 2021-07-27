from elftools.common.py3compat import itervalues
from elftools.dwarf.descriptions import describe_DWARF_expr
from elftools.dwarf.locationlists import LocationParser, LocationExpr
from elftools.elf.elffile import ELFFile


def offset_finder_from_dump(dump: list) -> object:
    for i in range(len(dump)):
        if "addi s0,sp," in dump[i]["next_instruction"]:
            return dump[i + 1]["FP_offsets"]
    return None


def offset_finder(filename: str) -> object:
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
            return None


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


if __name__ == "__main__":
    print(offset_finder("../a.out"))
