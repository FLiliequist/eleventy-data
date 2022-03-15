import re, json
from classes.chapter import Chapter
from classes.article import Article
from classes.recital import Recital
from classes.section import Section

def readFile(file):
    """
    Argument: 'file' path, type string. \n
    Reads data from file and returns a list 
    with each line in in a seprate element.
    """
    f = open(file, 'r')
    lines = []
    for line in f:
        #Remove uncesseary div tags
        if re.search('<div class=".*">|<\/div>', line) == None:
            lines.append(line)
    f.close()
    return lines


def mapText(lines):
    """
    Arguments: 'lines' list of strings.\n
    Will loop over the html code and try to map each needed line.\n
    Creates a object for each Chapter, Section and Article.
    """
    chapters, sectinos ,articles, recitals = [], [], [], []
    lineCounter, recitleCounter, articleCounter = 0, 0, 0
    CLEANR = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')

    for line in lines:
        if re.search('CHAPTER (M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))', line):
            try:
                # Sets the end line for the previous object.
                chapterObj.endLine = lineCounter - 1
            except UnboundLocalError:
                #The first object will trigger this.
                pass
            chapterObj = Chapter(lineCounter, line)
            chapters.append(chapterObj)
            chapterObj.addTitle(lines[lineCounter + 3])

            tempTitleLineNr = lineCounter

        elif re.search('SECTION (M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3}))', line):
            try:
                sectionObj.endLine = lineCounter - 2
            except UnboundLocalError:
                #The first object will trigger this.
                pass
            
            sectionObj = Section(lineCounter - 1)

            # If the third next row have 'Article [0-9]', then it means
            # that the section does not have a section name. 
            # So then i call the section 'Section I' or 'Section II'
            # Else the Section name is on the third next row.
            if re.search('Article [0-9]', lines[lineCounter + 3]):
                sectionObj.setTitle(line)
            else:
                sectionObj.setTitle(lines[lineCounter + 3])

            sectinos.append(sectionObj)
            chapterObj.hasSections = True
            chapterObj.addSection(sectionObj)

        elif re.search('<span>( |)Article <\/span><span>[0-9].<|<span>( |)Article [0-9](.|)(<| <)', line):
        # Need to do regex because the htmlcode does not follow a standard
            articleCounter += 1
            try:
                articleObj.endLine = lineCounter - 1
            except UnboundLocalError:
                #The first object will trigger this.
                pass

            articleObj = Article(lineCounter, articleCounter)
            chapterObj.addArticle(articleObj)
            
            # This is for Chapter titles that are on 2 rows.
            # tempTitleLineNr is the line where the current chapter started.
            # if lineCounter - tempTitleLineNr == 9 and that the previous third row does
            # not contain 'SECTION' then it means there is
            # a 2 rowed title.
            # The second row title is on the current - 3 row.
            if lineCounter - tempTitleLineNr == 9 and re.search('SECTION', lines[lineCounter - 3]) == None:
                chapterObj.addTitle(lines[lineCounter - 3])

            # Need to do this because of no standard in html code.
            # Often the Article title is in its own <p> tag that is 3 row under
            # but sometimes its in the same <p> tag then its 2 row under. 
            if re.search('Titrearticle', lines[lineCounter + 2]):
                articleObj.setTitle(lines[lineCounter + 3])
            else:
                articleObj.setTitle(lines[lineCounter + 2])

            # Have a try/catch here because each chapter does not have sections.
            try:
                sectionObj.addArticle(articleObj)
            except UnboundLocalError:
                pass
            articles.append(articleObj)
            
        elif re.search('<p class="li ManualConsidrant">', line):
        # This is for the recitals.
            try:
                recitalObj.endLine = lineCounter
            except UnboundLocalError:
                pass
            recitleCounter += 1
            recitalObj = Recital(lineCounter + 1, recitleCounter)
            recitals.append(recitalObj)

        lineCounter += 1
    # Manual sets the endlines for each type,
    # dont know if there is any better way.
    recitals[-1].endLine = 669
    chapters[-1].endLine = 3008
    articles[-1].endLine = 3008
    sectinos[-1].endLine = 3008

    articles = addContent(articles, lines)
    recitals = addContent(recitals, lines)

    createJson(articles, chapters, recitals)

def addContent(objects, content):
    """
    Arguments: 'objects', type list of objects. 'content' list of strings.\n
    Adds content to object.
    """
    for obj in objects:
        for lineNr in range(obj.startLine - 1, obj.endLine):
            obj.addContent(content[lineNr])
    return objects

def createJson(articles, chapters, recitals):
    # These are the lists that will be written to the json files.
    jsonArtList, jsonRecitalList, jsonChapterList = [], [], []

    for article in articles:
        text = article.content

        # Each first article in every chapter gets some ChapterTitle data,
        # that should not be in the article text. This is a fix to remove that data.
        if re.search('<p (id=".*") class="ChapterTitle">', text):
            text = re.split('<p (id=".*") class="ChapterTitle">', text)
        else:
            text = re.split('class="ChapterTitle">', text)
        text = re.split('class="SectionTitle">', text[0])
        articleData = {
            'id': article.id,
            'name': 'article-' + str(article.id),
            'text': text[0]
        }
        jsonArtList.append(articleData)
    
    for recital in recitals:
        recitalData = {
            'id': recital.id,
            'text': recital.content
        }
        jsonRecitalList.append(recitalData)

    for chapter in chapters:
        # This is a mess
        sections = []

        if chapter.hasSections == True:
            
            # Sections in a chapter
            for section in chapter.sections:
                sectionArticles = []

                # Articles in a section in a chapter
                for sectionArticle in section.articles:
                    articleData = {
                        'id': sectionArticle.id,
                        'name': sectionArticle.title
                    }                    
                    sectionArticles.append(articleData)
                
                sectionData = {
                    'title': section.title,
                    'articles': sectionArticles
                }
                sections.append(sectionData)
        else:
            # If chapter dont have section
            
            # Temp list just to get the same strutcure in the json 
            dummySectionArticles = []

            # Articles in chapter
            for article in chapter.articles:
                articleData = {
                    'id': article.id,
                    'name': article.title
                }
                dummySectionArticles.append(articleData)

                # Leaving the title empty because this is not a section.
                sectionData = {
                    'title': '',
                    'articles': dummySectionArticles
                }

            sections.append(sectionData)
        chapterData = {
            'id': chapter.id,
            'title': chapter.title,
            'sections': sections
        }
        jsonChapterList.append(chapterData)

    writeToFile('articles.json', jsonArtList)
    writeToFile('recitals.json', jsonRecitalList)
    writeToFile('chapters.json', jsonChapterList)

def writeToFile(filename, content):
    path = '.eleventy/_data/' + filename
    f = open(path, 'w')
    jsonStr = json.dumps(content)
    f.write(jsonStr)
    f.close()

def main():
    htmlCode = '.python/getHtmlCode/htmlCode.html'
    content = readFile(htmlCode)
    mapText(content)

main()
