
from firebase import firebase
from imgColorReader import ImgColorReader

url = 'https://hackalexa.firebaseio.com'
fb = firebase.FirebaseApplication(url, None)
var = 'color'

class DetectColorAndSendService(object):
    @staticmethod
    def detectAndSend(tableUrl, frame):
        print('detectAndSend')
        colorValue = ImgColorReader.readMainColorOfPicture(frame)
        print(tableUrl)
        print(var)
        print(colorValue)
        # result = firebase.put(tableUrl, var, colorValue)

        result = fb.put(tableUrl, var, 'ttt')
        # # print('blue')
        # print(result)
