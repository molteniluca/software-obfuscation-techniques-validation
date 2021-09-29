from sotv.Tracer import tracer


class Metrics:
    metrics_heat: dict
    metrics_trash: dict
    tracer: tracer.Tracer

    def __init__(self, completed_tracer):
        self.tracer: completed_tracer

    def metric_score(self):
        for instruction in self.tracer.execution_dump.dump:
            registers_status = self.tracer.tracing_graph[instruction]
            if registers_status is not None:
                temp_reg = instruction.executed_instruction.modified_register()
                for reg in registers_status.keys():
                    self.metrics_heat[reg] += 1
                for reg in self.metrics_trash.keys():
                    self.metrics_trash[reg] += 1
                if temp_reg is not None:
                    if temp_reg not in registers_status.keys():
                        self.metrics_trash[temp_reg] += 1
        self.print()

    def print(self):
        print(self.metrics_trash)
        print(self.metrics_heat)
