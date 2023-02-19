import environ
import os

env = environ.Env()
environ.Env.read_env()
print(env('NAME'))
