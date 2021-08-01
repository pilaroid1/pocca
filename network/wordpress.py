"""
POCCA (Python Open CV Camera Applications)
Author : µsini
Wordress API

Sources
- https://timosam.com/auto-upload-images-wordpress-python-caption-description-alt-text-etc/
- https://playingwithpixels.gildasp.fr/article/introduction-a-lapi-json-de-wordpress
"""
import requests
import json
import base64

class Wordpress():
    def __init__(self, settings):
        self.url = settings["WORDPRESS"]["url"]
        self.user = settings["WORDPRESS"]["user"]
        self.password = settings["WORDPRESS"]["password"]

    def send(self, filename, caption, description):
        # Generate Authorization token using username / password
        token = base64.standard_b64encode((self.user + ":" + self.password).encode("utf-8"))
        headers = {'Authorization': 'Basic ' + token.decode("utf-8")}

        #  Generate image upload request
        media = {'file': open(filename, 'rb' )} # Load image data
        image = requests.post(self.url + "/wp-json/wp/v2/media", headers=headers, files=media)
        response = json.loads(image.content)

        link = response["link"]
        postid = response["id"]
        print('Your image is published on {} with ID {}'.format(link, postid))

        # Generate Caption/Description modification request
        post = {"caption": caption}, {"description": description}
        print("Request:" + self.url + "/wp-json/wp/v2/media/" + str(postid))
        r = requests.post(self.url + "/wp-json/wp/v2/media/" + str(postid), headers=headers, json=post)
        print(json.loads(r.content))
        return postid