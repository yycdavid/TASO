import taso
import onnx
import argparse
import time

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="Path to input ONNX file", required=True)

args = parser.parse_args()

#graph = taso.load_onnx("/home/ubuntu/taso/onnx/squeezenet1.1.onnx")
#graph = taso.load_onnx("/home/ubuntu/taso/onnx/bertsquad10.onnx")
graph = taso.load_onnx(args.file)
#print("input time")
#print(graph.run_time())
#graph = xflow.load("/home/ubuntu/resnext-101.onnx") 
#graph = xflow.load("/home/ubuntu/ONNXModel/inception_v2/model.onnx")
#start = time.time()
#new_graph = taso.optimize(graph, alpha = 1.0, budget = 100, print_subst = True)
#end = time.time()
#print(end - start)
#print("opt time")
#print(new_graph.run_time())
#onnx_model = taso.export_onnx(new_graph)
#onnx.checker.check_model(onnx_model)
#onnx.save(onnx_model, "{}.taso.onnx".format(args.file))
#print("exporting")
taso.export_to_file(graph, b"/usr/TASO/examples/out.model")
