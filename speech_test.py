from multiprocessing import Process, Queue


from Speech_Dispatcher import intent_dispatcher
from Speech_Dispatcher import listening_server


dis_to_app = Queue()
app_to_diss = Queue()

dis = intent_dispatcher.intent_dispatcher(dis_to_app,app_to_diss)
server = listening_server.SpeechDetector(dis)
server.model_tuning = True
server.run()
#Audio_FileTest