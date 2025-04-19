
import os


FG_HOME = "fg/validator"

def home_path():

    return FG_HOME

def  jdk_path():
    return os.path.join(FG_HOME, "jdk")