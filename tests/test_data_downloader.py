import data_downloader
import unittest
import os

class UpdateTest(unittest.TestCase):
    def test_download(self):
        file = {"name": "test_file.txt", "url": "https://www.google.com"}
        if(os.path.exists("./" + file["name"]) and os.path.isfile("./" + file["name"])):
            os.remove("./" + file["name"])
        upd = data_downloader.DataDownloader([file])
        upd.download()
        assert os.path.exists("./" + file["name"]) == True
        assert os.path.isfile("./" + file["name"]) == True
        if(os.path.exists("./" + file["name"]) and os.path.isfile("./" + file["name"])):
            os.remove("./" + file["name"])