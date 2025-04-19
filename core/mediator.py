from typing import Type, Any, Dict, Callable


class Mediator:
    def __init__(self):
        self.handlers: Dict[Type, Callable] = {}

    def register_handler(self, message_type: Type, handler: Callable):
        self.handlers[message_type] = handler

    async def send(self, message: Any, **kwargs) -> Any:
        handler = self.handlers.get(type(message))
        if not handler:
            raise ValueError(f"No handler registered for {type(message)}")
        # On passe les arguments supplémentaires au handler
        return await handler(message, **kwargs)


mediator = Mediator()
