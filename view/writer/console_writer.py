from view.writer import Writer


class ConsoleWriter(Writer):
    def write(self, data: str):
        print(data)
