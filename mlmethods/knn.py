import numpy as np
from sklearn import preprocessing, neighbors
from sklearn.model_selection import train_test_split
import convert

unprocessed_data = convert.convert()

for item in unprocessed_data:
    print(item)
