import taso as ts
import onnx
import sys

# convert serialized taso graph to onnx graph
# to run: python load_model.py < bts.model
# you can serialize a taso graph with taso.export_to_file()

ac_mode = {
  ts.get_activation_mode("NONE"): "NONE",
  ts.get_activation_mode("SIGMOID"): "SIGMOID",
  ts.get_activation_mode("RELU"): "RELU",
  ts.get_activation_mode("TANH"): "TANH",
}

graph = ts.new_graph()
guid_node = dict()

# can replace while true with walrus in python 3.8
while True:
  l = sys.stdin.readline()
  if not l:
    break
  guid = int(l.strip())
  op = int(sys.stdin.readline().strip())
  deps = [int(s.split(':')[0]) for s in sys.stdin.readline().strip().split(',')]
  params = [int(s) for s in sys.stdin.readline().strip().split(',')]

  node = {
    'Input':     lambda: graph.new_input(dims=tuple(params)),
    'Weight':    lambda: graph.new_weight(dims=tuple(params)),
    # activation for matmul
    'Matmul':    lambda: graph.matmul( guid_node[deps[0]], guid_node[deps[1]], activation=ac_mode[params[0]]),
    'Reshape':   lambda: graph.reshape(guid_node[deps[0]], shape=tuple(params)),
    # perm, shuffle
    'Transpose': lambda: graph.transpose(guid_node[deps[0]], perm=(1,0,2), shuffle=True),
    'Relu':      lambda: graph.relu(guid_node[deps[0]]),
  }[ts.op_table[op]]
  guid_node[guid] = node()

onnx_model = ts.export_onnx(graph)
onnx.save(onnx_model, "out.onnx")
