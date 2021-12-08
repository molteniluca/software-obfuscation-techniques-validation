import json

test_registers = ["a4", "a5"]
test_variables = ["n"]


def main():
    data = json.loads(open("scoreCalculator/results_bulk/bubblesort.json", "r").read())
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
    print(result)


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
                results = {variable: {temp: format(ratios[register][variable] * 100, '.2f')}}
            else:
                results[variable][temp] = format(ratios[register][variable] * 100, '.2f')
        for register in test_registers:
            for el in ratios[register].values():
                i += 1
                tot += el
        temp = "tot % of the variable in register subset:"
        results[variable][temp] = format((tot / i * 100), '.2f')
    return results


if __name__ == "__main__":
    main()
