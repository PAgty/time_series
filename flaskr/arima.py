from algorithms import algorithm
from statsmodels.tsa.arima_model import ARIMA
from pandas import datetime
start_index = datetime(2018, 6, 30)
end_index = datetime(2018, 12, 31)
# p,q,i predict_time
class arima(algorithm):
	data = {}
	output = []
	def __init__(self,params):
		for k,v in params.items():
			setattr(self,k,int(v))

	def fit(self,data):
		# get all parameters prepared
		self.data = self.preprocess(data)
		if not self.P:
			self.P = self.Get_P()
		if not self.I:
			self.I = self.Get_I()
		if not self.Q:
			self.Q = self.Get_Q()

		# do the fitting
		values = []
		parameters =[self.P,self.I,self.Q]
		for x in self.data.values():
			val = self.convert(x)
			if(val):
				values.append(val)
		# print(values)
		self.model = ARIMA(values, order=parameters)
		self.model_fit = self.model.fit(disp=0)
		return self.model_fit

	def predict(self):

		self.output = self.model_fit.forecast(self.predict_time)
		# self.output = self.model_fit.predict(start = start_index,end = end_index)
		# print(self.output)
		k = 0
		for i in self.output[0]:
			k = k + 1
			s = 'perdict_next_{}_quarter'.format(k)
			self.data[s] = i
		return self.data



