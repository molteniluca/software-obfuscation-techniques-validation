import json
from sotv.Tracer.structures import registers
import matplotlib.pyplot as plt

test_registers = registers.copy()[:32]
test_variables = []

for i in range(112):
    test_variables.append("ctx[{}]".format(i))


def main():
    data = json.loads(open("scoreCalculator/results_bulk/sha256.json", "r").read())
    result = None
    deton_heat = average_heat(data)
    for key in data.keys():
        print("Evaluating: " + key)
        if result is None:
            result = {key: []}
        if key not in result.keys():
            result[key] = []
        result[key].append(funct(data, key))
#        if isinstance(test, list):
#            for lil_test in test:
#                result[key].append(funct(lil_test))
#        else:
#            result[key].append(funct(test))
    temp_dict = {}
    for key in result.keys():
        if key != "plain":
            temp_dict[key] = average(result[key][0])
        else:
            temp_dict[key] = result[key][0]
    result.update(**temp_dict)
    collection = collection_detector(result)
    print(json.dumps(collection, indent=4))
    print_graph(collection)


def print_graph(result):
    dict_2 = {}
    for key in result.keys():
        if "average" in key:
            dict_2[key[1:-len(")_average")]] = 0
    dict_2["plain"] = 0
    for variable in test_variables:
        dict_2["plain"] += result["plain"][0][variable]["tot % of the variable in register subset:"]
        for key in result.keys():
            if "average" in key:
                dict_2[key[1:-len(")_average")]] += result[key][variable]["tot % of the variable in register subset:"]

    plt.bar(list(dict_2.keys()), dict_2.values())
    plt.savefig("chart.png")


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


def average_heat(data):
    dict_heat = {"plain": data["plain"]["DETON"]["mean_heat"]}
    average_heat_list = None
    for lev_obf in data.keys():
        if lev_obf != "plain":
            for elem in data[lev_obf]:
                if average_heat_list is None:
                    average_heat_list = data[lev_obf][elem]["DETON"]["mean_heat"]
                else:
                    average_heat_list = [x + y for x, y in zip(average_heat_list, data[lev_obf][elem]["DETON"]["mean_heat"])]
            dict_heat.update(**{lev_obf: [x / len(data[lev_obf]) for x in average_heat_list]})
        average_heat_list = None
    return dict_heat


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

def score_calc(calc):
    for key in calc.keys():
        if key != "DETON":
            metrics_heat = calc[key]["metrics_heat"]
            ratios = {}
            value = None
            results = None
            for variable in test_variables:
                for register in test_registers:
                    try:
                        try:
                            value = metrics_heat[register][variable] / calc[key]["dump_length"]
                        except KeyError:
                            value = 0
                        ratios[register][variable] += value
                    except KeyError:
                        try:
                            ratios[register].update(**{variable: value})
                        except KeyError:
                            ratios[register] = {variable: value}
                    if results is None:
                        results = {variable: {register: ratios[register][variable] * 100}}
                    else:
                        try:
                            results[variable][register] = ratios[register][variable] * 100
                        except KeyError:
                            results.update(**{variable: {register: (ratios[register][variable] * 100)}})
    return results

def funct(data, key):
    results = []
    if key != "plain":
        for elem in data[key].keys():
            results.append(score_calc(data[key][elem]))
    else:
        results = score_calc(data[key])
    return results




if __name__ == "__main__":
    main()
