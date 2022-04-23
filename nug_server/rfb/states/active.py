from nug_server.core.states import BaseState


class ActiveState(BaseState):
    def handle(self, data: bytes):
        for device in self.context.devices.all():
            device.transport.write(data)
        return self

    def __str__(self) -> str:
        return "active"
