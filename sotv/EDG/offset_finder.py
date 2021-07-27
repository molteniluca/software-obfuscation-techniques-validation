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
            values = {}

            dwarf = elf_file.get_dwarf_info()
            location_parser = LocationParser(dwarf.location_lists())

            for CU in dwarf.iter_CUs():
                for functionDie in CU.get_top_DIE().iter_children():
                    for variable in functionDie.iter_children():
                        for attr in itervalues(variable.attributes):
                            if location_parser.attribute_has_location(attr, CU['version']):
                                loc = location_parser.parse_from_attribute(attr, CU['version'])
                                if isinstance(loc, LocationExpr):
                                    try:
                                        tmp=values[functionDie.attributes["DW_AT_name"].value.decode()]
                                    except:
                                        values[functionDie.attributes["DW_AT_name"].value.decode()] = {}
                                    values[functionDie.attributes["DW_AT_name"].value.decode()][variable.attributes["DW_AT_name"].value.decode()] = int(describe_DWARF_expr(
                                        loc.loc_expr, dwarf.structs, CU.cu_offset).split("(DW_OP_fbreg: ")[1][:-1])
            return values
        else:
            return None


if __name__ == "__main__":
    print(offset_finder("../a.out"))
