def offset_finder(dump: list) -> object:
    for i in range(len(dump)):
        if "addi s0,sp," in dump[i]["next_instruction"]:
            return dump[i+1]["FP_offsets"]
    return None
