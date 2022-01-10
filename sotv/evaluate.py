import json
import matplotlib.pyplot as plt

test_registers = ["ra", "sp", "gp", "tp", "t0", "t1", "t2", "t3", "t4", "t5", "t6", "s0", "s1", "s2", "s3", "s4",
             "s5", "s6", "s7", "s8", "s9", "s10", "s11", "a0", "a1", "a2", "a3", "a4", "a5", "a6", "a7"]
test_variables = ["crctable", "datablkptr", "0x70df8", "crcaccum", "crc32"]


def main():
    data = json.loads(open("scoreCalculator/results_bulk/crc_32_old.c.json", "r").read())
    result = None
    min_length = data["plain"][0]["calc"]["dump_length"]
    deton_heat = {"plain": data["plain"][0]["DETON"]["mean_heat"]}
    average_heat = None
    for lev_obf in data.keys():
        for elem in data[lev_obf]:
            if lev_obf != "plain":
                if average_heat is None:
                    average_heat = elem["DETON"]["mean_heat"]
                else:
                    average_heat = [x + y for x, y in zip(average_heat, elem["DETON"]["mean_heat"])]
        if lev_obf != "plain":
            deton_heat.update(**{lev_obf: [x/len(data[lev_obf]) for x in average_heat]})
        average_heat = None
    for key, test in data.items():
        print("Evaluating: " + key)
        if result is None:
            result = {key: []}
        if key not in result.keys():
            result[key] = []
        if isinstance(test, list):
            for lil_test in test:
                if lil_test["calc"]["dump_length"] >= min_length:
                    result[key].append(funct(lil_test))
        else:
            if test["calc"]["dump_length"] >= min_length:
                result[key].append(funct(test))
    temp_dict = {}
    for key in result.keys():
        if key != "plain":
            temp_dict[key + "_average"] = average(result[key])
    result.update(**temp_dict)
    print(json.dumps(result, indent=4))
    print_graph(result)

def print_graph(result):
    dict_2={}
    dict_2["plain"]=result["plain"][0]['crc32']["tot % of the variable in register subset:"]
    for key in result.keys():
        if "average" in key:
            dict_2[key[1:-len(")_average")]] = result[key]['crctable']["tot % of the variable in register subset:"]


    plt.bar(list(dict_2.keys()), dict_2.values())
    plt.savefig("myfig.png")


def average(list_val):
    temp_elem = None
    for elem in list_val:
        for var in test_variables:
            if temp_elem is None:
                temp_elem = dict(elem)
            else:
                if len(list_val) != 1:
                    for key in temp_elem[var].keys():
                        temp_elem[var][key] += elem[var][key]
    if temp_elem is not None:
        for val in temp_elem.keys():
            for key in temp_elem[val].keys():
                temp_elem[val][key] = temp_elem[val][key]/len(list_val)
    return temp_elem


def funct(test):
    if "calc" not in test.keys():
        calc = test
    else:
        calc = test["calc"]

    metrics_heat = calc["metrics_heat"]

    ratios = {}
    value = None
    results = None

    for variable in test_variables:
        tot = 0
        i = 0
        for register in test_registers:
            try:
                try:
                    value = metrics_heat[register][variable] / calc["dump_length"]
                except KeyError:
                    value = 0
                ratios[register][variable] += value
            except KeyError:
                try:
                    ratios[register].update(**{variable: value})
                except KeyError:
                    ratios[register] = {variable: value}
            temp = "tot % of the variable in " + register
            if results is None:
                results = {variable: {temp: ratios[register][variable] * 100}}
            else:
                try:
                    results[variable][temp] = ratios[register][variable] * 100
                except KeyError:
                    results.update(**{variable: {temp: (ratios[register][variable] * 100)}})

            if variable in ratios[register].keys():
                tot += ratios[register][variable]
        temp = "tot % of the variable in register subset:"
        results[variable][temp] = (tot * 100)
    return results


if __name__ == "__main__":
    main()
