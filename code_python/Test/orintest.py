import torch
import torchvision.models as models
from timeit import timeit
import numpy as np
# import
model = models.resnet50(pretrained=True)
# PyTorch model
torch.save(model, 'resnet.pth')
# random input
data = torch.rand(1,3,224,224)
# ONNX needs data example
torch.onnx.export(model, data, 'resnet.onnx') 
import onnxruntime
# PyTorch model
torch_model = torch.load('resnet.pth')
# ONNX model
onnx_model = onnxruntime.InferenceSession('resnet.onnx',providers=['CUDAExecutionProvider'])
torch_model.to("cuda:0")
torch_data = torch.from_numpy(data).to("cuda:0")
torch_model.eval()
data = np.random.rand(1,3,224,224).astype(np.float32)
torch_data = torch.from_numpy(data)
def torch_inf():
    torch_model(torch_data)
 
def onnx_inf():
    onnx_model.run(None,{
                onnx_model.get_inputs()[0].name: data
           })
n = 200
#warmup
#for i in range(1,100):
#    torch_inf()
torch_t = timeit(lambda : torch_inf(), number=n)/n
onnx_t = timeit(lambda : onnx_inf(), number=n)/n
 
print(f"PyTorch {torch_t} VS ONNX {onnx_t}")