from sotv.Tracer import tracer
from typing import Dict


from sotv.Tracer.structures import Register


# Updates the dictionary of the variable at his last edit
def lock(variables, registers_status):
    variables_names = variables.keys()
    for reg in registers_status:
        for temp in registers_status[reg].keys():
            if temp not in variables_names:
                for number in registers_status[reg][temp].keys():
                    try:
                        if variables[temp] < number:
                            variables[temp] = number
                    except KeyError:
                        variables[temp] = number
            for elem in variables.keys():
                if elem == temp:
                    for number in registers_status[reg][temp].keys():
                        if variables[temp] < number:
                            variables[elem] = number


def verify_is_update(variables, register):
    for elem in register:
        if elem in variables.keys():
            for number in register[elem].keys():
                if number == variables[elem]:
                    return True
    return False


def verify_elem_in_dict(reg, metric, variables, variable_name, reg_status):
    if reg in metric.keys() and variable_name in metric[reg].keys() and variables[variable_name] in reg_status[reg][variable_name].keys():
        return True
    return False


class Metrics:
    metrics_heat: Dict[Register, Dict[str, int]]
    tracer: tracer.Tracer

    def __init__(self, completed_tracer):
        self.tracer = completed_tracer
        self.metrics_heat = {}
        self.metrics_trash = {}
        self.old_variables = {}

    def metric_score(self):
        variables = {}
        for instruction in self.tracer.execution_dump.dump:
            try:
                registers_status = self.tracer.tracing_graph[instruction]
            except KeyError:
                registers_status = None
            if registers_status is not None:
                for reg in registers_status.keys():
                    lock(variables, registers_status)
                    if verify_is_update(variables, registers_status[reg]):
                        for var_name in registers_status[reg].keys():
                            if verify_elem_in_dict(reg, self.metrics_heat, variables, var_name, registers_status):
                                self.metrics_heat[reg][var_name] += 1
                            else:
                                try:
                                    self.metrics_heat[reg][var_name] = 1
                                except KeyError:
                                    self.metrics_heat[reg] = {var_name: 1}

#    @deprecated
#    use to track not correlated changes to the code
#    def trash_detector(self, register):
#        if register is not None:
#            if register not in not_trash_registers:
#                if register in self.metrics_trash.keys():
#                    self.metrics_trash[register] += 1
#                else:
#                    self.metrics_trash[register] = 1

    def print(self):
        print("metrics_heat")
        print(self.metrics_heat)

    def get_dict(self):
        return {
            "metrics_heat": self.metrics_heat,
        }
