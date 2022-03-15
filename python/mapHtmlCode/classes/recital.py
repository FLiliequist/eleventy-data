class Recital:
    def __init__(self, startLine, id) -> None:
        self.startLine = startLine
        self.endLine = 0
        self.content = ''
        self.id = id
    
    def addContent(self, value):
        self.content += str(value)
    def __str__(self) -> str:
        return f'{self.startLine} {self.endLine}, {self.content}'