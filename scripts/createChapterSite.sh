#! /bin/bash
echo 'Removing old content...'
rm -rf ../eleventy/chapters ../eleventy/articles
echo 'Creating new content folders...'
mkdir ../eleventy/chapters ../eleventy/articles
chapters=$(ls ../doraData/)


echoToFile () {
    echo """
$1
""" >> $2
}
createSiteMd (){
    echo """---
layout: layouts/$1
title: $2
description: $3
permalink: $4
---
$5
$6
""" >> $7
}

for chapter in $chapters
do
    chapterContent=$( ls ../doraData/$chapter/)
    fileChapter=../eleventy/chapters/$chapter.md
    chapterTitle=$( cat ../doraData/$chapter/chapterInfo.txt ) 
    touch $fileChapter
    echo """---
layout: layouts/chapter.njk
title: $chapter
description: $chapterTitle
---
""" >> $fileChapter

    for article in $chapterContent
    do
        if [[ $article =~ "SECTION-I" ]]; then
            echoToFile $article $fileChapter
            articles=$(ls ../doraData/$chapter/$article/ | sort -V )
            for subArticle in $articles
            do
                echoToFile "<a href="$subArticle">$subArticle</a>" $fileChapter
                pathToArticle="../doraData/$chapter/$article/$subArticle"

                targetPath="../eleventy/articles/$subArticle.md"
                permalink="chapters/$chapter/$subArticle/"
                articleTitle=$(head -n1 $pathToArticle)
                articleContent=$(tail -n +2 $pathToArticle)
                : '
                Me trying to get some linebreaks in the HTML code
                articleContent=$(echo $articleContent | sed -e "s/\:/: <br>/")
                articleContent=$(echo $articleContent | sed -e "s/\;/; <br>/")
                articleContent="${$articleContent/'\n'/<br>\n}"
                sed -e "s/\$articleContent/\n/<br>\n/g" "$articleContent"
                articleContent=$(sed -i "s/$articleContent/\n/<br>\n/g" "$articleContent")
                '
                createSiteMd 'article.njk' $subArticle $subArticle $permalink "$articleTitle" "$articleContent" $targetPath

            done
        elif [[ $article =~ "Article-" ]]; then
            pathToArticle="../doraData/$chapter/$article"
            targetPath="../eleventy/articles/$article.md"

            permalink="chapters/$chapter/$article/"
            articleTitle=$(head -n1 $pathToArticle)
            articleContent=$(tail -n +2 $pathToArticle)
            
            echoToFile "<a href="$article">$article - $articleTitle</a>" $fileChapter
            createSiteMd 'article.njk' $article $article $permalink "$articleTitle" "$articleContent" $targetPath
        fi
        if [ $article = 'chapterInfo.txt' ]; then
            break
        fi
    done
done

echo '''{
  "tags": "articles"
}''' >> ../eleventy/articles/articles.json
echo '''{
  "tags": "chapters"
}''' >> ../eleventy/chapters/chapters.json