from imaplib import Commands
import os 
import subprocess
from concurrent.futures import ThreadPoolExecutor
def get_env_var(var_name):
    variable = os.environ.get(var_name)
    if variable is None or variable == "":
        raise Exception(f"Missing environment variable: {var_name}")
    return variable

