# GRAS
## Generating Recipes with an Algorithmic Sensibility
### ("Gras" means fat in french)

Tool that generates recipes with machine learning techniques. The learning is done on recipes from the french website
marmiton.org. Why? Because when it comes to food, french is always the answer. ;)

This is a project done at the Universidad Nacional de Colombia for the Machine Learning class during my exchange semester. This is was my first confrontation with generative models, and I am really happy to have get a foothold on that really exciting field.

You can find on the repo the pdf of the **article** and the **poster** of the presentation of the project. I am sorry, these documents are in spannish...


This is a project done in 1 week approximately, so I didn't have the time to push it as much as I would like to and would need to be improved in many ways:
- The method used for recipe generation is using a probabilistic model and is quite long to execute. We should try other techniques, like the Adversarial networks described in a reference below.
- The method used for title generation could be improved.
- Adding the instructions generation (which requires quite a lot of work to be coherent).
- Make the code cleaner, more readable and more integrated. For now, each part is independent, and not all of them are used. Some of them are just technique tests. It would be good to refactor everything to integrate it in a complete pipeline.
- And maybe many more...



REFs: (you can find others/more on the article)
https://openai.com/blog/generative-models/
https://github.com/fagonzalezo/dl_tutorial_upv/blob/gh-pages/LSTMs_Language_Modeling.ipynb
https://arxiv.org/abs/1406.2661
http://cs229.stanford.edu/notes/cs229-notes2.pdf

