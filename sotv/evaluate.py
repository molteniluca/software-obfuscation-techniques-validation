import json
from sotv.Tracer.structures import registers
from matplotlib import pyplot


test_registers = registers.copy()[:32]
test_variables = []

for i in range(108):
    test_variables.append("ctx[{}]".format(i))

def main():
    data = json.loads(open("scoreCalculator/results_bulk/sha256.c.json", "r").read())
    result = None
    min_length = data["plain"][0]["calc"]["dump_length"]
    DETON_heat = {"plain": {test_registers[x]: data["plain"][0]["DETON"]["mean_heat"][x] for x in range(len(test_registers))}}
    average_heat = None
    for lev_obf in data.keys():
        for elem in data[lev_obf]:
            if lev_obf != "plain":
                if average_heat is None:
                    average_heat = elem["DETON"]["mean_heat"]
                else:
                    average_heat = [x + y for x, y in zip(average_heat, elem["DETON"]["mean_heat"])]
        if lev_obf != "plain":
            DETON_heat.update(**{lev_obf: {test_registers[x]: average_heat[x] / len(data[lev_obf]) for x in range(len(average_heat))}})
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
            temp_dict[key] = average(result[key])
        else:
            temp_dict[key] = result[key][0]
    result.update(**temp_dict)
    open("heat.json", "w").write(json.dumps(DETON_heat, indent=4))
    open("score.json", "w").write(json.dumps(collection_detector(result), indent=4))
    save_histogram(collection_detector(result), DETON_heat)



def collection_detector(score):
    collections_score = None
    collection_list = []
    for elem in test_variables:
        if "[" in elem:
            temp = elem.split("[")[0]
            if temp not in collection_list:
                collection_list.append(temp)
    for lev_obf in score.keys():
        for var in score[lev_obf].keys():
            if var.split("[")[0] in collection_list:
                for reg in score[lev_obf][var].keys():
                    if collections_score is None:
                        collections_score = {lev_obf: {var.split("[")[0]: {reg: score[lev_obf][var][reg]}}}
                    else:
                        try:
                            collections_score[lev_obf][var.split("[")[0]][reg] += score[lev_obf][var][reg]
                        except KeyError:
                            if lev_obf not in collections_score.keys():
                                collections_score.update(**{lev_obf: {var.split("[")[0]: {reg: score[lev_obf][var][reg]}}})
                            elif var.split("[")[0] not in collections_score[lev_obf].keys():
                                collections_score[lev_obf].update(**{var.split("[")[0]: {reg: score[lev_obf][var][reg]}})
                            else:
                                collections_score[lev_obf][var.split("[")[0]].update(**{reg: score[lev_obf][var][reg]})
    return collections_score


def save_histogram(data):
    new_list=[]
    for arr in data.values():
        for el in arr:
            calc = el["calc"]
            DETON = el["DETON"]
            for var in test_variables:
                for idx, reg in enumerate(test_registers):
                    try:
                        new_list.append((DETON["mean_heat"][idx], calc["metrics_heat"][reg][var]/calc["dump_length"]))
                    except KeyError as e:
                        new_list.append((DETON["mean_heat"][idx], 0))

    pyplot.scatter(*zip(*new_list))
    pyplot.xlabel("DETON")
    pyplot.ylabel("REAL")
    pyplot.show()


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
                temp_elem[val][key] = temp_elem[val][key] / len(list_val)
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
            temp = register
            if results is None:
                results = {variable: {temp: ratios[register][variable]}}
            else:
                try:
                    results[variable][temp] = ratios[register][variable]
                except KeyError:
                    results.update(**{variable: {temp: (ratios[register][variable])}})
    return results


if __name__ == "__main__":
    main()
