import json
import requests
from PIL import ImageTk, Image
from firebase import Firebase
from io import BytesIO

class search:
    def __init__(self):
        #url = "https://dsci551-project.firebaseio.com/project.json"
        #self.data = requests.get(url).json()
        #print(len(self.data))
        self.c_url = 'https://dsci551-project.firebaseio.com/project.json?orderBy="common name"'
        self.f_url = 'https://dsci551-project.firebaseio.com/project.json?orderBy="formal name"'

        config = {
            "apiKey": "AIzaSyBecKsdkKYSh_sjvlo8Y0MDOn-A7eS1sgE",
            "authDomain": "dsci551-project.firebaseapp.com",
            "databaseURL": "https://dsci551-project.firebaseio.com",
            "projectId": "dsci551-project",
            "storageBucket": "dsci551-project.appspot.com",
            "messagingSenderId": "108599614218",
            "appId": "1:108599614218:web:d1ec7ea4b953989a7d38f3",
            "measurementId": "G-C5JBDCXECT"
        }

        firebase = Firebase(config)
        self.storage = firebase.storage()
        
    def search_data(self, content):
        res = self._load_data(content)

        summary = {"Total":0,
                   "Age": {"adult":0, "juvenile":0, "unknown":0},
                   "Sex": {"male":0, "female":0, "unknown":0}}

        for img_id in res.keys():
            summary["Total"] += 1

            age = res[img_id]["age"].strip().lower()
            sex = res[img_id]["sex"].strip().lower()
            summary["Age"][age] += 1
            summary["Sex"][sex] += 1
        
        return res, summary

    def _load_data(self, content):
        text = '&equalTo="{}"'.format(content)
        c_u = self.c_url+text
        f_u = self.f_url+text
        c_data = requests.get(c_u).json()
        f_data = requests.get(f_u).json()

        c_data.update(f_data)
        return c_data

    def search_img(self, file_path):
        try:
            url = "images/" + file_path
            pic_path = self.storage.child(url).get_url(None) 
            pic_content = requests.get(pic_path).content

            img = Image.open(BytesIO(pic_content))

        except OSError:
            img = Image.open("no_image.jpg")
            
        finally:
            img = img.resize((1000,532), Image.ANTIALIAS)
            tk_img = ImageTk.PhotoImage(img)
            return tk_img
