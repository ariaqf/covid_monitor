import datetime
import pre_processor
import numpy as np
import matplotlib.pyplot as plt

class Regressor:
    def __init__(self, dataset = None, identifier = None):
        self.defaults()
        if dataset == None:
            pp = pre_processor.PreProcessor(self.file)
            self.dataset = pp.pre_process()
        else:
            self.dataset = dataset
    
    def defaults(self):
        self.file = "full_data_"+datetime.date.today().isoformat()+".csv"
        self.threshold = 1
        self.total_training_days = 0
        self.model_trained = False
        self.fit_percent = 0.01
        self.minimum_last_value = 10
        self.minimum_days = 21
        self.evaluated_country = 'Brazil'
        self.identifier = 'total_cases'
        self.specific_defaults()
    
    def specific_defaults(self):
        pass
        
    def select_training_test_data(self, identifier = ''):
        self.training_test_set = {}
        self.current_identifier = identifier
        for country_name in self.dataset.keys():
            country = self.dataset.get(country_name)
            data = country.get(identifier)
            result = self.test_fit(data, country_name)
            if(result):
                if self.total_training_days < len(data):
                    self.total_training_days = len(data)
                self.training_test_set[country_name] = data
                
      
    def test_fit(self, data, country_name=""):
        result = False
        if len(data) >= self.minimum_days and data[-1] > self.minimum_last_value:
            previous_variation = 0
            current_variation = 0
            for i in range(1,8):
                previous_variation += (data[-7-i] - data[-8-i])
                current_variation += (data[-i] - data[-1-i])
            mean_previous_variation = previous_variation/7
            mean_current_variation = current_variation/7
            last_total = data[-1]
            if mean_current_variation < mean_previous_variation and mean_current_variation <= last_total*self.fit_percent:
                result = True
        return result
    
    def train_model(self):
        pass
    
    def fit_into_model(self):
        pass
    
    def run(self):
        self.select_training_test_data()
        self.train_model()
        self.fit_into_model()
    
    def plot_training_test_set(self):
        for key in self.training_test_set.keys():
            data = self.training_test_set[key]
            plt.scatter(range(len(data)),data,color=np.random.rand(3,), edgecolors='black', label=key)
        plt.title("Training Test Points")
        plt.xlabel('Days')
        plt.ylabel(self.current_identifier)
        plt.legend()
        plt.show()


    