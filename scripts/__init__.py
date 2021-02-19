import os
# imports all .py modules from scripts
imports = list(set([file.split('.')[0] for file in os.listdir('scripts/') if file.endswith('.py')]))
#not using verify script... for now
#TODO: refactor verify.py to work with repo program flow
imports.remove('verify')
imports.remove('__init__')
print(imports)
__all__ = imports

