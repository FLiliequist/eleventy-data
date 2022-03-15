import re
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

class Chapter:
    def __init__(self, startLine, id) -> None:
        self.startLine = startLine
        self.endLine = 0
        self.articles = []
        self.sections = []
        self.hasSections = False
        self.title = ''
        self.id = re.sub(CLEANR, '', id).lstrip().replace('\n','')

    def addTitle(self, title):
        title = re.sub(CLEANR, '', title)
        self.title += title.replace('\n','').upper().strip()
    def addSection(self, seciton):
        self.sections.append(seciton)
    def addArticle(self, article):
        self.articles.append(article)

    def __str__(self) -> str:
        return f'{self.startLine} {self.endLine} |{self.title}| {self.id}'