# MonaCoin Transaction Analyzer
### Useage
* `python3 get_transaction_tree_and_terminate_transactions.py [transaction_json] [transaction_id] [recursive_time] [svg_output]`
transaction_jsonは https://github.com/gurisaka/MonaCoin_Block_Getter で作成したトランザクションデータのパスを入力する。transaction_idは探索の始端トランザクションを入力する。recursive_timeは探索する階層の深さを決める。svg_outputは1を指定するとSVGファイルも出力される。0を指定することでキャンセルできる。  
基本的に階層が深くなるほどSVGファイルの出力が絶望的なまでに遅くなるので、100階層以上を設定する場合はSVGファイルの出力を切ることも考慮すべき。
出力されるのは「トランザクションの繋がりと送金量の.dotファイルと.svgファイル」、「末端のトランザクションidのリスト」

* Sample : `python3 get_transaction_tree_and_terminate_transactions.py MONA_Transactions.json 9b09....116cc 100 1`

### Requirements
 * pydot

### Author
#####  https://twitter.com/GuriTech.com
