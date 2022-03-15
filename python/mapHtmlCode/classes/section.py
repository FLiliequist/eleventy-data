import re
CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
class Section:
    def __init__(self, startLine) -> None:
        self.startLine = startLine
        self.endLine = 0
        self.title = ''
        self.articles = []

    def addArticle(self, article):
        self.articles.append(article)
    def setTitle(self, title):
        self.title = re.sub(CLEANR, '', title).lstrip().replace('\n','')