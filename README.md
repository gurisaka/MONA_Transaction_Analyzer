# MonaCoin Transaction Analyzer
![5](https://user-images.githubusercontent.com/36693422/45124926-36b0a080-b1a7-11e8-9ea9-3db4826b45e1.png)
### Useage
* `python3 get_transaction_tree_and_terminate_transactions.py [transaction_json] [transaction_id] [recursive_time] [svg_output]`  
transaction_jsonは https://github.com/gurisaka/MonaCoin_Block_Getter で作成したトランザクションデータのパスを入力する。transaction_idは探索の始端トランザクションを入力する。recursive_timeは探索する階層の深さを決める。svg_outputは1を指定するとSVGファイルも出力される。0を指定することでキャンセルできる。  
基本的に階層が深くなるほどSVGファイルの出力が絶望的なまでに遅くなるので、100階層以上を設定する場合はSVGファイルの出力を切ることも考慮すべき。
出力されるのは「トランザクションの繋がりと送金量の.dotファイルと.svgファイル」、「末端のトランザクションidのリスト」

* `python3 get_transaction_tree_and_terminate_transactions.py MONA_Transactions.json 9b09....116cc 100 1`

### Requirements
 * pydot

### Author
#####  https://twitter.com/GuriTech.com
