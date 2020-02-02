'''
qHacks 2020
'''
# import libraries
import os
#import pyaudio
#import wave
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

#from __future__ import division

import re
import sys

from pygame import mixer
from random import randint
from datetime import datetime

from google.cloud import language
from google.cloud.language import types, enums 
from google.cloud import texttospeech

import speech_recognition as sr

from google.cloud import speech
from google.cloud.speech import types as tps 
from google.cloud.speech import enums as enm

from six.moves import queue
import pyaudio

history = []
game_links = ["https://findtheinvisblecow.com/"]
playlist_links = ["https://open.spotify.com/playlist/37i9dQZF1DX3rxVfibe1L0","https://open.spotify.com/playlist/37i9dQZF1DXdPec7aLTmlC",
                "https://open.spotify.com/playlist/1llkez7kiZtBeOw5UjFlJq",]
video_links = ["https://www.youtube.com/watch?v=ZmOvNQu1YVw","https://www.youtube.com/watch?v=rC58kVFT1rA","https://www.youtube.com/watch?v=qxJU4PYuNP0",
            "https://www.youtube.com/watch?v=2aK8hy50fS4","https://www.youtube.com/watch?v=hZyJ-rMyTKk","https://open.spotify.com/playlist/37i9dQZF1DX0UrRvztWcAU",
            "https://open.spotify.com/playlist/3d67ufMEJnDAd8PBsVBF8m"]
meme_links=["https://9gag.com/funny","https://bestlifeonline.com/funniest-memes-all-time/"]


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    """Opens a recording stream as a generator yielding the audio chunks."""
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        # Create a thread-safe buffer of audio data
        self._buff = queue.Queue()
        self.closed = True

    def __enter__(self):
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            # The API currently only supports 1-channel (mono) audio
            # https://goo.gl/z757pE
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            # Run the audio stream asynchronously to fill the buffer object.
            # This is necessary so that the input device's buffer doesn't
            # overflow while the calling thread makes network requests, etc.
            stream_callback=self._fill_buffer,
        )

        self.closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self.closed = True
        # Signal the generator to terminate so that the client's
        # streaming_recognize method will not block the process termination.
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        """Continuously collect data from the audio stream, into the buffer."""
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self):
        while not self.closed:
            # Use a blocking get() to ensure there's at least one chunk of
            # data, and stop iteration if the chunk is None, indicating the
            # end of the audio stream.
            chunk = self._buff.get()
            if chunk is None:
                return
            data = [chunk]

            # Now consume whatever other data's still buffered.
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)


def listen_print_loop(responses):
    """Iterates through server responses and prints them.

    The responses passed is a generator that will block until a response
    is provided by the server.

    Each response may contain multiple results, and each result may contain
    multiple alternatives; for details, see https://goo.gl/tjCPAU.  Here we
    print only the transcription for the top alternative of the top result.

    In this case, responses are provided for interim results as well. If the
    response is an interim one, print a line feed at the end of it, to allow
    the next result to overwrite it, until the response is a final one. For the
    final one, print a newline to preserve the finalized transcription.
    """
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        # The `results` list is consecutive. For streaming, we only care about
        # the first result being considered, since once it's `is_final`, it
        # moves on to considering the next utterance.
        result = response.results[0]
        if not result.alternatives:
            continue

        # Display the transcription of the top alternative.
        transcript = result.alternatives[0].transcript

        # Display interim results, but with a carriage return at the end of the
        # line, so subsequent lines will overwrite them.
        #
        # If the previous result was longer than this one, we need to print
        # some extra spaces to overwrite the previous result
        overwrite_chars = ' ' * (num_chars_printed - len(transcript))

        if not result.is_final:
            sys.stdout.write(transcript + overwrite_chars + '\r')
            sys.stdout.flush()

            num_chars_printed = len(transcript)

        else:
            answer = (transcript + overwrite_chars)
            print(answer)


            # Exit recognition if any of the transcribed phrases could be
            # one of our keywords.
            if re.search(r'\b(exit|quit)\b', transcript, re.I):
                print('Exiting..')
                break

            num_chars_printed = 0




class convo:

    def __init__(self):
        questionLis = ["What is on your mind?", "How are you feeling today?", "If you could do one thing today what would it be?",
                        "How's your week been?","How are your friend?", "What do you plan on doing today?", "How would you describe yourself?",
                        "If you could have superpowers, would you use it for good or for evil, and why?","What is your morning routine like?",
                        "What lyrics would describe your life right now?", "What do you think your life will look like in 10 years?",
                        "What do you think your life will look like in 5 years?","What do you think your life will look like next year?"]

        self.api_client = language.LanguageServiceClient()
        self.t2s_client = texttospeech.TextToSpeechClient()
        #self.s2t_client = speech.SpeechClient()

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

        print(question)  

        self.questions.remove(question)

    def reply(self):
        #print("...speak!...")
        #answer  = self.transcribe() 
        answer = input("")
        #print(answer)
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
                j=randint(0,len(game_links))
                result = "Hmm, looks like you're not your best self... Check this game out!"
                self.speak(result)
                print(result)
                print(game_links[j])

            if i == 1:
                j=randint(0,len(playlist_links))
                result = "Time to get your vibe up! Check out this playlist..."
                self.speak(result)
                print(result)
                print(playlist_links[j])
            if i == 2:
                j=randint(0,len(meme_links))
                result="Check out these funky memes!"
                self.speak(result)
                print(result)
                print(meme_links[j])

        elif -0.25<=self.sScore<=0.25:
            result="You seem to be doing alright... Check out this video to boost your vibe!"
            print(result)
            j=randint(0,len(playlist_links))
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
            new_Convo.reply()
        moodScore = new_Convo.getScore()
        new_Convo.recommend()

        date = datetime.now()
        history.append("Date: "+str(date)+" Score: "+str(moodScore))
    
        restart = input("Try again? Enter y to Try again or any other key to see history!")

        if restart != "y":
            appOpen = False

    print("History of your moods")
    print("Scores in range -1 to 1 where 1 is your happiest!")
    for x in range(0,len(history)):
        print(history[x])


main()