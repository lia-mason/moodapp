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


game_links=["https://findtheinvisblecow.com/"]
playlist_links=["https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0","https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                "https://open.spotify.com/playlist/1llkez7kiZtBeOw5UjFlJq",]
video_links=["https://www.youtube.com/watch?v=ZmOvNQu1YVw","https://www.youtube.com/watch?v=rC58kVFT1rA","https://www.youtube.com/watch?v=qxJU4PYuNP0",
            "https://www.youtube.com/watch?v=2aK8hy50fS4","https://www.youtube.com/watch?v=hZyJ-rMyTKk","https://open.spotify.com/playlist/37i9dQZF1DX0UrRvztWcAU",
            "https://open.spotify.com/playlist/3d67ufMEJnDAd8PBsVBF8m"]
meme_links=["https://9gag.com/funny","https://bestlifeonline.com/funniest-memes-all-time/"]

class convo:

    def __init__(self):
        questionLis = ["What is on your mind?", "How are you feeling today?", "If you could do one thing today what would it be?",
                        "How's your week been?","How are your friend?", "What do you plan on doing today?", "How would you describe yourself?",
                        "If you could have superpowers, would you use it for good or for evil, and why?","What is your morning routine like?",
                        "What lyrics would describe your life right now?", "What do you think your life will look like in 10 years?",
                        "What do you think your life will look like in 5 years?","What do you think your life will look like next year?"]

        self.api_client = language.LanguageServiceClient()
        self.t2s_client = texttospeech.TextToSpeechClient()
        #self.speech_client = speech.SpeechClient()

        self.questions = questionLis  # list of questions
        self.answers = []
        self.sScore = 0  # range of +-0.25 on google sentiment analysis

    def speak(self,words):
        synthesis_input = texttospeech.types.SynthesisInput(text=words)
        voice = texttospeech.types.VoiceSelectionParams(
            language_code ='en-US',
            ssml_gender=texttospeech.enums.SsmlVoiceGender.MALE)
        audio_config = texttospeech.types.AudioConfig(
            audio_encoding=texttospeech.enums.AudioEncoding.MP3)
        response = self.t2s_client.synthesize_speech(synthesis_input,voice,audio_config)
        with open('output.mp3', 'wb') as out:
        # Write the response to the output file.
            out.write(response.audio_content)
        mixer.init()
        mixer.music.load('output.mp3')
        mixer.music.play()

    def ask(self):
        i = randint(0, len(self.questions) - 1)  # ask a random question from the list of questions

        question = self.questions[i]
        self.speak(question)

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
        if self.sScore < -0.25:
            i = randint(0,2)
            if i == 0:
                j=randint(0,len(game_links)-1)
                result = "Hmm, looks like you're not your best self... Check this game out!"
                self.speak(result)
                print(result)
                print(game_links[j])

            if i == 1:
                j=randint(0,len(playlist_links)-1)
                result = "Time to get your vibe up! Check out this playlist..."
                self.speak(result)
                print(result)
                print(playlist_links[j])
            if i == 2:
                j=randint(0,len(meme_links)-1)
                result="Check out these funky memes!"
                self.speak(result)
                print(result)
                print(meme_links[j])

        elif -0.25<=self.sScore<=0.25:
            result="You seem to be doing alright... Check out this video to boost your vibe!"
            print(result)
            j=randint(0,len(playlist_links)-1)
            print(video_links[j])
            self.speak(result)

        elif self.sScore>0.25:
            result="You seem to be doing great! Keep up your positive vibe!"
            print(result)
            self.speak(result)
        else:
            result="Error: OUT OF RANGE"
            print("Error: OUT OF RANGE") 
            self.speak(result)



#need function to generate recommendations to improve mood!!!!!!!!!!!!

def main():
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="nodal-alcove-265318-9c7023a7e9c1.json"
    #language_code = 'en-US'



    # if possible find a way to get name on first access and store
    appOpen = True
    Name = "Julia"
    print("Hey", Name, "!")
    while appOpen:
        new_Convo = convo()
        for x in range(0,4):
            new_Convo.ask()
            storeResponse = input("Response: ")
            new_Convo.reply(storeResponse)
        moodScore = new_Convo.getScore()
        new_Convo.recommend()

        restart = input("Response: 1 for more questions, 0 for no")
        if restart == "0":
            appOpen = False


main()