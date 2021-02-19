import os
# imports all .py modules from scripts
imports = list(set([file.split('.')[0] for file in os.listdir('scripts/')][3:]))
#not using verify script... for now
#TODO: refactor verify.py to work with repo program flow
imports.remove('verify')
imports.remove('__init__')
imports.remove('__pycache__')
print(imports)
__all__ = imports

