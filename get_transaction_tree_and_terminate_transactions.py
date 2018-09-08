import pydot
import json
import sys
import datetime
import os
from pprint import pprint


class TransactionsAnalyzer:
	def __init__(self, transaction_data_json_path):
		self.__transactions = {}
		self.__load_transaction_data(transaction_data_json_path)

	# Load Data
	def __load_transaction_data(self, transaction_data_json_path):
		with open(transaction_data_json_path, 'r') as file:
			self.__transactions = json.load(file)

	# Get Transaction Information
	def __get_transaction(self, txid):
		if txid in self.__transactions.keys():
			return self.__transactions[txid]
		else:
			return {}

	@classmethod
	def __get_spent_txids(cls, transaction):
		spent_txids = []

		for output in transaction['out']:
			if 'spent' in output.keys():
				spent_txids.append(output['spent'])

		return spent_txids

	@classmethod
	def __get_terminate_txids(cls, edges):
		input_txids = [edge[0] for edge in edges]
		output_txids = [edge[1] for edge in edges]
		terminate_txids = []

		for output_txid in output_txids:
			if output_txid in input_txids:
				continue
			terminate_txids.append(output_txid)

		return terminate_txids

	def __get_transactions_edges(self, root_txid, search_depth):
		search_target_txids = [root_txid]
		searched_txids = [root_txid]

		edges = []

		for depth in range(search_depth):
			if search_target_txids == []:
				break

			for search_target_txid in search_target_txids[:]:
				search_target_transaction = self.__get_transaction(search_target_txid)

				if search_target_transaction != {}:
					spent_txids = TransactionsAnalyzer.__get_spent_txids(search_target_transaction)
				else:
					spent_txids = []

				for spent_txid in spent_txids:
					search_target_txids.append(spent_txid)
					edges.append([search_target_txid, spent_txid])

				search_target_txids = list(set(search_target_txids))
				search_target_txids.remove(search_target_txid)
				searched_txids.append(search_target_txid)

		return edges

	# Make Output File
	def __make_dot_file(self, root_txid, edges, terminate_txids, output_path):
		# Make Edges
		edge_strings = []
		for edge in edges:
			money_value = 0

			for input_transaction in self.__transactions[edge[1]]['in']:

				if input_transaction['tx'] == edge[0]:
					money_value += float(input_transaction['value'])/100000000.0

			edge_strings.append("\"" + edge[0] + '" -> "' + edge[1] + '"' + ' [label="' + str(money_value) + '"];\n')

		edge_strings = list(set(edge_strings))

		# File Header
		dot_data = "digraph G {randir=TB;layout=dot;\n"
		dot_data += root_txid + ' [style = "solid,filled",color = red,fontcolor = white];\n'

		# Terminate Transactions
		terminate_txids = list(set(terminate_txids))
		for terminate_txid in terminate_txids:
			dot_data += terminate_txid + ' [style = "solid,filled",color = black,fontcolor = white];\n'

		# Edges
		for edge_string in edge_strings:
			dot_data += edge_string

		# File Tail
		dot_data += '}'

		with open(output_path, 'w') as file:
			file.write(dot_data)

	@classmethod
	def __make_terminate_transactions_list_file(cls, terminate_txids, output_path):
		with open(output_path, 'w') as file:
			for terminate_txid in terminate_txids:
				file.write(terminate_txid + '\n')

	@classmethod
	def __make_svg_file(self, dot_file_path, output_path):
		(graph,) = pydot.graph_from_dot_file(dot_file_path)
		graph.write_svg(output_path)

	def run_analyzer(self, root_txid, search_depth, dot_file_path, terminate_transactions_list_path, svg_file_path):
		edges = self.__get_transactions_edges(root_txid, search_depth)
		terminate_txids = self.__get_terminate_txids(edges)
		self.__make_dot_file(root_txid, edges, terminate_txids, dot_file_path)
		TransactionsAnalyzer.__make_terminate_transactions_list_file(terminate_txids,terminate_transactions_list_path)

		if svg_file_path != '':
			TransactionsAnalyzer.__make_svg_file(dot_file_path, svg_file_path)


if __name__ == '__main__':
	transactions_data_json_path = sys.argv[1]
	root_txid = sys.argv[2]

	if '-r'in sys.argv:
		recurcive_max_time = int(sys.argv[sys.argv.index('-r') + 1])
	else:
		recurcive_max_time = 100

	if '-s' in sys.argv:
		svg_output_flag = True
	else:
		svg_output_flag = False

	#Make File Paths
	now = datetime.datetime.now()
	output_dir = './AnalyzeResults/' + root_txid + '_{0:%Y%m%d_%H_%M_%S}'.format(now) + '/'
	os.mkdir(output_dir)

	dot_file_path = output_dir + 'money_flow.dot'
	terminate_transactions_list_path = output_dir + 'terminate_transaction_list.txt'
	
	if svg_output_flag == True:
		svg_file_path = output_dir + 'money_flow.svg'
	else:
		svg_file_path = ''

	transaction_analyzer = TransactionsAnalyzer(transactions_data_json_path)
	transaction_analyzer.run_analyzer(root_txid, recurcive_max_time, dot_file_path, terminate_transactions_list_path, svg_file_path)