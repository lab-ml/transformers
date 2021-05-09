import torch
import torch.autograd
from labml_helpers.module import Module


class GradientPenalty(Module):
    def __call__(self, x: torch.Tensor, f: torch.Tensor):
        batch_size = x.shape[0]
        gradients, *_ = torch.autograd.grad(outputs=f,
                                            inputs=x,
                                            grad_outputs=f.new_ones(f.shape),
                                            create_graph=True,
                                            only_inputs=True)

        gradients = gradients.reshape(batch_size, -1)
        norm = gradients.norm(2, dim=-1)
        return torch.mean((norm - 1) ** 2)
