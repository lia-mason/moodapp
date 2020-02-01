'''
qHacks 2020
'''
# import libraries
from random import randint


class convo:

    def __init__(self):
        questionLis = ["What is on your mind?", "How are you feeling today?", "If you could do one thing today what would it be?" , "What do you plan on doing today?", "Fill in question" ]

        self.questions = questionLis  # list of questions
        self.response = []
        self.sScore = 0  # range of +-0.25 on google sentiment analysis
        self.askingPeriod = False

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
            temp += 0  # googleSentiment(i) GOOOOOOOOOOOOOOOOOGLE
        sScore = temp / len(self.response)
        return sScore
    def print_responses(self):
        print(self.response)

def main():
    # if possible find a way to get name on first access and store
    appOpen = True
    Name = "Julia"
    print("Hey", Name, "!")

    while appOpen:
        new_Convo = convo()

        for x in range(0,5):
            new_Convo.ask()
            storeResponse = input("Response: ")
            new_Convo.reply(storeResponse)
        appOpen = False


main()
