import os
from pocketsphinx import AudioFile, get_model_path, get_data_path
import pkg_resources

model_path = MODELDIR = pkg_resources.resource_filename(__name__, "/Corpus/")
INTENTMODELDIR = pkg_resources.resource_filename(__name__,"/Corpus/Calendar")
data_path = get_data_path()

config = {
    'verbose': False,
    'audio_file': os.path.join(data_path, 'output.wav'),
    'buffer_size': 2048,
    'no_search': False,
    'full_utt': False,
    'hmm': os.path.join(model_path, 'en-us'),
    'lm': os.path.join(INTENTMODELDIR, 'model.bin'),
    'dict': os.path.join(INTENTMODELDIR, 'dictionary.dict')
}
AudioFile.set_search('search name':"keyword")
AudioFile.set_keyphrase("Pandas")

audio = AudioFile(**config)
for phrase in audio:
    print(phrase)