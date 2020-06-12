import numpy as np
import pre_processor
import matplotlib.pyplot as plt
import models
import regressor

from scipy.optimize import curve_fit
from scipy.optimize import fsolve

# if mean_previous_variation > mean_current_variation we're past the halfway point, but how to know if we're close to the end?
# my proposal is to use a rate of growth less than 1% of the total, moreover they also need to have a minimum number of cases 
# and have at least 21 days of data so it's decreasing and not a new country being infected

class TotalFunctionRegressor(regressor.Regressor):
    def specific_defaults(self):
        self.add_future_days = 0
        self.add_past_days = 0
        self.model = models.logistic_model2
        self.future_prediction = 21
    
    def run(self):
        self.setup_country_data(self.dataset[self.evaluated_country][self.identifier])
        self.fit_into_model()
    
    def setup_country_data(self, data):
        result = False
        if len(data) >= self.minimum_days and data[-1] > self.minimum_last_value:
            old_variation = 0
            previous_variation = 0
            current_variation = 0
            for i in range(1,8):
                old_variation += (data[-14-i] - data[-15-i])
                previous_variation += (data[-7-i] - data[-8-i])
                current_variation += (data[-i] - data[-1-i])
            mean_old_variation = old_variation/7
            mean_previous_variation = previous_variation/7
            mean_current_variation = current_variation/7
            last_total = data[-1]
            self.current_speed = mean_current_variation/mean_previous_variation
            self.expected_day_decay = (mean_current_variation/mean_previous_variation - mean_previous_variation/mean_old_variation)
            if mean_current_variation < mean_previous_variation and mean_current_variation <= last_total*self.fit_percent:
                result = True
        return result
       
    def fit_into_model(self):
        data = self.dataset[self.evaluated_country]
        self.X = range(
            len(data[self.identifier])
            +self.add_future_days
            +self.add_past_days
        )
        self.y = data[self.identifier]
        if(self.add_past_days > 0):
            self.y = np.append(
                np.zeros(self.add_past_days), 
                self.y
            )
        for i in range(self.add_future_days):
            self.y = np.append(
                self.y,
                self.y[-1]*(self.current_speed - self.expected_day_decay*i)
            )
        fitted = curve_fit(
            self.model, 
            self.X, 
            self.y,
            maxfev = 1000000
        )
        self.Pi,self.ki,self.x0 = fitted[0]
        self.sigma_Pi, self.sigma_ki,self.sigma_x0 = np.sqrt(np.diag(fitted[1]))
        #print(self.Pi, self.ki, self.x0, self.sigma_Pi, self.sigma_ki, self.sigma_x0)
        
    def plot_prediction(self):
        plt.clf()
        future_dates = range(len(self.X)+self.future_prediction-self.add_future_days)
        plt.scatter(
            self.X[:len(self.X)-self.add_future_days], 
            self.y[:len(self.X)-self.add_future_days], 
            label=self.identifier
        )
        y_pred = self.model(future_dates,self.Pi,self.ki,self.x0)
        upper_lim = [
            self.model(i,self.Pi+self.sigma_Pi,self.ki,self.x0) 
            for i in future_dates
        ]
        lower_lim = [
            self.model(i,self.Pi-self.sigma_Pi,self.ki,self.x0) 
            for i in future_dates
        ]
        plt.plot(future_dates,y_pred )
        plt.fill_between(
            future_dates, 
            lower_lim, 
            upper_lim, 
            alpha=0.4
        )
        plt.legend()
        plt.show()

    
if(__name__ == "__main__"):
    total_regressor = TotalLogisticRegressor()
    pp = pre_processor.PreProcessor(total_regressor.file, filter_date=True)
    total_regressor.dataset = pp.pre_process()
    total_regressor.identifier = 'total_deaths'
    total_regressor.run()
    total_regressor.plot_prediction()