import torch

# Check if CUDA is available
cuda_available = torch.cuda.is_available()
print(f"CUDA available: {cuda_available}")

# Check the PyTorch version
print(f"PyTorch version: {torch.__version__}")

# Check the CUDA version PyTorch is built with
if cuda_available:
    print(f"CUDA Version: {torch.version.cuda}")
else:
    print("CUDA is not available with this PyTorch installation.")
