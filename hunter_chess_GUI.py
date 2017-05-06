# -*- coding: utf-8 -*-
#!/usr/bin/python
#HunterChess:
#    author: 刘浩杰
#    e-mail：sadnoodles@gmail.com
import wx
import re
import cStringIO

SERVER, PORT =  ('60.191.205.87', 52700)

image_white='iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA\nIGNIUk0AAHol\
AACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAb/SURBVHja3FpdaFNn\nGH6SJmniYhq7tput3UZXf9COIghicDiGP0\
ywOOgseOXVmNCLspsJDqc4NiZs2MteSRleDSz+7aJX\nbqiTolAW3dbWatI20dqY09qmJ8k553t38x44jSfJOclZJwZezpfvHJL3\
+Z7373u/4yIivA4fN16T\nz2sDxGP84nK5bP+ApmkgIugmSkQ+IvrAcNXvLxHRmH4VQoCIUF9f7wgQl9FHKgGiqiqIqIWIPiWi\n\
LiLaZ1C+mMxpmvarEGLI5XINNzY2yv8rEEVRdhHROSLazWyUFJ2Fgjk5n8//PD09/XUkEkkBoFUD\noijKVgDfMguwK0ZA+lgIkV\
lcXPzpxo0b548fPy7ZBWQbiKIoXzILNVWwUHSsqmoiGo1+dvjw4bsA\nVKuALANRFMUHYICIjlW6+laAEBE0TVuemJjoO3jw4EUA\
OQCiHCBLQBRFqSeiy+V8QQgBABUpbzaO\nx+M/7N+//3sAGQBaKTBuC6ZUQ0S/ENFu/Q+KSbn7VkXTNAgh0NLS8tXFixd7AdQB8A\
JwVQxECHGe\niD4uXOVSihufqRSELtu2bTt95syZrnJgSgLJ5XKfE1GvmdJmpuAECyaL4jlw4MD57u7uHQBCnMRd\nln0km802Et\
EjAEGj7VvxAau+UGxBzK6xWOyP7u7uLwBMA1jkiFaeESI6Q0TBcn9q15z0lTdjoNS9\nDRs27Orp6dkPoAlAoFB3U0ZkWW4XQjwA\
4DNbabssWJmzwkoymXzErPwNYA5AXo9k7iIOfpKIfNX4\nQKkVt+IbZvNNTU1tR48e/QTA2wDeMOr/EpClpaWgEKLHSiQq/G5XeS\
vPFz4biUT2AmgBEDZGMY+J\nb3QRUcCK6dgxpVImY8fp29vbt3i93ncVRXkKYAGAAkBzm5jVnkryQTETKceCXcbcbrd3z549O9i8\
\n1upkuE02Sh9WG/srMSE75tnR0bGZo1cYgA+Aa4VpSZLkE0JscqJOqtaESt1raGhoBNDA2T4AIOMp\nMKt3iKjGSeXthFer90Kh\
0FrO8jqQGk9BSRL2eDyOKe8kMOO4tra2FsAa9pEAAI+nIGIFrP6Y0ytt\nZ+G8Xq8HgJ9zSe1LQHK5XNbv978yJlRsLMuyxjnEz9\
eVpiXLcsbn870yJlRsnM1mNQA1OggArhXh\n9+rVqzEhhOZEkVcuQ1ciOqBUKiVz6nDpmX0FkBMnTuTz+XzSyp/ZBeakJBKJDBeL\
urxUopAsy3cD\ngUDrapqQlbLHKOPj4wu8h1f1vXxhZhfpdPr31TAhq6wVLlYulxOjo6PPucbKFq21Ll26dFXTNKXS\n0sMJ5UsB\
Gh8fT2ez2RyDyHC76CUg1N/f/0ySpFtOFXlW5uzsNm/evPmUWVjmLW8WgGq2sVJGRkYG\nnCzyKmWj0E/m5uaWb9269YyVXwTwAo\
BsaloA1L6+vt9SqdRoJdWrU6Zkxtjw8PCUpmk5AEsAngOY\nZ1DCDIgGQL58+fI5TdOEEznF6m6zVMSLx+MLw8PDT5iBNO/ZX7CP\
kBkQAiD39/ffiUajQ6udN8xA\nqKoqBgcHx4QQeVb+GYBZHiul2kEqgBe9vb0/JpPJyf/KbEp1LY3zQ0NDDycnJxfZpJ4BmGFGMt\
zg\nLgpEAMgsLy8/PXXq1DeSJKWrBVAqEpVKinfu3Eleu3Ytwb6QZhAzPC7dDuKbCgApGo3eP3v27Hfp\ndHreaectB/revXtPBg\
YGxlhhibuMjwE8YXY0K8cKLq4u6wG0t7a27jp9+nRfa2trs9VqtdRcmTMV\nun79+qOhoaEpXtB5AI8A/AngPoApO0B0MH7e6G/0\
er2dJ0+ePLZz584Op4Ho5y65XE67cOHCg5GR\nkefMxAIr/heDiDGwFadZVg563LytbAKwEcDWrq6uvUeOHPkoFAqtsQLEqoyNja\
UGBwcfzs7OLnNY\nnWdz+ofbpPFC37B79FbDYBoBtAHYXFdXt+XQoUORffv2bQ0Gg/5qWIjFYvNXrlyJjY6OSnoeY4Wn\nAIwDmO\
CxpOeNag5Da3ij/yaAdwC0A3gfQHMkEtm0ffv2DZ2dnW+FQiG/ldV//PixFI1G07dv356b\nnZ2VOVLm2fZTrPhDAJMAEmxi+WLH\
b3ZPdd282Q8DaAbwHkszAwy2tbU1NDc3161bty5QV1dXGw6H\nfUSEmZmZjKqqFI/HlxKJhCxJUt4QHfPMwgLnCT06TfH3JX6OnD\
xnd3F3L8jKr+em8npumoW5u+E3\n7KndhlMm4tVX2UyWWVGJlU4yA7M8J5c7CK3mzQcXK1jLvaUwg2pgWccNtACD8RhylmZgIcMO\
neYi\nMMXjBQMLYjXeRTECCjBLIb4GDX0nHz8HAxMys/GCS/IllqwBgOW3H6p+qcYASE+gPpZaFiMjZNhr\n51myhrGGCt9F+XcA\
0CcTQNyoqtEAAAAASUVORK5CYII=\n'
image_black='iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA\nIGNIUk0AAHol\
AACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAgBSURBVHja3JpPjBxH\nFca/qp7ZXTu7i4FsUAQBGZGAViAuHAgKAq\
GAxSWST0Y+WUKO4GAJ5WAOBgMyWtmRQDli5BvCFw45\nBHFA4hAsBAgOJAoQgzcYJ+vYa2dndz3/urqrHgdejd68qeqZ3RgObqnU\
1bM9ve9X33uvXlWPISI8\nCIfFA3I8MCAteWGM2fMDLly4AACILkpEc0T0qRBCPMN7jxBCt67rq977blVVV51zcM7h0qVL9x9k\n\
PwcDfBDAUQDPENGX5d8E4OgcQrjjvf9VXdcvHj9+/NeXL18evFs7jAz2vSpy/vz5JwE8D+ApaTgb\nOzp77+G9R13XqKoKUY2yLF\
GW5aDf7/9se3v7O1euXLkLgP5vIGtra6sAfgjgaPyOHPEIIFtVVWOt\nLEs45zAcDlGWJYbDYa/X6/14c3PzhfX19c5egfYc7OfO\
nXsuhPAqER2VCmgV5Gd1XY9Uicp471FV\nFeq6ju0hAN9dWlp69fDhw58F0AZg7rsiZ8+enbPWXrTWnoj3yvtlPESQaHRs0q2Ea0\
VF5HW/2+1+\na2Nj4+cASgBhmkIzKXLmzJn3EdFvQggntMvkWnQhCdHUJLD3/mBRFD9dWVk5C2ARQDFNnalZ6/Tp\n04X3/hcAnj\
LGgIjG1IifiYw05kKyOedGhkdVIoQG8t7DGPPt5eXle7u7uz8BcA9AlVNmKoj3/gUi\n+hIRwVoLa/8rYjzHIyrBc8YYiB59DeCc\
m4COMNba78/Pz98sy/KXAHZyMI0xcurUqWettReLohhB\nGGMmIGSW0gEtQbQiMXPFfgqSn7dbluXXvPd/Yphaw2RBTp48udJqtd\
6w1i42gchMpZXQINqtdNMx\nIzNdCOH3zrlvAHiT3ayeybWqqvoBES0WRYEQAoqiGEHIuJABHt1KgugYiAbrs44PARAz4pPW2q+E\
\nEF5iiB5nszzIsWPHPlbX9dfjSEcYqUQOJLboFhok5WaZzDV6ZrQDwDcBvMIQjhtlQaqqOkNEc0VR\nILaohI4LnamkIjrYc/0m\
NeTkSkQfBfBVAB0AfVbGJ0GOHDmy6Jw7FpXQELIk0XOHNCQFI8+6L78r\nn6mrBwBPA3gZwBbDBAA0AeKceyaEcMB7Dx3kqTkj5V\
YpkBSYzm56YBRAHMRPENFHANwS6dinQL4Q\nR1eqoUG0W+VSr+7r0Y8AGVeaKIW4BvsMgH8DuA2gmwQpy/LzOYgIkqpwtSIaRALq\
JgFCCCPD9Xwl\njo8T0SMADgF4B4AbA1ldXZ0ry/IJa+0EiJ7FI4xUI6VKriUy0lh6b1jEAcAKgIcBvAfAAQC9llLj\nw0VRFDou\
Umo0KZJTSLtQynidGWVf1HpLRLQsQIqWio9DegbXo6PTrlZDp+JUForPjq4zbUGnIEBE\n8wAOAlhikFZLzR8HtBL6gXoRJQ1NAc\
WRT5U4M7gQ9L4bX7cALAB4CMD8BIhzbpiLC72MjRCpOJHG\nt1qtMXX1c3VKnwIwKso5ey3wedy16rruyUyh/4mODa0IABRFgXa7\
PWH8tBho+ixxj+fFVjsuunSw\nX2+32/GmiZHSsaFHXheWORfVft8EpVXi6wGvbk1cOWoQZ4y5CeCx1M6IhIjGS7/X2S4VB03uo/\
9X\nw2c9LhYpVzSS9/7PAB5LQcTRb7fbY4brLJeqy1Iq6OdPa+I7OxwnsWgkPXWGEMJvdRrV7pNrKbiU\ni2njdBJJXUsbeTavAA\
xjrTVRA4QQXgohVHH0ooHR2FarNQHUBDDLyOsSRddc6tjiLaIhu1iZAiEi\n2rTW/k4bl2syPnJBnQORZUqTK6nn3WIV+rzkHQKo\
U1VZBeBiHNHcaOc2InIVQC5tp9Y1DSm4D2CT\njb8HYJczmE9ZUYcQXjbG/CXl500zf5Mb6bI/51ZT5o8b7EpdjpNthgopEA9gEE\
J43hgTUsGamtRS\nBudKF12PyTmp4dgB8DYrsAXgDitSprIWOC8PvPd/CCG8mKuJUllnFphUZprhCER0lTcbdtm9bnO/\natr7rQ\
HsOud+BGB9lgBOle4SIHXPjBAgomscE12GeIsVGW0J5UAC33SrLMvvEdFWUwbSI51SIRUL\nuXlGHTcBbHAsbDHEW9wfbQflQIgl\
64QQXivLco2ItvXqMFfGa6OlCpl1+FihKv72tnCpDu8y/otj\npRu3gqa9Vgic7m577/84GAzWvPc39Q5KUyzk1uKzeBOAdSJ6nQ\
d0h1W4xpsOY2rM8qLHcM3/CIDH\nAXx6YWHhRFEUn2xKt9rN9vh+0hPRX4noHTZ2B8ANAH8D8BqA65x2672ARNUOCpjVVqv1dLvd\
/qIx\n5mBuzohuuEeIuyGEa+wJJRv8JoDXAfw9p8asr6cD5+47ccTqunbe+zeKovictXYVwMI+Uqo8tono\nOhF14jzGBt8A8A8A\
/+R+JwWxl/fsXpQHHkBJRP26rncAvGKtfQLAh4wxHwghLMz4I4QOEW0R0R02\nPLCRXQB32fBrnP432MXcvt9YJWA8P7DPE1InhN\
Dhf7oo95uMMfNENKcWQ10iGgijKu4P2NhNkZ1u\n8HW36bXbft+zGwBzbPT7ATzKv3x4lCEO8e7GglhTW/Eyk3j0a46DPhvaYaPj\
vHGbPxvExdP/4pcP\nhg2c572lQwz1MLf3AljmPac2K2+FslGFHgf0FheBd7m/I1SYKeDe1U84FNABVmmZz4ti32kubmgI\nJQbC\
PWP50RWrvqnv1u8niAQyPPpz3Oa5SUVIrLXjG6eh6Hvs87co/xkANa6XmYBwDVMAAAAASUVO\nRK5CYII=\n'
image_mask='iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAA\nIGNIUk0AAHol\
AACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYAAAgQSURBVHja3JpfaBzH\nHce/s7f3/3x30klWbbWO7FrFji03qR2CHy\
pTy23IUxuCcR9CodBgkkJJSx9KoQHlqeqDoaVyU1oK\nbQgYk4cSUkpKiYXjtEncGOcc7EYxRkRRLZ3OOt3pdm//zM70ITPu3Hr3\
bu/k6iELw+ztrlbz+f2f\nmSWcc3wWDg2fkUOXJ4SQvl7A+W/CbuUch5Y0TcsBgG27RqNhre3c+ZMN+QClv+acc3DOwRgDY6zt\n\
PErbvXumHWSzB6Vsv6aRA4TgIULIIAAkEv97va4nkc0mwdhZUOrVLMstf/JJ7cbY2M9uAGCiodH4\nBY8C4HkeGGN330+kj/SjEd\
P8VSmdjj8O4CEAmW7PS4lLqXPOQanXMgz7g4sXb75+8uQfqgA8CbWy\nMs3DAOT5/v2/7B+kVjuTzedTj2saOQYg1t382gcfZEqe\
57HV1eY/X3zxrb+dOTPXAEAl0Mcf/5T7\nAWQ/MTHbHwils1+NxbRvAUhHBfCDdPIHSj17fr7y+rFjZy8BcKSGbt78MVcBZP/ww7\
/tDeTChR/G\nJifHT2oamYwWBO4dfC9OvbhYe++JJ/705+XljZYChGvXvs9VmCNHfh89/NZqZ7KTk+M/iAKhDlA1\nB/lblabaKK\
V3e0opRkayh1977TunH3tsfDuAFIA4ADIxMUvUZyPnkeXlmVShkPqRppHxXiCCAIIg\n5KA+NSvadj2Xi39+evr49yYmRoaEKccB\
aIcP/45I4KggZHh423cJITt6BQiTvCp1vxb89yilSKe1\nwZmZqVP5fLIoYHQA5OjRPxIVpJOPEM87+01NI9+IArHZxOZ3ZL8pXr\
26/P7TT//lrwDqAFoiqnHR\nwjXiurOHOkF00kKYJjppJ8hP1GcefHDwy889d+QrAPLCZ2Jda63l5ZlULEa+3SmxhUmyX4Ao7cSJ\
\nL0zu2JHdDiAHIClgSBgIGRzMniCEFHpx5qgQUQDC7iUSJHX69MRRAAXV+QEQPUAbSV3XvrbZxNbN\n7Dr5RZBw5PnBgwNfGhpK\
XatWLVv4iQeAaQHaOEoISQcltk7/oBcN+P0hTAOu696jKV3n+pNP7j7o\n18o9GtE08qhfC0FRKUwTnueBcx6YDKNEpyBB+a8fOF\
B8AMAHAAwRwdw2kKWln5diMW1X0OC7QUiA\nfs2oF5ChoXhuz57cyK1bzQ0ATQC2CkJyucTeoNooSPJBUu9FA91AumulsOPWreZt\
YV5Gm0ZiMTLe\njyP3ktiiaCKKMMbGMiURhtMAEn4fGdksQL9+0Ks5Fot6WkCkACT19uTIB1Rb3yzAZhw6rHqWJp3J\nICkgUgDi\
PhCWZgz3HaCbGXX6uyAgxhjicWgi9Cb9IIRzntqqxNbLO4KarnMJEgegt4FQSh3OeSIq\nQBTp3m8A2Wzb46I8iQOItTm741BH05\
DYqsTWD4BslkUliObP7MRx3Kauk9xWJbZ+AGREbTRcJgtG\nf9HI63WzUiymPreVia1XAHm+smI7ysSKt5nW2pqxsm1bfEsTW1it\
FgYh+5UVxxUQzA/CL19evDk6\nmvv6Via2ID8Mq+vU2m9+3jJFCe8B8NQyns/MzN02TduIOmPrZVLkn7pKGPV60LQgSGsbGx5bWn\
It\nMR9xAVBVI6xSaboLC2vXx8YKj2xVYgvTRFDhKhdKrl9vtTyPSwgHAG3TCAB67lz5X47jsl7m050m\nSkGLCUGtk4mqEJ7H8f\
bbRlNA2AAsAI4fxHv55XJlfr7676gztigm1m0eHxRI/JqSR7ncalWr1BIQ\npphYOf6prgfAmZ29fMmyHNqvH0QF6BbF/NuCjsPx\
xhsbTWFOrTAQGcqcS5cWq1eu3L7Wr5NHXRLq\nFJKDjnfeMcx63bPE4A0AG2EaYSIStKan3/pHpdKsB0WcbgtqUQDCNBG2OVupUO\
/ChY2G8AkTQENM\nc1t+Z7+7BQLAXl+3G7OzV/9umu0mFmRWYasnvZhSp91l2+b8/Pm1OqVc+kVdNEP4CvXPEKV5uQDM\nixeXFo\
vF+JtPPbX3mKZB+38ktm7b45RynD+/1qhUaEtIvwFgXfSmGCsL2wylQoXNV19dmKfUS586\nNfaIriMWZeknDMIP0g3Ctjl/5ZVa\
46OPbFOBqAmQphgj7bQaT8TyfQbAAIDhffsKX3z22fFH83k9\neb8SW6djfd1jL710p766SqVPrAOoAFgRfU1cpwB4JxACIAEgK2\
FKpeToM8/sObJrVzrfK0RULQDA\nwoLjnju3VjdNJsPsOoCqAFgVEIYIw7wTiITRfDBDALZPTQ3vPX68tCufj8U7QfSjhbm5DePK\
FdNU\nckUdwJqAqCpm5cjKN8pmqIRJCpgCgBKAoXiclKamSg9MThZHEgloYSYUlhPUw7IYn5trmu++a5iU\nclfJ2g0BUQVwxxep\
2Asv7OTPP/+fyLu6qmYyYqNlQAANAMgfOpQd3rcvXRwfT2UzGaJFMaNmk7H5\necv58EPLuXHDaomqwlUytnTsO6KXUcqREAAgQa\
J8wnE34/vCs5SaUS4bRrlsZAGkR0cTueFhPZ3J\naHqhENMzGS326VcSjK2vU2YYjFUqlC4vu9I0PKWKlRm7IaRf8yU+V4UI/Kgm\
IoyrZH9XhD9ZKmwD\nkF1achpLS05Srm6IJufW6rs8BcL2lR0N0TeFsGy5DxIE0c+XD0QRgC5W+dLC5DLCjzLKUqZ8LgiE\nKvlK\
CsQQA5d5w1Kek3+L+wHi95uYGGhS+JBcwpS/E+J+TNnmk9qgwpwcZV5hKb+p8oFN15D33wEA\nGJD4dBeYRlwAAAAASUVORK5CYI\
I=\n'

