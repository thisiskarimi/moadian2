import uuid

class PacketHeader():
    def __init__(self, fiscal_id) -> None:
        self.request_trace_id = str(uuid.uuid4())
        self.fiscal_id = fiscal_id

    def build(self) -> str:
        return {
            "requestTraceId": self.request_trace_id,
            "fiscalId": self.fiscal_id
        }


class Packet():
    def __init__(self, payload, fiscalId) -> None:
        self.payload = payload
        self.header = PacketHeader(fiscalId)
    
    def build(self):
        return {
            "payload": self.payload.decode(),
            "header": self.header.build()
        }

