#! /bin/bash
echo 'Removing old content...'
rm -rf ../eleventy/chapters
echo 'Creating new chapters folder...'
mkdir ../eleventy/chapters
chapters=$(ls ../doraData/)

echoToFile () {
    echo """
$1
""" >> $2
}

for chapter in $chapters
do
    echo $chapter
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
                echo $subArticle
                echoToFile "<a href="$subArticle">$subArticle</a>" $fileChapter
            done
        elif [[ $article =~ "Article-" ]]; then
            echoToFile "<a href="$article">$article</a>" $fileChapter
        fi
        if [ $article = 'chapterInfo.txt' ]; then
            break
        fi
    done
done


echo '''{
  "tags": "chapters"
}''' >> ../eleventy/chapters/chapters.json