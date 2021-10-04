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
        for instruction in self.tracer.execution_dump.dump:
            try:
                registers_status = self.tracer.tracing_graph[instruction]
            except:
                registers_status = None
            if registers_status is not None:
                temp_reg = instruction.executed_instruction.modified_register()
                for reg in registers_status.keys():
                    if reg in self.metrics_heat.keys():
                        self.metrics_heat[reg] += 1
                    else:
                        self.metrics_heat[reg] = 1
                for reg in self.metrics_trash.keys():
                    if reg in self.metrics_trash.keys():
                        self.metrics_trash[reg] += 1
                    else:
                        self.metrics_trash[reg] = 1
                if temp_reg is not None:
                    if temp_reg not in registers_status.keys():
                        if temp_reg in self.metrics_trash.keys():
                            self.metrics_trash[temp_reg] += 1
                        else:
                            self.metrics_trash[temp_reg] = 1
        self.print()

    def print(self):
        print(self.metrics_trash)
        print(self.metrics_heat)
