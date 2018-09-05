import pydot
import json
import sys
import datetime
import os
from pprint import pprint

def get_transactions(txid):
	try:
		return transactions[txid]
	except Exception as e:
		return {}

def get_spent_ids(transaction):
	spent_txids = []

	if transaction == {}:
		return spent_txids

	for output in transaction['out']:
		try:
			spent_txids.append(output['spent'])
		except:
			pass

	return spent_txids

def recurcive_search(root_txid,recurcive_max_time):
	target_txids = [root_txid]

	searched_txids = [root_txid]

	edges = []

	for n in range(recurcive_max_time):
		if target_txids == []:
			break
		for target_txid in target_txids[:]:
			target_transaction = get_transactions(target_txid)
			spent_txids = get_spent_ids(target_transaction)

			for txid in spent_txids:
				target_txids.append(txid)
				edges.append([target_txid,txid])

			target_txids = list(set(target_txids))
			target_txids.remove(target_txid)
			searched_txids.append(target_txid)
		print(n)

	return edges

def get_terminate_txids(edges):
	input_txids = [edge[0] for edge in edges]
	output_txids = [edge[1] for edge in edges]
	terminate_txids = []

	for output_txid in output_txids:
		if output_txid in input_txids:
			continue
		terminate_txids.append(output_txid)

	return terminate_txids

block_data_json_path = sys.argv[1]
root_txid = sys.argv[2]
recurcive_max_time = int(sys.argv[3])

try:
	need_svg = int(sys.argv[4])
except:
	need_svg = 0

with open(block_data_json_path,'r') as file:
	transactions = json.load(file)

edges = recurcive_search(root_txid,recurcive_max_time)
terminate_txids = get_terminate_txids(edges)

edge_strings = []

for edge in edges:
	money_value = 0

	for input_transaction in transactions[edge[1]]['in']:

		if input_transaction['tx'] == edge[0]:
			money_value += float(input_transaction['value'])/100000000.0

	edge_strings.append("\"" + edge[0] + '" -> "' + edge[1] + '"' + ' [label="' + str(money_value) + '"];\n')

edge_strings = list(set(edge_strings))

#Make Graph
#Header
dot_data = "digraph G {randir=TB;layout=dot;\n"

#Nodes
dot_data += root_txid + ' [style = "solid,filled",color = red,fontcolor = white];\n'

terminate_txids = list(set(terminate_txids))
for terminate_txid in terminate_txids:
	dot_data += terminate_txid + ' [style = "solid,filled",color = black,fontcolor = white];\n'

#Edges
for edge_string in edge_strings:
	#dot_data += "\"" + edge[0] + '" -> "' + edge[1] + '"' + ';\n'
	dot_data += edge_string
dot_data += '}'

#Make Files
now = datetime.datetime.now()
output_dir = './AnalyzeResults/' + root_txid + '_{0:%Y%m%d_%H_%M_%S}'.format(now) + '/'
os.mkdir(output_dir)

with open(output_dir + 'money_flow.dot','w') as file:
	file.write(dot_data)

with open(output_dir + 'terminate_transaction_list','w') as file:
	for terminate_txid in terminate_txids:
		file.write(terminate_txid + '\n')

if need_svg == 1:
	(graph,) = pydot.graph_from_dot_file(output_dir + 'money_flow.dot')
	graph.write_svg(output_dir + 'money_flow.svg')