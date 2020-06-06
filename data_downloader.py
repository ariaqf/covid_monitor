"""
 This file aims to offer a function for downloading updated files for data processing.
"""
import urllib.request
import datetime

class DataDownloader:

    def __init__(self, file_list = None):
        self.file_list = file_list
        if(self.file_list == None):
            self.defaults()
        
    def defaults(self):
        self.file_list = [
            {
            "name": "full_data_"+datetime.date.today().isoformat()+".csv", 
            "url":"https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/ecdc/full_data.csv"
            }           
        ]

    def download(self):
        for file in self.file_list:
            urllib.request.urlretrieve(file["url"], file["name"])
      

if(__name__ == "__main__"):
    dd = DataDownloader()
    dd.download()