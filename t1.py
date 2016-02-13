#!flask/bin/python
from os import path, getcwd, chdir

def print_my_path():
    print('cwd:     {}'.format(getcwd()))
    print('__file__:{}'.format(__file__))
    print('abspath: {}'.format(path.abspath(__file__)))
            
print_my_path()
            
chdir('..')
            
print_my_path()

print(__file__)
print(__name__)
