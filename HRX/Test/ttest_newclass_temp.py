import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
model_dict=load_all()
print(model_dict['IDClassifier'].classify('嗯嗯'))

