""""
this interface handle the tracing after a specific type of instruction
"""


class AdapterInterface:
    pass

    def adapt(self, register, variable, reference, tracer):
        pass


class MoveAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        instruction = tracer.execution_dump.instructions.get(reference.ref_next_instruction)
        tracer.tracing_graph[reference] = {}
        try:
            tracer.tracing_graph[reference][instruction.r1].append(variable)
        except KeyError:
            tracer.tracing_graph[reference][instruction.r1] = []
            tracer.tracing_graph[reference][instruction.r1].append(variable)
        try:
            tracer.tracing_graph[reference][register].append(variable)
        except KeyError:
            tracer.tracing_graph[reference][register] = []
            tracer.tracing_graph[reference][register].append(variable)
        tracer.check_after(instruction.modified_register(), variable, instruction)


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        tracer.tracing_graph[reference] = {}
        try:
            tracer.tracing_graph[reference][register].append(variable)
        except KeyError:
            tracer.tracing_graph[reference][register] = []
            tracer.tracing_graph[reference][register].append(variable)


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, reference, tracer):
        instruction = tracer.execution_dump.instructions.get(reference.ref_next_instruction)
        tracer.tracing_graph[reference] = {}
        if instruction.modified_register() != register:
            try:
                tracer.tracing_graph[reference][register].append(variable)
            except KeyError:
                tracer.tracing_graph[reference][register] = []
                tracer.tracing_graph[reference][register].append(variable)
