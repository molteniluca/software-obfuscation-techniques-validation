from sotv.Tracer import tracer


class Metrics:
    metrics: dict
    tracing_graph: tracer.Tracer.tracing_graph

    def metric_score(self):
        pass
    # first metric higher time of a variable stay in a register unmodified (num_instruction*100)/(Tot_instruction)
    # second metric medium time of a variable stay in a register unmodified
    # third metric a variable stay in more register for more than one instruction (true/false)
    # fourth metric time from the first change to the last one
    # fifth metric the obfuscate code have a hide for the important value? (Example addi 1 , addi -1)
    # sixth metric the code store the value after has end to work with it or there is more rubbish code?
