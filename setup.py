'''
The setup.py file is an essential part for packaging and distributing 
Python projects. It is used by setuptools (or distutils in older Python 
versions) to define the configuration of your project, such as its 
metadata, dependencies, and more.
'''


from setuptools import find_packages, setup #Findes the init files and considers the folder with that file as a package
from typing import List

def get_requirements()->List[str]:
    '''
    This function will return the list of reqiremetns
    '''
    requirement_lst:List[str] = []
    try:
        with open('requirements.txt','r') as file:
            #reads the line from lines
            lines = file.readlines()
            #proess each line
            for line in lines:
                requirement = line.strip()
                ##ignore empty lines and -e .
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found")
    return requirement_lst
print(get_requirements())

setup(
    name="Soteria-Network-Security",
    version="0.0.1",
    author="Aviral Soni",
    author_email="aviralsoni22@gmail.com",
    packages=find_packages(),
    install_reqires=get_requirements()
)