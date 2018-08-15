import sys,os
loader_path = '../../classifier/loader/'
sys.path.append(loader_path)
from loader import load_all
tt=load_all()
print(tt['IfKnowDebtor'].classify('你说什么'))