from multiprocessing import Process, Queue


from Speech_Dispatcher import intent_dispatcher
from Speech_Dispatcher import listening_server
from Kivy_App import mainApp

dis_to_app = Queue()
app_to_diss = Queue()

dis = intent_dispatcher.intent_dispatcher(dis_to_app,app_to_diss)
server = listening_server.SpeechDetector(dis)
app = mainApp.AssistantFrame(inbound=dis_to_app, outbound=app_to_diss)

p1 = Process(target=app.run)
p2 = Process(target=server.run)
p1.start()
#p2.start()
#app.run()
server.run()
