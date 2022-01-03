import json

test_registers = ["a4", "a5"]
test_variables = ["n", "0xafffffc8", "d"]


def main():
    data = json.loads(open("scoreCalculator/results_bulk/bubblesort_old.c.json", "r").read())
    result = None
    min_length = data["plain"][0]["calc"]["dump_length"]
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


def average(list_val):
    temp_elem = None
    for elem in list_val:
        for var in test_variables:
            if temp_elem is None:
                temp_elem = dict(elem)
            else:
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

    results = None

    for variable in test_variables:
        tot = 0
        i = 0
        for register in test_registers:
            try:
                ratios[register][variable] += (metrics_heat[register][variable] / calc["dump_length"])
            except KeyError:
                ratios[register] = {variable: (metrics_heat[register][variable] / calc["dump_length"])}
            temp = "tot % of the variable in " + register
            if results is None:
                results = {variable: {temp: ratios[register][variable] * 100}}
            else:
                results[variable][temp] = ratios[register][variable] * 100

        for register in test_registers:
            tot += sum(ratios[register].values())
        temp = "tot % of the variable in register subset:"
        results[variable][temp] = (tot * 100)
    return results


if __name__ == "__main__":
    main()
