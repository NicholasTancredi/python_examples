# How to install
```sh
bash install.sh
```
Calling this in your terminal will run **start_pipenv.sh** and **build_cython.sh** which will install all the python requirements, activate the environment, and finally build the cython files.

### Thats it, your done installing.
#### If you want you can do this without the bash script, see below.

# How to manually install
## Install packages
This ignores *pre-versions* error message, and uses the terminal python. (These are issues I experience on my local system often). Otherwise the 
```sh
pipenv install --pre --python=$(which python)
```
## Activate the environment
```sh
pipenv shell
```
## Build the cython files
```sh
python setup.py build_ext --inplace
```
## Useful commands
### pipenv run
This lets you run commands as if you where in the pipenv environment.
```sh
pipenv run pip install -r requirements.txt 
```
#### Equivalent to:
```sh
pipenv shell
pip install -r requirements.txt
exit
```