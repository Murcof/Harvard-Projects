# Final-Project [Capstone]
This repository contains the final project of Harvards CS50’s Web Programming with Python and JavaScript.
***

### Distinctiveness and Complexity

This application differs in many aspects from all others developed during this course and its previous versions. It has its own database and accesses an API developed by third parties, something not executed in any of the previously delivered projects. The back-end of this application was developed with Django and has the 'Word' model in its database. Actions such as choosing a random page and playing the game in which the user needs to find the name of the word related to the artwork were implemented with JavaScript language. In the CSS file of this project, it can be seen that the arrangement of elements varies according to the orientation of the screen in which the application is being accessed, having different interfaces when it is opened on a Desktop or on a Mobile.

#### Why?

The GRE test requires different knowledge from students. While I was studying, the hardest aspect to learn, as a non native speaker, was the volumous vocabulary present on the verbal part. It was not simple to find material with the most important words and its applications. Furtherly, once I found the words, the memorization proccess was tiresome sometimes. Having a simple and friendly application could have helped me to easily walk this path. 

Moreover, although I was not accepted in any university I applicated, I wanted to generate some value from my efforts and help other students.

#### How?

Compiling in one place, with a simple and friendly interface, words present in the test, in addition to their part of speech, description and possible synonyms. In addition, the application aids learning by stimulating students' visual memory, presenting them with an image of a related art piece for each word in the database. Artwork images are acquired by accessing the Art institute of Chicago's API(artic).
* The API's documentation can be found here: https://api.artic.edu/docs/#quick-start

#### What?

The GRE Words, an application that dynamically centralizes information and helps in the process of memorizing the words that may appear in the test.
***
##### What is contained in files?
* util.py -> The alphabet and a function to search results
* urls.py -> Applications URLs and its API route to random page id
* views.py -> Functions to render each page of this application. Although all the functions in this file are small and intuitive, a note here is valid: the 'game' function always sends the words arranged randomly
* styles.css -> All the styling aspects of the whole application
* index.js -> Functions to random page, game and word search
* aux_page.js -> Functions to random page and word search
* word.js -> Functions to random page, word search and the fetch to the artic's API. Here another note is valid: if atic's API doesn't return a response, this application displays a default image informing the user that no related artpiece was found but presents normally the information in the database.
* game.js -> Functions to random page, word search, the fetch to the artic's API and the game part
* layout.html -> Parts of the layout that change the least
* All other HTML files are referent to each page of the application

##### How to run this application?
This application does not have any requirements different from the other applications in this course in order to work. Having Django and a browser installed on your machine, run the command "python manage.py runserver" in the folder the application is in and it will run. No additional library or software installation required.
