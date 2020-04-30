import numpy as np
import math
from Renyi_entropy_functions import *

data = get_data_in_column()
dec = ask_for_dec()
data = dataprocess(data, dec)

vec_P = vec_P_generate(data)

alpha = ask_for_alpha()

print_entropy(alpha, vec_P)