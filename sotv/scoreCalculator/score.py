from sotv.Tracer import tracer
from typing import Dict

from sotv.Tracer.defines import not_trash_registers
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


def verify(variables, register):
    for elem in register:
        if elem in variables.keys():
            for number in register[elem].keys():
                if number == variables[elem]:
                    return True
    return False


class Metrics:
    metrics_heat: Dict[Register, int]
    metrics_trash: Dict[Register, int]
    old_variables: Dict[Register, int]
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
                    if verify(variables, registers_status[reg]):
                        if reg in self.metrics_heat.keys():
                            self.metrics_heat[reg] += 1
                        else:
                            self.metrics_heat[reg] = 1
                    else:
                        if reg in self.old_variables.keys():
                            self.old_variables[reg] += 1
                        else:
                            self.old_variables[reg] = 1
                        self.trash_detector(instruction.executed_instruction.modified_register())

    def trash_detector(self, register):
        if register is not None:
            if register not in not_trash_registers:
                if register in self.metrics_trash.keys():
                    self.metrics_trash[register] += 1
                else:
                    self.metrics_trash[register] = 1

    def print(self):
        print("old_variables")
        print(self.old_variables)
        print("metrics_heat")
        print(self.metrics_heat)
        print("trash_added")
        print(self.metrics_trash)

    def get_dict(self):
        return {
            "old_variables": self.old_variables,
            "metrics_heat": self.metrics_heat,
            "trash_added": self.metrics_trash
        }