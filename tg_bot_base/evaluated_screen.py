from .message import Message

class EvaluatedScreen:
    def __init__(self, *messages: Message):
        self.messages: list[Message] = []
        self.extend(messages)
    
    def extend(self, messages: list[Message]):
        self.messages.extend(messages)
    
    def clone(self) -> "EvaluatedScreen":
        return EvaluatedScreen(*[message.clone() for message in self.messages])
    
    def __repr__(self):
        return f"EvaluatedScreen({",".join([str(message) for message in self.messages])})"
    