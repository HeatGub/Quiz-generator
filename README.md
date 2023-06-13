# Quiz generator (django + AJAX + GPTchat)
## Overview
- Backend - django, AJAX and GPTchat API to generate quizes
  - relational DB
  - asynchronous reading and saving of the highscore value 
  - extended admin page with nested lists

- Frontend - HTML, CSS, vanilla JS
  - works quite well on lower resolution devices

You can find it hosted at https://quizgenerator.pythonanywhere.com/. 
Git version does not contain personal keys needed to run the website locally.

Warning: Because my harddrive suddenly broke, I lost the credentials to OPENAI account, therefore my API key might expire soon. If so, you'll see a message to try again later and won't be able to generate a quiz. Good news is that you may always choose already generated quiz from the highscores instead.

## Generate
Generate a quiz based on form input values (topic, time limit, GPT temperature, amounts of questions and answers)

<!-- MY NOTE: DROP A PICTURE HERE TO GET ITS URL. PASTE THE URL INTO HTML img AS BELOW -->
<!-- ![Screenshot from 2023-06-10 20-40-20](https://github.com/HeatGub/Quiz-generator/assets/115884941/b23af63a-5a48-4504-8156-896c57ece92b) -->
<p align="center">
  <img src="https://github.com/HeatGub/Quiz-generator/assets/115884941/b23af63a-5a48-4504-8156-896c57ece92b" width=60% height=60%>
</p>

Generated quiz looks like this:

<p align="center">
  <img src="https://github.com/HeatGub/Quiz-generator/assets/115884941/7733a3b3-4398-4a45-a871-1f2e7a36331c" width=60% height=60%>
</p>

It's GPT 3.5 (text-davinci-003) so it bases on the training set which is already outdated (up to Jun 2021).
If it won't know much about the topic it will make it up, thus I do not guarantee that the quizzes are in line with reality.

## Beat the highscore
If you earn enough points, you can overwrite current highscore with your nickname (asynchronously - AJAX)

<p align="center">
  <img src="https://github.com/HeatGub/Quiz-generator/assets/115884941/cf813561-25b2-4626-94fd-97658c98a767" width=60% height=60%>
</p>

You can check the table of generated quizes, ordered by the score (highscores) to compare your results. Hover over the table header's name to see detailed description.

<p align="center">
  <img src="https://github.com/HeatGub/Quiz-generator/assets/115884941/f9c0740b-af59-4dad-a121-69fe90406189" width=60% height=60%>
</p>

## Admin page
Here you can see a list of all the generated quizes (or - potentially - generation requests which went wrong with the whole response text).

![Screenshot from 2023-06-13 18-07-37](https://github.com/HeatGub/Quiz-generator/assets/115884941/d936fc66-b95d-4fc2-a30b-56486971f69b)

When you enter a single quiz from that list, you get more details. 

You can see a nested list implemented here for better control and overview of questions and answers from the admin page.
![Screenshot from 2023-06-13 19-02-20](https://github.com/HeatGub/Quiz-generator/assets/115884941/84678ee6-ee2b-4865-b208-95bda5b2fee2)

That's all folks. Go and solve a quiz now ;)
