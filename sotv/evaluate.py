import json

test_registers = ["a4", "a5"]
test_variables = ["c"]

def main():
    data = json.loads(open("scoreCalculator/results_bulk/bubblesort_old.c.json", "r").read())


    for key, test in data.items():
        print("Evaluating: " + key)
        if isinstance(test, list):
            for lil_test in test:
                funct(lil_test)
        else:
            funct(test)




def funct(test):
    if not "calc" in test.keys():
        calc = test
    else:
        calc = test["calc"]

    metrics_heat = calc["metrics_heat"]

    ratios = {}

    for register in test_registers:
        for variable in test_variables:
            if register not in ratios.keys():
                ratios[register] = 0
            ratios[register] += (metrics_heat[register][variable]/calc["dump_length"])

    tot = 0
    i = 0
    for el in ratios.values():
        i += 1
        tot += el
    print(tot/i * 100)



if __name__ == "__main__":
    main()
