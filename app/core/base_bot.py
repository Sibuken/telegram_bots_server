

class AbstractTelegramBot(object):
    db_class = None

    def __init__(self, data: dict):
        self.data = data

    def resolve_command(self):
        raise NotImplementedError

    def parse_input_data(self):
        raise NotImplementedError

    async def handle(self):
        raise NotImplementedError


class BaseTelegramBot(object):
    HANDLERS = []
