
import numpy as np


array = [0, 1, 2, 3, 4]
n_elements = len(array)
containers = []
i = 0

for element in array:
	containers.append(element)
	i += 1
	if i >= n_elements:
		break

print(containers[:i])