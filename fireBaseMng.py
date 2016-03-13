import threading
from firebase import firebase

userUrl = 'https://hackalexa.firebaseio.com'
repoName = '/test/'
tableUrl = userUrl + repoName


existVisitorVar = 'existVisitor'
toPlayVideoVar = 'playVideo'
lastTimeVisitedVar = 'lastTimeVisited'
numOfVisitorsVar = 'numOfVisitors'
playIndexVar = 'playIndex'
# askExistVisitorPeriod
# askExistVisitorFrom
# askExistVisitorTo

class FireBaseMng(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.threadLock = threading.Lock()
        self.fb = firebase.FirebaseApplication(userUrl, None)
        if self.fb==None:
            print('error!')

    def setExistVisitorVar(self, value):
        self.setter(self, existVisitorVar,value)

    def setToPlayVideoVar(self,value):
        self.setter(toPlayVideoVar,value)

    def getToPlayVideoVar(self):
        result = self.getter(toPlayVideoVar)
        return result

    def setLastTimeVisited(self,value):
        self.setter(self, lastTimeVisitedVar, value)

    def setNumOfVisitors(self,value):
        self.setter(self, numOfVisitorsVar, value)

    def setPlayIndexVar(self,value):
        self.setter(self, playIndexVar, value)

    def setter(self,varName,value):
        self.threadLock.acquire()
        self.fb.put(tableUrl, varName, value)
        self.threadLock.release()

    def getter(self,varName):
        self.threadLock.acquire()
        result = self.fb.get(repoName+varName, None)
        self.threadLock.release()
        return result