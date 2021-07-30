from abc import ABC, abstractmethod
"""
this interface handle the tracing after a specific type of instruction
"""


class AdapterInterface(ABC):
    pass

    @abstractmethod
    def adapt(self, register, variable, index, tracer):
        pass


class MoveAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, index, tracer):
        pass


class ReadOnlyAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, index, tracer):
        pass


class WriteAdapter(AdapterInterface):
    pass

    def adapt(self, register, variable, index, tracer):
        pass
