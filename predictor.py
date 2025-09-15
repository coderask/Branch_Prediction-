#generate accuracy from each predictor:
import parser #parser.py
from learning import gShare_prediction #gShare_prediction.py
import learning.Bimodal_prediction as bimodal_prediction #Bimodal_prediction.py
import importlib.util
import sys

# Import 1-bit prediction
spec1 = importlib.util.spec_from_file_location("one_bit_prediction", "learning/1-bit-prediction.py")
one_bit_prediction = importlib.util.module_from_spec(spec1)
spec1.loader.exec_module(one_bit_prediction)

# Import 2-bit prediction  
spec2 = importlib.util.spec_from_file_location("two_bit_prediction", "learning/2-bit-prediction.py")
two_bit_prediction = importlib.util.module_from_spec(spec2)
spec2.loader.exec_module(two_bit_prediction)
# Import the trace data from parser.py
trace, branches_map = parser.generate_branch_trace()

print("=== GShare Prediction ===")
print(gShare_prediction.gShare_prediction(trace))

print("\n=== Bimodal Prediction ===")
print(bimodal_prediction.bimodal_prediction(trace))

print("\n=== 1-bit Prediction ===")
print(one_bit_prediction.one_bit_prediction(trace))

print("\n=== 2-bit Prediction ===")
print(two_bit_prediction.two_bit_prediction(trace))


