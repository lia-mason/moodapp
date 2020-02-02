'''
qHacks 2020
'''
# import libraries
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
from pygame import mixer
from random import randint

from google.cloud import language
from google.cloud.language import types,enums
from google.cloud import texttospeech
#from google.cloud import speech
#from google.cloud.speech import types,enums


links=["https://findtheinvisblecow.com/"]
class convo:

    def __init__(self):
        questionLis = ["What is on your mind?", "How are you feeling today?", "If you could do one thing today what would it be?" , "What do you plan on doing today?", "Fill in question" ]
        self.api_client = language.LanguageServiceClient()
        self.t2s_client = texttospeech.TextToSpeechClient()
        #self.speech_client = speech.SpeechClient()

        self.questions = questionLis  # list of questions
        self.answers = []
        self.sScore = 0  # range of +-0.25 on google sentiment analysis

    def ask(self):
        i = randint(0, len(self.questions) - 1)  # ask a random question from the list of questions

        question = self.questions[i]
        synthesis_input = texttospeech.types.SynthesisInput(text=question)
        voice = texttospeech.types.VoiceSelectionParams(
            language_code ='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.NEUTRAL)
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = self.t2s_client.synthesize_speech(synthesis_input,voice,audio_config)

        with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
            out.write(response.audio_content)
        mixer.init()
        mixer.music.load('output.mp3')
        mixer.music.play()

        print(question)  # googleTextToSpeech()replace with display and google speech GOOOOOOOOOOOOGLE

        self.questions.remove(question)

    def reply(self, answer):
        #self.speech_client = speech.SpeechClient()

        self.answers.append(answer)


    def getScore(self):
        temp = 0
        for i in self.answers:
            document = types.Document(
                content = i,
                type=enums.Document.Type.PLAIN_TEXT)
            annotations = self.api_client.analyze_sentiment(document = document)
            #print(annotations)
            temp += annotations.document_sentiment.score
        self.sScore = temp / len(self.answers)
        return self.sScore
    
    def print_responses(self):
        print(self.answers)

    def recommend(self):
        score = self.getScore()
        if score < -0.25:
            i = randint(0,2)
            if i==0:
                print("Hmm, looks like your not your beset self... Check this game out!")
                print(links[0])
            if i == 1:
                print("Time to get your vibe up! Check out this playlist...")
                print("https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0")
            if i == 2:
                print("Check out these funky memes!")
                print("Nothing YET!")
        elif -0.25<=score<=0.25:
            print("TO BE DETERMINED") 
        else:
            print("TO BE DETERMINED") 



#need function to generate recommendations to improve mood!!!!!!!!!!!!

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/juliapuistonen/Documents/qHacks/nodal-alcove-265318-9c7023a7e9c1.json"
    #language_code = 'en-US'



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
        new_Convo.recommend()


        appOpen = False


main()