import taso as ts
import onnx
import sys

# convert serialized taso graph to onnx graph
# to run: python load_model.py < your.model
# output is stored in `out.onnx`

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
  deps = [(int(s.split(':')[0]), int(s.split(':')[1])) for s in sys.stdin.readline().strip().split(',')]
  params = [int(s) for s in sys.stdin.readline().strip().split(',')]

  print(op)
  print(ts.op_table[op])
  node = {
    'Input':     lambda: [graph.new_input(dims=tuple(params))],
    'Weight':    lambda: [graph.new_weight(dims=tuple(params))],
    'Matmul':    lambda: [graph.matmul(guid_node[deps[0][0]][deps[0][1]], guid_node[deps[1][0]][deps[1][1]], activation=ac_mode[params[0]])],
    'Reshape':   lambda: [graph.reshape(guid_node[deps[0][0]][deps[0][1]], shape=tuple(params))],
    'Transpose': lambda: [graph.transpose(guid_node[deps[0][0]][deps[0][1]], perm=tuple(params[:3]), shuffle=params[3])],
    'Relu':      lambda: [graph.relu(guid_node[deps[0][0]][deps[0][1]])],
    'Split':     lambda: graph.split(guid_node[deps[0][0]][deps[0][1]], axis=params[0], sizes=params[1:]),
  }[ts.op_table[op]]
  guid_node[guid] = node()

onnx_model = ts.export_onnx(graph)
onnx.save(onnx_model, "out.onnx")