import socket
import time
import re
socket.setdefaulttimeout(3)
class Client:
    def __init__(self, server='127.0.0.1', port=52700):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))
        
    def read(self, size=10240):
        return self.sock.recv(size)
        
    def write(self, msg):
        self.sock.send(msg)
        


class Chess(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(10, 10))
        self.SetBackgroundColour('WHITE')
        self.win_count = 0
        stream = cStringIO.StringIO(image_white.decode('base64'))
        self.WhitePiece =wx.BitmapFromImage(wx.ImageFromStream( stream ))
        
        stream = cStringIO.StringIO(image_black.decode('base64'))
        self.BlackPiece =wx.BitmapFromImage(wx.ImageFromStream( stream ))
        
        stream = cStringIO.StringIO(image_mask.decode('base64'))
        self.MaskPiece=wx.BitmapFromImage(wx.ImageFromStream( stream ))
        
        # self.WhitePiece=wx.Bitmap(r'img\白子.png', wx.BITMAP_TYPE_PNG)
        # self.MaskPiece=wx.Bitmap(r'img\mask.png', wx.BITMAP_TYPE_PNG)
        self.newGame()
        # print self.BlackPiece.Size
        
        
        
        self.piece_r=20
        self.rcWidth=100
        
        self.meshLeftTop=(50,50)
        self.Size=2*self.meshLeftTop[0]+self.rcWidth*3+20,3*self.meshLeftTop[1]+self.rcWidth*3
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        # self.Bind(wx.EVT_LEFT_DCLICK, self.OnDbClick)
        # wx.EVT_LEFT_DCLICK
        # wx.EVT_LEFT_DOWN
        # wx.EVT_LEFT_UP
        self.InitBuffer()
        self.Bind(wx.EVT_SIZE, self.OnSize) 
        self.Bind(wx.EVT_PAINT, self.OnPaint) 
        self.Centre()
        self.cli = Client(SERVER, PORT)
        self.cli.read()
        self.last_recv = ''
        time.sleep(0.1)
        
        
        
    def OnSize(self, evt): 
        # When the window size changes we need a new buffer. 
        self.InitBuffer() 
    def OnPaint(self, evt):   
        dc = wx.BufferedPaintDC(self, self.buffer)

    def InitBuffer(self): 
        u'''生成一个缓存PaintDC,并在其上绘制，避免直接显示造成闪烁'''
        w, h = self.GetClientSize()         
        self.buffer = wx.EmptyBitmap(w, h) 
        dc = wx.BufferedDC(wx.ClientDC(self), self.buffer) 
        self._mesh(dc)
        self._draw_info(dc)
        self._draw_pieces(dc)
        
    def _mesh(self,dc):
        u'''绘制网格'''
        dc.SetBackground(wx.Brush(self.GetBackgroundColour())) 
        dc.Clear()
        dc.DrawRectangle(self.meshLeftTop[0]-1,self.meshLeftTop[1]-1, self.rcWidth*3+2, self.rcWidth*3+2)
        for i in range(3):
            for j in range(3):
                dc.DrawRectangle(self.meshLeftTop[0]+self.rcWidth*i,self.meshLeftTop[1]+self.rcWidth*j, self.rcWidth, self.rcWidth)
    def _draw_info(self,dc):
        u'''显示当前玩家信息'''
        info="Current player:%s"%(['','Black','White'][self.currentPlayer])
        dc.DrawText(info,5,5)
    def _draw_piece_by_pos(self,dc,pos,player=1):
        u"""根据在棋盘中的位置绘制一个棋子"""
        x,y=self.pos2xy(pos)
        # dc.DrawCircle(x,y,self.piece_r)
        # ic=wx.Bitmap(r'GitHub40001.ico', wx.BITMAP_TYPE_ICO)
        if player==1:
            x0,y0=self.BlackPiece.Size
            dc.DrawBitmap(self.BlackPiece,x-x0/2,y-y0/2,True)
        elif player==2:
            x0,y0=self.WhitePiece.Size
            dc.DrawBitmap(self.WhitePiece,x-x0/2,y-y0/2,True)
        elif player=="SELECT":
            x0,y0=self.MaskPiece.Size
            dc.DrawBitmap(self.MaskPiece,x-x0/2,y-y0/2,True)
        else:
            raise 'Error drawing pieces'
    def _draw_pieces(self,dc):
        u'''绘制所有棋子'''
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j]==0:
                    continue
                self._draw_piece_by_pos(dc,(i,j),self.map[i][j])
                if (i,j)==self.selected_pos: #绘出选中的棋子
                    self._draw_piece_by_pos(dc,(i,j),"SELECT")
                    
    def OnDbClick(self,event):
        self.undo()
        self.undo()
        self.selecting=False
        self.selected_pos=None
        self.OnSize(None)
        # for i in self.history:print i
    def OnClick(self,event):
        x,y = event.GetPosition()
        pos=self.xy2pos(x,y)
        #printpos
        moved = False
        if pos:
            if (not self.selecting):
                if self.map[pos[0]][pos[1]]==self.currentPlayer:
                    self.selecting=True
                    self.selected_pos=pos
            else:
                self.selecting=False
                if self.selected_pos and  self.canMove(self.selected_pos,pos):
                    self.move(self.selected_pos,pos)
                    moved = True
                    if 'input from pos, to pos' not in self.last_recv:
                        r = self.cli.read()
                        print r
                    self.cli.write('{0[0]},{0[1]},{1[0]},{1[1]}\n'.format(self.selected_pos,pos))
                self.selected_pos=None
            self.OnSize(None)
            self.ifWin(self.currentPlayer)
        if moved:
            self.afterClick()
    def ifWin(self,player):
        if (not self.GameOver) and (not self.count[player]):
            ap = self.getAnotherPlayer(player)
            if ap == 1 : #black
                self.win_count += 1
                print('win_count', self.win_count)
            else:
                self.cli.sock.close()
                exit(1)
                self.win_count = 0
            wx.MessageBox("Player %s WIN!"%(['','Black','White'][ap]),'Note')
            self.GameOver=True
    def afterClick(self):
        r = ''
        count =0
        while not r and count <3:
            try:
                r = self.cli.read()
            except:
                r= ''
            count += 1
        print r
        r = r.lower()
        self.last_recv = r
        if 'win' in r or 'flag' in r:
            wx.MessageBox(r)
            self.newGame()
            self.currentPlayer = 2
            self.OnSize(None)
        m = re.findall('\[(\d), (\d), (\d), (\d)\]', r)
        new_map=[]
        
        if 'white win' in r:
            self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
            return
        
        if not m:
            raise ValueError(r)
            
        for i in m:
            new_map.append(map(int, i))
        self.map = new_map
        self.OnSize(None)
        self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        
    def newGame(self):
        u'''新游戏开始，初始化数据
        currentPlayer：当前玩家 值为1或2
        selecting    ：是否正在选择False
        selected_pos ：被选中的子位置
        history      ：走子历史
        count        ：计数，剩余子的数目，列表,第一项起占位作用[0,4,4]
        map          : 棋盘的数据
            '''
        self.currentPlayer=1
        self.selecting=False
        self.GameOver=False
        self.selected_pos=None
        self.history=[]
        self.count=[0,4,4]
        self.map=[[1,1,1,1],
                  [0,0,0,0],
                  [0,0,0,0],
                  [2,2,2,2]]
    def canMove(self,pos1,pos2):
        u"""判断是否能移动，判断标准：1，距离为1；2，没有子。"""
        s1=abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])
        return s1==1 and self.map[pos2[0]][pos2[1]]==0
    def undo(self):
        u"""撤销移动，如果有吃子，也同时撤销"""
        if not self.history:
            return
        if self.GameOver==True:
            self.GameOver=False
        from_pos,to_pos,eat=self.history.pop()
        if eat:
            self.map[eat[0]][eat[1]]=self.currentPlayer
            self.count[self.currentPlayer]+=1
        self.map[to_pos[0]][to_pos[1]]=0
        self.map[from_pos[0]][from_pos[1]]=self.getAnotherPlayer(self.currentPlayer)
        self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        
    def move(self,pos1,pos2):
        u'''移动一个棋子从pos1到pos2，如果有吃子eaten是被吃的坐标'''
        self.map[pos2[0]][pos2[1]]=self.currentPlayer
        self.map[pos1[0]][pos1[1]]=0
        eaten=self.canEat(self.map,self.currentPlayer,pos2)
        if eaten:
            self.map[eaten[0]][eaten[1]]=0
            self.count[self.getAnotherPlayer(self.currentPlayer)]-=1
        self.history.append((pos1,pos2,eaten))
        self.currentPlayer=self.getAnotherPlayer(self.currentPlayer)
        return eaten
    def _strip(self,l):
        u'''去除列表首尾的0，返回剩余的'''
        line=[a for a in l]
        while len(line)>0 and line[0]==0:
            line.pop(0)
        while len(line)>0 and line[-1]==0:
            line.pop()
        return line
    def _hasEatPattern(self,line,currentPlayer,lastStep):
        u'''判断是否有吃子的结构'''
        left=self._strip(line)
        if currentPlayer==1:
            if left==[1,1,2] or left==[2,1,1]:
                return True
            return False
        if currentPlayer==2:
            if left==[1,2,2] or left==[2,2,1]:
                return True
            return False
    def canEat(self,m,currentPlayer,lastStep=(0,0)):
        u'''判断是否能吃子，是则返回被吃子的位置；否则返回None'''
        line=m[lastStep[0]]
        col=[a[lastStep[1]] for a in m]
        if self._hasEatPattern(line,currentPlayer,lastStep):
            return (lastStep[0],line.index(self.getAnotherPlayer(currentPlayer)))
        if self._hasEatPattern(col,currentPlayer,lastStep):
            return (col.index(self.getAnotherPlayer(currentPlayer)),lastStep[1])
        return None
    def getAnotherPlayer(self,player):
        return 1 if player==2 else 2
    def pos2xy(self,pos):
        u""" 将地图坐标，即列表的行、列转化为GUI的坐标  """
        x0,y0=self.meshLeftTop[0],self.meshLeftTop[1]
        w=self.rcWidth
        return y0+w*pos[1],x0+w*pos[0]
    def xy2pos(self,x,y):
        u""" 将GUI的坐标转化为地图坐标，即列表的行、列  """
        x,y=x-self.meshLeftTop[0],y-self.meshLeftTop[1]
        r=self.piece_r
        if -r<x<r+3*self.rcWidth and -r<y<r+3*self.rcWidth:
            posx=(x+r)/self.rcWidth
            posy=(y+r)/self.rcWidth
            if x <=(posx*self.rcWidth+r) and y<=(posy*self.rcWidth+r):
                return posy,posx
        return None
#

if __name__=='__main__':
    app = wx.App()
    c=Chess(None, -1, 'Chess')
    c.Show(True)
    app.MainLoop()