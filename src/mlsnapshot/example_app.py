import torch
from api import MLSnapshot

@MLSnapshot('snapshots')
def example_function(u, delta, A, B, C, D=None, z=None, deltabias=None, delta_softplus=False):
    return u + delta + A + B + C + (D if D is not None else 0), 10

# Example tensors
u = torch.tensor([1.0])
delta = torch.tensor([0.1])
A = torch.tensor([0.2])
B = torch.tensor([0.3])
C = torch.tensor([0.4])
D = torch.tensor([0.5])
z = None
deltabias = None
delta_softplus = True

# Call the function
output1=example_function(u, delta, A, B, C, D, z, deltabias, delta_softplus)
print(u,delta,A,B,C,D,z,deltabias,delta_softplus)
print(output1)
