'''
qHacks 2020
'''
#import libraries
from random import randint

q = ["How are you?", "What are you doing today?"]

class convo:
    def _init_(self,questions,response, sScore):
        self.questions = q #list of questions
        self.response = []
        self.sScore = 0 # range of +-0.25 on google sentiment analysis
        

    def ask(self):
        i = randint(0,len(q)-1) #ask a random question from the list of questions
        print(questions[i]) #googleTextToSpeech()replace with display and google speech GOOOOOOOOOOOOGLE

    def reply(self):
        speech = "This is the input from google speech to text"
        self.response.append(speech)

    def getScore(self):
        temp = 0
        for i in self.response:
             temp += 0#googleSentiment(i) GOOOOOOOOOOOOOOOOOGLE
        sScore = temp/len(response)
        return sScore



#if possible find a way to get name on first access and store
appOpen = True
Name = "Julia"
print("Hey",Name,"!")

while appOpen:
    
    newConvo= convo()



        

