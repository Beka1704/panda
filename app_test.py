from multiprocessing import Process, Queue


from Speech_Dispatcher import intent_dispatcher
from Speech_Dispatcher import listening_server
from Kivy_App import mainApp

dis_to_app = Queue()
app_to_diss = Queue()

dis = intent_dispatcher.intent_dispatcher(dis_to_app,app_to_diss)
#server = listening_server.SpeechDetector(dis)
app = mainApp.AssistantFrame(inbound=dis_to_app, outbound=app_to_diss)
app.run()
