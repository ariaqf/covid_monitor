# Function models to be used in COVID assessment
#
import math

def logistic_model(x, P, k):
    return P/(1- (1 -P)*math.e**(-k*x))

def logistic_model2(x, P, k, x0):
    return P/(1 + math.e**(-k*(x-x0)))