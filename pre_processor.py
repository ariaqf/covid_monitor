import numpy as np
import datetime

class PreProcessor:
    def __init__(self, file_name = None, data_identifiers = None, blacklist = None, whitelist = None):
        self.defaults()
        if(file_name != None):
            self.file_name = file_name
        if(data_identifiers != None):
            self.data_identifiers = data_identifiers
        self.blacklist = blacklist
        self.whitelist = whitelist

    def defaults(self):
        self.file_name = "full_data_"+datetime.date.today().isoformat()+".csv" 
        self.data_identifiers = ['new_cases','new_deaths','total_cases','total_deaths']

    def pre_process(self, data_identifiers = None):
        if data_identifiers != None:
            self.data_identifiers = data_identifiers
        file_data = self.read_file()
        data = self.extract_data(file_data)
        return data
    
    def extract_data(self, data):
        macro_data = {}
        countries = self.filter_countries(data)
        for country in countries:
            macro_data[country] = {}
            for ident in self.data_identifiers:
                macro_data[country][ident] = self.filter_range(data, country, ident)
        return macro_data
    
    def filter_countries(self, data):
        countries = data['location']
        if self.whitelist != None:
            countries = self.whitelist
        elif self.blacklist != None:
            blacklist_filter = np.ones(len(countries), dtype=bool)
            for blacklist_item in self.blacklist:
                blacklist_filter &= (data['location'] != blacklist_item)
            countries = data[blacklist_filter]['location']            
        return np.unique(countries)


    def filter_range(self, data, country, identity):
        date_filters = (data['location'] == country) & (data[identity] > 0)
        dates = data[date_filters]['date']
        selected_range = np.array([])
        if len(dates) != 0:
            first_date = dates[0]
            filters = (data['location'] == country) & (data['date'] > first_date)
            selected_range = data[filters][identity]
        return selected_range

    def read_file(self):
        file = np.genfromtxt(self.file_name, delimiter=",", dtype=None, names=True, encoding='UTF-8')
        return file

if(__name__ == "__main__"):
    pp = PreProcessor()
    pp.pre_process()