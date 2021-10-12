from sotv.Tracer import tracer
from typing import Dict
from sotv.Tracer.structures import Register


# Updates the dictionary of the variable at his last edit
def lock(variables, registers_status):
    temp1_list = []
    for elem in variables:
        temp1_list.append(elem.split("_")[0])
    for reg in registers_status:
        for temp in registers_status[reg]:
            temp_list = temp.split("_")
            if temp_list[0] not in temp1_list:
                variables.append(temp)
            for elem in variables:
                if elem.split("_")[0] == temp_list[0]:
                    if elem.split("_")[1] < temp_list[1]:
                        variables.remove(elem)
                        variables.append(temp)


def verify(variables, register):
    for elem in register:
        if elem in variables:
            return True
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
        lock_dict = []
        for instruction in self.tracer.execution_dump.dump:
            try:
                registers_status = self.tracer.tracing_graph[instruction]
            except KeyError:
                registers_status = None
            if registers_status is not None:
                for reg in registers_status.keys():
                    lock(lock_dict, registers_status)
                    if verify(lock_dict, registers_status[reg]):
                        if reg in self.metrics_heat.keys():
                            self.metrics_heat[reg] += 1
                        else:
                            self.metrics_heat[reg] = 1
                    else:
                        if reg in self.metrics_trash.keys():
                            self.metrics_trash[reg] += 1
                        else:
                            self.metrics_trash[reg] = 1
                    temp_reg = instruction.executed_instruction.modified_register()
                    # case that the instruction modified a register that is not in the tracer
                    if temp_reg is not None:
                        if temp_reg not in registers_status.keys():
                            if temp_reg in self.metrics_trash.keys():
                                self.metrics_trash[temp_reg] += 1
                            else:
                                self.metrics_trash[temp_reg] = 1
        self.print()
        print(lock_dict)

    def print(self):
        print(self.metrics_heat)
        print(self.metrics_trash)
