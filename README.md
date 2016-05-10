# Live example
http://plutec.github.io/smali_graph/
# Installation
```
git clone https://github.com/plutec/smali_graph.git
```
# Execution
First you must generate a json file with your class structure. This can be do with the script **generate_json.py** and passing as argument the folder with the smali code.
```
$ python generate_json.py -s smali_test/
```
Second, open with your browser the file **graph.html** or with double-clicking.

Third, open the json file generated in the first step using the button *LOAD* and the result is this:

![](https://raw.githubusercontent.com/plutec/smali_graph/master/graph.png)

# Credits
- Thanks to D3.js people for their great job.
- Thanks to http://vowl.visualdataweb.org/ team for their ontology graph implementation that we are reusing.

# License
MIT License
