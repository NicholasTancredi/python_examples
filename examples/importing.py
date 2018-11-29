import package
import package.subpackage as subpackage
from package import Package
from package.subpackage import Subpackage
print('package:', package)
print('subpackage:', subpackage)
print('Package:', Package)
print('Subpackage:', Subpackage)

# cython test import and run
from cython_array_sum import array_sum
import numpy as np
print('array_sum:', array_sum(np.random.randn(10, 10)))