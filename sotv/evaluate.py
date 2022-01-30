import json
from sotv.Tracer.structures import registers
import matplotlib.pyplot as plt
from numpy import random
from itertools import combinations

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
    group_average(collection, deton_heat)


def group_average(collection_score, heat, num_reg=6, name_collection = "ctx"):
    subset_list = random.choice(test_registers, num_reg, False)
    subset_list_2 = list(combinations(subset_list, 2))
    subset_list_4 = list(combinations(subset_list, 4))
    temp_score = None
    temp_heat = None
    for lev_obf in collection_score.keys():
        value_heat = 0
        value_score = 0
        for elem in subset_list:
            if temp_score is None:
                temp_score = {lev_obf: {elem: collection_score[lev_obf][name_collection][elem]}}
            elif lev_obf not in temp_score.keys():
                temp_score.update(**{lev_obf: {elem: collection_score[lev_obf][name_collection][elem]}})
            else:
                temp_score[lev_obf].update(**{elem: collection_score[lev_obf][name_collection][elem]})
            if temp_heat is None:
                temp_heat = {lev_obf: {elem: heat[lev_obf][elem]}}
            elif lev_obf not in temp_heat.keys():
                temp_heat.update(**{lev_obf: {elem: heat[lev_obf][elem]}})
            else:
                temp_heat[lev_obf].update(**{elem: heat[lev_obf][elem]})
            value_heat += heat[lev_obf][elem]
            value_score += collection_score[lev_obf]["ctx"][elem]
        temp_score[lev_obf].update(**{"AVG_1": value_score/len(subset_list)})
        temp_heat[lev_obf].update(**{"AVG_1": value_heat/len(subset_list)})
        value_heat = 0
        value_score = 0
        for elem in subset_list_2:
            value_t_1 = (collection_score[lev_obf][name_collection][elem[0]] + collection_score[lev_obf][name_collection][elem[1]])/2
            value_t_2 = (heat[lev_obf][elem[0]] + heat[lev_obf][elem[1]])/2
            value_score += value_t_1
            value_heat += value_t_2
            if lev_obf not in temp_heat.keys():
                temp_heat.update(**{lev_obf: {str(elem): value_t_2}})
            else:
                temp_heat[lev_obf].update(**{str(elem): value_t_2})
            if lev_obf not in temp_score.keys():
                temp_score.update(**{lev_obf: {str(elem): value_t_1}})
            else:
                temp_score[lev_obf].update(**{str(elem): value_t_1})
            temp_score[lev_obf].update(**{"AVG_2": value_score / len(subset_list_2)})
            temp_heat[lev_obf].update(**{"AVG_2": value_heat / len(subset_list_2)})
        value_heat = 0
        value_score = 0
        for elem in subset_list_4:
            value_t_1 = (collection_score[lev_obf][name_collection][elem[0]] + collection_score[lev_obf][name_collection][elem[1]] +
                         collection_score[lev_obf][name_collection][elem[2]] + collection_score[lev_obf][name_collection][elem[3]])/4
            value_t_2 = (heat[lev_obf][elem[0]] + heat[lev_obf][elem[1]] +
                         heat[lev_obf][elem[2]] + heat[lev_obf][elem[3]] )/4
            value_heat += value_t_2
            value_score += value_t_1
            if lev_obf not in temp_heat.keys():
                temp_heat.update(**{lev_obf: {str(elem): value_t_2}})
            else:
                temp_heat[lev_obf].update(**{str(elem): value_t_2})
            if lev_obf not in temp_score.keys():
                temp_score.update(**{lev_obf: {str(elem): value_t_1}})
            else:
                temp_score[lev_obf].update(**{str(elem): value_t_1})
            temp_score[lev_obf].update(**{"AVG_4": value_score / len(subset_list_2)})
            temp_heat[lev_obf].update(**{"AVG_4": value_heat / len(subset_list_2)})

    to_be_printed = ["AVG_1", "AVG_2", "AVG_4"]
    deton_params = ['plain', '0_0_1_1', '0_0_10_1', '0_0_20_1', '0_0_30_1', '0_0_40_1', '0_0_50_1', '0_1_0_1',
                    '0_2_0_1', '0_3_0_1', '0_4_0_1', '0_5_0_1', '0_1_10_1', '0_2_20_1', '0_3_30_1']

    print_graph(temp_heat, temp_score, to_be_printed, deton_params)


def print_graph(temp_heat, temp_score, to_be_printed, deton_params):
    fig, to_be_printed_graphs = plt.subplots(len(to_be_printed))

    for i, to_print in enumerate(to_be_printed):
        x_array = []
        SCORE_array = []
        DETON_array = []

        for key in deton_params:
            value = temp_score[key]
            x_array.append(key)
            SCORE_array.append(value[to_print])
            DETON_array.append(temp_heat[key][to_print])

        to_be_printed_graphs[i].plot(x_array, SCORE_array, color="blue", label="Calculated Score")
        to_be_printed_graphs[i].set_ylabel('Score', color="blue")
        to_be_printed_graphs[i].set_title(to_print)
        to_be_printed_graphs[i].tick_params(axis='y', labelcolor="blue")

        second_graph = to_be_printed_graphs[i].twinx()
        second_graph.set_ylabel("DETON Heat", color='red')
        second_graph.plot(x_array, DETON_array, color="red")
        second_graph.tick_params(axis='y', labelcolor="red")

    fig.tight_layout()
    plt.tight_layout()
    plt.show()


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
    dict_heat = {"plain": {test_registers[x]: data["plain"]["DETON"]["mean_heat"][x] for x in range(len(test_registers))}}
    average_heat_list = None
    for lev_obf in data.keys():
        if lev_obf != "plain":
            for elem in data[lev_obf]:
                if average_heat_list is None:
                    average_heat_list = data[lev_obf][elem]["DETON"]["mean_heat"]
                else:
                    average_heat_list = [x + y for x, y in zip(average_heat_list, data[lev_obf][elem]["DETON"]["mean_heat"])]
            dict_heat.update(**{lev_obf: {test_registers[x]: average_heat_list[x] / len(data[lev_obf]) for x in range(len(average_heat_list))}})
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
