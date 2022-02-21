import pickle
import time

import torch

torch.rand([10, 10]).cuda()
time.sleep(30)

result = {
    "suite_id": 233,
    "results": [{"result": {"value": float(dim * dim) / 1024 / 1024}}]
}

print(pickle.dumps(result))
