import re
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
class Article:
    def __init__(self, startLine, id) -> None:
        self.startLine = startLine
        self.endLine = 0
        self.content = ''
        self.id = id
        self.title = ''

    def addContent(self, value):
        self.content += str(value)
    def setTitle(self, title):
        self.title = re.sub(CLEANR, '', title).strip()
    def __str__(self) -> str:
        return f'{self.startLine} {self.endLine}, {self.content}, {self.title}'