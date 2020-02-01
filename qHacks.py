'''
qHacks 2020
'''
# import libraries
import os
from random import randint

from google.cloud import language
from google.cloud.language import types,enums


class convo:

    def __init__(self):
        questionLis = ["What is on your mind?", "How are you feeling today?", "If you could do one thing today what would it be?" , "What do you plan on doing today?", "Fill in question" ]
        self.api_client = language.LanguageServiceClient()
        self.questions = questionLis  # list of questions
        self.response = []
        self.sScore = 0  # range of +-0.25 on google sentiment analysis

    def ask(self):
        i = randint(0, len(self.questions) - 1)  # ask a random question from the list of questions

        question = self.questions[i]

        print(question)  # googleTextToSpeech()replace with display and google speech GOOOOOOOOOOOOGLE

        self.questions.remove(question)

    def reply(self, response):
        self.response.append(response)

    def getScore(self):
        temp = 0
        for i in self.response:
            document = types.Document(
                content = i,
                type=enums.Document.Type.PLAIN_TEXT)
            annotations = self.api_client.analyze_sentiment(document = document)
            #print(annotations)
            temp += annotations.document_sentiment.score
        sScore = temp / len(self.response)
        print (sScore)
        return sScore
    def print_responses(self):
        print(self.response)

#need function to generate recommendations to improve mood!!!!!!!!!!!!

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/juliapuistonen/Documents/qHacks/nodal-alcove-265318-9c7023a7e9c1.json"
    # if possible find a way to get name on first access and store
    appOpen = True
    Name = "Julia"
    print("Hey", Name, "!")

    while appOpen:
        new_Convo = convo()

        for x in range(0,1):
            new_Convo.ask()
            storeResponse = input("Response: ")
            new_Convo.reply(storeResponse)
        mood = new_Convo.getScore()

        appOpen = False


main()