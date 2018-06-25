import os

def say(utterance, language):
    cmd = 'pico2wave -l "'+language+'" -w temp.wav "'+utterance+'"'
    os.system(cmd)
    os.system('aplay temp.wav')
