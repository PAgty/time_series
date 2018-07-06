import os

from flask import Flask
import json
import redis
import pickle
from algorithms import * 
from utility import *
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

algs = ['ARIMA']
alg_param = {'ARIMA':['P','I','Q']}
# with open('indexing','rb') as f:
#     index=pickle.load(f)


query_name_time_series = {}
selected_time_series = ""
selected_alg = ""
app = Flask(__name__)
db = redis.StrictRedis(host='localhost', port=6379, db=0,decode_responses=True)

index = json.loads(db.get('indexing'))

@app.route('/')
def main_page():
	global query_name_time_series
	global selected_alg	
	global selected_time_series	
	if request.args:
		if request.args.get('algorithms'):
			selected_alg = request.args['algorithms']
			selected_time_series = request.args.get('tags')
			# print(selected_time_series)
			return render_template('main_page.html',values = selected_time_series,selected_algs = selected_alg, algs = algs,params = alg_param[selected_alg])
		else:
			tags = request.args['search_tags']
			query_name_time_series = query(tags,index,db)
			if(query_name_time_series):
				return render_template('main_page.html',values = query_name_time_series,algs = algs)
			else:
				return render_template('main_page.html',values = False)
	return render_template('main_page.html')

@app.route('/result',methods=['GET'])
def result():
	global selected_alg
	global selected_time_series
	index_key = index[selected_time_series]
	v = json.loads(db.get(index_key))
	print(v)
	operator = request.args['operator']
	data_type = request.args['data_type']
	request_time = request.args['frequency']
# def apply(algorithm,params,data,operator,data_type,time,weight):
	if is_valid(v):
		predicted_data = apply(algorithm = selected_alg,params = request.args,data = v,operator =operator,data_type = data_type,time = request_time)
		return render_template('result.html',values = predicted_data)
	else:
		return render_template('result.html',values = {'no/invalid data':'no/invaid data'})

@app.route('/data',methods =['POST'])
def get_data():
	showed_data_name = request.form.get('data_name')
	if showed_data_name:
		data_value = get_from_database(showed_data_name,db,index)
		return render_template('data.html',values = data_value)

@app.route('/transform', methods = ['POST'])
def get_transform():
	global selected_time_series
	data_type = ['aggregate','average']
	showed_data_name = request.form.get('data_name')
	selected_time_series = showed_data_name 
	print(selected_time_series)
	if showed_data_name:
		data_value = get_from_database(showed_data_name,db,index)
		# get frequent
		freq_list = get_frequent(data_value)
		return render_template('transform.html',values = freq_list,type = data_type)

if __name__ == '__main__':
    app.run()
