from sotv.Tracer import tracer
from typing import Dict
from sotv.Tracer.structures import Register


class Metrics:
    metrics_heat: Dict[Register, int]
    metrics_trash: Dict[Register, int]
    tracer: tracer.Tracer

    def __init__(self, completed_tracer):
        self.tracer = completed_tracer
        self.metrics_heat = {}
        self.metrics_trash = {}

    def metric_score(self):
        registers_lock_list = []
        for instruction in self.tracer.execution_dump.dump:
            try:
                registers_status = self.tracer.tracing_graph[instruction]
            except:
                registers_status = None
            if registers_status is not None:
                self.lock(registers_lock_list, instruction.executed_instruction)
                temp_reg = instruction.executed_instruction.modified_register()
                for reg in registers_status.keys():
                    if reg not in registers_lock_list:
                        if reg in self.metrics_heat.keys():
                            self.metrics_heat[reg] += 1
                        else:
                            self.metrics_heat[reg] = 1
                    else:
                        if reg in self.metrics_trash.keys():
                            self.metrics_trash[reg] += 1
                        else:
                            self.metrics_trash[reg] = 1
                for reg in self.metrics_trash.keys():
                    if reg in self.metrics_trash.keys():
                        self.metrics_trash[reg] += 1
                if temp_reg is not None:
                    if temp_reg not in registers_status.keys():
                        if temp_reg in self.metrics_trash.keys():
                            self.metrics_trash[temp_reg] += 1
                        else:
                            self.metrics_trash[temp_reg] = 1
        self.print()

    def lock(self, registers, instruction):
        if instruction.opcode == "mv":
            if instruction.modified_register() in registers:
                registers.remove(instruction.modified_register())
            registers.append(instruction.r2)

    def print(self):
        print(self.metrics_trash)
        print(self.metrics_heat)
