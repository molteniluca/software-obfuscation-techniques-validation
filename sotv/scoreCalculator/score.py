from sotv.Tracer import tracer


class Metrics:
    metrics = {"higher_register_heat": 0, "average_register_heat": 0,
               "variable_stay_in_a_register_after_been_used(move or sw)": False}
    tracer: None

    def __init__(self, completed_tracer):
        self.tracer: completed_tracer

    def metric_score(self):
        pass
