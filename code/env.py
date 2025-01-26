import sys
print(sys.executable)
 

import torch  

num_positions=16


print(torch.arange(num_positions))

print(torch.arange(num_positions).expand((1, -1)))
