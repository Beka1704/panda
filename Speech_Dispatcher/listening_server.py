#!/usr/bin/env python

from pocketsphinx import *
from sphinxbase import *

import os
import pyaudio
import wave
import audioop
from Speech_Dispatcher.utils import mapping_reader
from collections import deque
import time
import math

import pkg_resources

from Speech_Dispatcher import intent_dispatcher

"""
Written by Sophie Li, 2016
http://blog.justsophie.com/python-speech-to-text-with-pocketsphinx/
"""

class SpeechDetector:
    model_tuning = False

    def __init__(self, intent_dispatcher):
        self.dispatcher = intent_dispatcher
        # Microphone stream config.
        self.CHUNK = 8192  # CHUNKS of bytes to read each time from mic
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000

        self.SILENCE_LIMIT = 2 # Silence limit in seconds. The max ammount of seconds where
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
       # MODELDIR = "/home/benjamin/PocketPy/Corpus"


        MODELDIR = pkg_resources.resource_filename(__name__, "/Corpus/")
        #fileDir = os.path.dirname(os.path.realpath('__file__'))
        #MODELDIR = fileDir+"/Corpus/"
        #print(fileDir)
        #DATADIR = "/home/pi/pocketsphinx-5prealpha/test/data"
        
        # Create a decoder with certain model
        INTENTMODELDIR = pkg_resources.resource_filename(__name__,"/Corpus/Calendar")
        self.config_calendar = Decoder.default_config()
        self.config_calendar.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        self.config_calendar.set_string('-lm', os.path.join(INTENTMODELDIR, 'model.lm'))
        self.config_calendar.set_string('-dict', os.path.join(INTENTMODELDIR, 'dictionary.dic'))
        #<property name="logLevel" value="WARNING"/
        self.config_calendar.set_string('-logfn', '/dev/null')
        #config.set_string('-dict', os.path.join(DICDIR, 'en-us/cmudict-en-us.dict'))

        # birthday files 5389
        INTENTMODELDIR = pkg_resources.resource_filename(__name__,"/Corpus/Birthday")
        self.config_birthday = Decoder.default_config()
        self.config_birthday.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        self.config_birthday.set_string('-lm', os.path.join(INTENTMODELDIR, 'model.lm'))
        self.config_birthday.set_string('-dict', os.path.join(INTENTMODELDIR, 'dictionary.dic'))
        self.config_birthday.set_string('-logfn', '/dev/null')
                # birthday files 5389
        INTENTMODELDIR = pkg_resources.resource_filename(__name__,"/Corpus/RNV")
        self.config_rnv = Decoder.default_config()
        self.config_rnv.set_string('-hmm',os.path.join(MODELDIR, 'en-us'))
        self.config_rnv.set_string('-lm', os.path.join(INTENTMODELDIR, 'model.lm'))
        self.config_rnv.set_string('-dict', os.path.join(INTENTMODELDIR, 'dictionary.dic'))
        #self.config_rnv.set_string('-logfn', '/dev/null')

        self.config_hotword = Decoder_default_config()
        HOTMODELDIR = pkg_resources.resource_filename(__name__,"/Corpus/Hotword")
        self.config_hotword = Decoder.default_config()
        self.config_hotword.set_string('-hmm', os.path.join(MODELDIR, 'en-us'))
        self.config_hotword.set_string('-dict',  os.path.join(HOTMODELDIR, 'dictionary.dic'))
        self.config_hotword.set_string('-lm', os.path.join(HOTMODELDIR, 'model.lm'))
        self.config_hotword.set_string('-kws', 'panda.list')
        #self.config_hotword.set_string('-logfn', '/dev/null')
        

        
        
        
        #self.config_hotword.set_string('-hmm',os.path.join(MODELDIR, 'en-us'))
        #self.config_hotword.set_string('-lm', os.path.join(HOTMODELDIR, 'model.lm'))
        #self.config_hotword.set_string('-dict', os.path.join(HOTMODELDIR, 'dictionary.dic'))
        #self.config_hotword.set_string('-logfn', '/dev/null')
        #self.config_hotword.set_string('-keyphrase', 'Panda')

        

        # Creaders decoder object for streaming data.
        self.decoder_calendar = Decoder(self.config_calendar)
        self.decoder_birthday = Decoder(self.config_birthday)
        self.decoder_rnv = Decoder(self.config_rnv)

        self.decoder_hotword = Decoder(self.config_hotword)
        
        #self.decoders = {'calendar':self.decoder_calendar, 'birthday':self.decoder_birthday, 'rnv':self.decoder_rnv}
        self.decoders = {'CALENDAR':self.decoder_calendar,'BIRTHDAY':self.decoder_birthday, 'RNV':self.decoder_rnv}
        self.p = pyaudio.PyAudio()
        self.setup_mic()

        mappingpath = pkg_resources.resource_filename(__name__, 'hotword_intent_mapping.csv')
        self.keyword_intent_mapping = mapping_reader.read_hotword_mapping(mappingpath)
        pass

    def setup_mic(self, num_samples=15):
        """ Gets average audio intensity of your mic sound. You can use it to get
            average intensities while you're talking and/or silent. The average
            is the avg of the .2 of the largest intensities recorded.
        """
        print ("Getting intensity values from mic.")
        
        stream = self.p.open(format=self.FORMAT, 
                        channels=self.CHANNELS,
                        rate=self.RATE, 
                        input=True, 
                        frames_per_buffer=self.CHUNK)
        num_samples = 10

        values = [math.sqrt(abs(audioop.avg(stream.read(self.CHUNK), 4)))
                  for x in range(num_samples)]
        values = sorted(values, reverse=True)
        r = sum(values[:int(num_samples * 0.2)]) / int(num_samples * 0.2)
        print (" Finished ")
        print (" Average audio intensity is ", r)
        time.sleep(2)
        stream.close()
        #self.p.terminate()

        if True: # r < 3000:
            self.THRESHOLD = r+1500
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

    def search_hotword_phrase(self, wav_file):
        decoder = self.decoder_hotword
        stream = open(wav_file, "rb")
        logmath = decoder.get_logmath()

        decoder.start_utt()
        while True:
            buf = stream.read(10024)
            if buf:
                decoder.process_raw(buf, False, False)
            else:
                break
        decoder.end_utt()
        if decoder.hyp() != None:
            words = []
            for seg in decoder.seg():
                words.append(seg.word)
                if self.model_tuning: 
                    print(seg.word)
                    print(seg.prob)
        else:
            return None
        words = [x.strip(' ') for x in words]
        
        if('PANDA' in words):
            for hw in self.keyword_intent_mapping.keys():
                if hw.upper() in words: return self.keyword_intent_mapping[hw]
        print ("Detected keyphrase, restarting search")
        



    def decode_phrase(self, wav_file, decoder):
        decoder.start_utt()
        stream = open(wav_file, "rb")
        while True:
          buf = stream.read(14024)
          if buf:
            decoder.process_raw(buf, False, False)
          else:
            break
        decoder.end_utt()
        stream.close()
        words = []
        [words.append(seg.word) for seg in decoder.seg()]

        hypothesis = decoder.hyp()
        logmath = decoder.get_logmath()
        if(self.model_tuning and hypothesis is not None):
            print ('Best hypothesis: ', hypothesis.hypstr, " model score: ", hypothesis.best_score, " confidence: ", logmath.exp(hypothesis.prob))

            #print ('Best 20 hypothesis: ')
            #sum = 0
            #for best, i in zip(decoder.nbest(), range(10)):
            ##    print (best.hypstr, best.score, logmath.exp(best.prob))
            #    sum += best.score
            #print(sum)
            wait = input("Hit some keys")
        if hypothesis is None:
            return 0.0, "", ""
        best_score = 0
        #for best, i in zip(decoder.nbest(), range(1)):
        #    if not best.hypstr == 'None':
        #        best_score += best.score
        return logmath.exp(hypothesis.prob), words, hypothesis.hypstr

    def run(self):
        """
        Listens to Microphone, extracts phrases from it and calls pocketsphinx
        to decode the sound
        """
        #self.setup_mic()

        #Open stream
        #self.p = pyaudio.PyAudio()
        stream = self.p.open(format=self.FORMAT, 
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

            elif started and time.time()-start > 2.0:
                stream.stop_stream()

                #stream.close()
                print ("Finished recording, decoding phrase")
                filename = self.save_speech(list(prev_audio) + audio2send, self.p)
                hotword = self.search_hotword_phrase(filename) 
                if hotword is not None:
                    decoder = self.decoders[hotword.upper()]
                    c,r,h = self.decode_phrase(filename, decoder)
                    #candidates[c] = h
                    #print(str(key)+":"+str(c)+" "+h)
                    #print ("DETECTED: ", str(candidates[max(candidates, key=float)]))
                    #input('Hit some key!')
                    self.dispatcher.dispatch(h)

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
        self.p.terminate()

#if __name__ == "__main__":
#    from multiprocessing import Queue
#    sd = SpeechDetector(intent_dispatcher.intent_dispatcher(Queue()))
#    sd.run()
    #parent_conn, child_conn = Pipe()