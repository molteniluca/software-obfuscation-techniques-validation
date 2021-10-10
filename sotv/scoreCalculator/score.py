from sotv.Tracer import tracer
from typing import Dict
from sotv.Tracer.structures import Register


# Updates the dictionary of the variable at his last edit
def lock(variables, string):
    temp_list = string.split("_")
    if temp_list[0] in variables.keys():
        if temp_list[1] > variables[temp_list[0]]:
            variables[temp_list[0]] = temp_list[1]
    else:
        variables[temp_list[0]] = temp_list[1]


# Condition that check if there are in the same register a variable not updated and ignore duplicates
def condition(register_status, register, lock_dict):
    variable_dict = {}
    # initialize variable_dict with the variable that are in the register
    for variable in register_status[register]:
        temp = variable.split("_")
        if temp[0] in variable_dict.keys():
            if variable_dict[temp[0]] < temp[1]:
                variable_dict[temp[0]] = temp[1]
        else:
            variable_dict[temp[0]] = temp[1]
    # search if in another register there is a more update version of the variables that are in variable_dict
    for reg in register_status.keys():
        if reg != register:
            for elem in register_status[reg]:
                temp = elem.split("_")
                if temp[0] in variable_dict.keys():
                    if temp[1] > variable_dict[temp[0]]:
                        return True
    # in the case of register a0:{a_0, a_1} but the last edit on the a is a_3
    for var in variable_dict.keys():
        if var in lock_dict.keys() and lock_dict[var] > variable_dict[var]:
            return True  # this return is reached in some wrong cases
    return False


class Metrics:
    metrics_heat: Dict[Register, int]
    metrics_trash: Dict[Register, int]
    tracer: tracer.Tracer

    def __init__(self, completed_tracer):
        self.tracer = completed_tracer
        self.metrics_heat = {}
        self.metrics_trash = {}

    def metric_score(self):
        lock_dict = {}
        for instruction in self.tracer.execution_dump.dump:
            try:
                registers_status = self.tracer.tracing_graph[instruction]
            except KeyError:
                registers_status = None
            if registers_status is not None:
                for reg in registers_status.keys():
                    for string in registers_status[reg]:
                        lock(lock_dict, string)
                    for string in registers_status[reg]:
                        temp_split = string.split("_")
                        if reg in self.metrics_heat.keys():
                            if lock_dict[temp_split[0]] <= temp_split[1]:
                                self.metrics_heat[reg] += 1
                            else:
                                if condition(registers_status, reg, lock_dict):
                                    if reg in self.metrics_trash.keys():
                                        self.metrics_trash[reg] += 1
                                    else:
                                        self.metrics_trash[reg] = 1
                        else:
                            self.metrics_heat[reg] = 1
                    temp_reg = instruction.executed_instruction.modified_register()
                    # case that the instruction modified a register that is not in the tracer
                    if temp_reg is not None:
                        if temp_reg not in registers_status.keys():
                            if temp_reg in self.metrics_trash.keys():
                                self.metrics_trash[temp_reg] += 1
                            else:
                                self.metrics_trash[temp_reg] = 1
        self.print()

    def print(self):
        print(self.metrics_heat)
        print(self.metrics_trash)
