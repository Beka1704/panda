#!/usr/bin/env python

from pocketsphinx import *
from sphinxbase import *

import os
import pyaudio
import wave
import audioop
from collections import deque
import time
import math

"""
Written by Sophie Li, 2016
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
"""

class SpeechDetector:
    def __init__(self):
        # Microphone stream config.
        self.CHUNK = 8192  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 1.5 # Silence limit in seconds. The max ammount of seconds where
                           # only silence is recorded. When this time passes the
                           # recording finishes and the file is decoded
                           
        self.PREV_AUDIO = 6
        #self.PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                          # is detected, how much of previously recorded audio is
                          # prepended. This helps to prevent chopping the beginning
                          # of the phrase.

        self.THRESHOLD = 1000
        self.num_phrases = -1

        # These will need to be modified according to where the pocketsphinx folder is
        MODELDIR = "/home/benjamin/PocketPy/CorpusENUS"
        #DATADIR = "/home/pi/pocketsphinx-5prealpha/test/data"

        # Create a decoder with certain model
        config = Decoder.default_config()
        config.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        config.set_string('-lm', os.path.join(MODELDIR, '8665.lm'))
        config.set_string('-dict', os.path.join(MODELDIR, '8665.dic'))
        #config.set_string('-dict', os.path.join(DICDIR, 'en-us/cmudict-en-us.dict'))

        # Creaders decoder object for streaming data.
        self.decoder = Decoder(config)

    def setup_mic(self, num_samples=50):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the .2 of the largest intensities recorded.
        """
        print ("Getting intensity values from mic.")
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, 
                        channels=self.CHANNELS,
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print (" Finished ")
        print (" Average audio intensity is ", r)
        time.sleep(2)
        stream.close()
        p.terminate()

        if True: # r < 3000:
            self.THRESHOLD = r+1000
        #else:
            #self.THRESHOLD = r + 200

    def save_speech(self, data, p):
        """
        Saves mic data to temporary WAV file. Returns filename of saved
        file
        """
        filename = 'output'#+str(int(time.time()))
        # writes data to WAV file
        data = b''.join(data)
        wf = wave.open(filename + '.wav', 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(16000)  # TODO make this value a function parameter?
        wf.writeframes(data)
        wf.close()
        return filename + '.wav'

    def decode_phrase(self, wav_file):
        self.decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
          buf = stream.read(8192)
          if buf:
            self.decoder.process_raw(buf, False, False)
          else:
            break
        self.decoder.end_utt()
        words = []
        [words.append(seg.word) for seg in self.decoder.seg()]

        hypothesis = self.decoder.hyp()
        logmath = self.decoder.get_logmath()
        print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))

        print ('Best 10 hypothesis: ')
        for best, i in zip(self.decoder.nbest(), range(10)):
            print (best.hypstr, best.score)

        wait = input("Hit some keys")
            
        return words

    def run(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        self.setup_mic()

        #Open stream
        p = pyaudio.PyAudio()
        stream = p.open(format=self.FORMAT, 
                        channels=self.CHANNELS, 
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)
        print ("* Mic set up and listening. ")

        audio2send = []
        cur_data = ''  # current chunk of audio data
        rel = int(self.RATE/self.CHUNK)
        slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
        #Prepend audio from 0.5 seconds before noise was detected
        prev_audio = deque(maxlen=int(self.PREV_AUDIO * rel))
        started = False
        start = float('inf')


        while True:
            #print("In While Loop!")
            cur_data = stream.read(self.CHUNK)
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))

            mx = audioop.max(cur_data, 2)
            #print mx

            

            #print("Current audio itensity is "+intensities+" Threshhold is "+str(self.THRESHOLD))
            #print(slid_win)

            #if sum([x > self.THRESHOLD for x in slid_win]) > 0:
            
            if mx > self.THRESHOLD:
                
                if started == False:
                    print ("Starting recording of phrase")
                    started = True
                    start = time.time()
                audio2send.append(cur_data)

            elif started and int(time.time())- start > 3.0:
                stream.stop_stream()

                #stream.close()
                print ("Finished recording, decoding phrase")
                filename = self.save_speech(list(prev_audio) + audio2send, p)
                r = self.decode_phrase(filename)
                print ("DETECTED: ", r)

                # Removes temp audio file
                os.remove(filename)
                # Reset all
                started = False
                start = float('inf')
                slid_win = deque(maxlen=int(self.SILENCE_LIMIT * rel))
                prev_audio = deque(maxlen=int(0.5 * rel))
                audio2send = []

                #stream = p.open(format=self.FORMAT, 
                #        channels=self.CHANNELS, 
                ##        rate=self.RATE, 
                #        input=True, 
                #        frames_per_buffer=self.CHUNK)


                stream.start_stream()
                print ("Listening ...")

            else:
                prev_audio.append(cur_data)

        print ("* Done listening")
        stream.close()
        p.terminate()

if __name__ == "__main__":
    sd = SpeechDetector()
    sd.run()
