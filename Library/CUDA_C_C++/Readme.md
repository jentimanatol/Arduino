# An Even Easier Introduction to CUDA

## Overview
This document provides a simplified introduction to CUDA, NVIDIA's parallel computing platform and programming model. CUDA enables developers to use the power of GPUs for high-performance computing. This guide covers fundamental CUDA concepts, basic programming examples, and performance optimizations.

<img src="CUDA_Cube_1K.jpg" alt="CUDA Cube Image" width="500">

## Prerequisites
To follow along with this tutorial, you will need:
- A CUDA-capable GPU (any NVIDIA GPU should work)
- A computer running Windows, macOS, or Linux
- The CUDA Toolkit installed
- A C++ compiler (e.g., `g++`, `clang++`, or MSVC)

Alternatively, you can use a cloud-based GPU instance from AWS, Azure, or IBM SoftLayer.

## Getting Started

### Basic C++ Example (CPU Implementation)
The following C++ program adds elements of two arrays:

```cpp
#include <iostream>
#include <math.h>

// Function to add the elements of two arrays
void add(int n, float *x, float *y) {
    for (int i = 0; i < n; i++)
        y[i] = x[i] + y[i];
}

int main(void) {
    int N = 1<<20; // 1M elements
    float *x = new float[N];
    float *y = new float[N];

    // Initialize arrays
    for (int i = 0; i < N; i++) {
        x[i] = 1.0f;
        y[i] = 2.0f;
    }

    // Perform addition
    add(N, x, y);

    // Check for errors
    float maxError = 0.0f;
    for (int i = 0; i < N; i++)
        maxError = fmax(maxError, fabs(y[i] - 3.0f));
    std::cout << "Max error: " << maxError << std::endl;

    // Free memory
    delete[] x;
    delete[] y;

    return 0;
}
```

Compile and run with:
```sh
clang++ add.cpp -o add
./add
```

### Moving to CUDA
To run the computation on a GPU, convert the `add` function into a CUDA kernel using `__global__`:

```cpp
__global__
void add(int n, float *x, float *y) {
    for (int i = 0; i < n; i++)
        y[i] = x[i] + y[i];
}
```

### Memory Allocation in CUDA
CUDA provides Unified Memory, accessible by both the CPU and GPU:

```cpp
float *x, *y;
cudaMallocManaged(&x, N * sizeof(float));
cudaMallocManaged(&y, N * sizeof(float));
```

Deallocate memory using:
```cpp
cudaFree(x);
cudaFree(y);
```

### Launching a CUDA Kernel
To execute the kernel, use the triple angle bracket syntax:
```cpp
add<<<1, 1>>>(N, x, y);
cudaDeviceSynchronize();
```

### Parallel Execution
Instead of running a single thread, launch multiple threads for better performance:

```cpp
__global__
void add(int n, float *x, float *y) {
    int index = blockIdx.x * blockDim.x + threadIdx.x;
    int stride = blockDim.x * gridDim.x;
    for (int i = index; i < n; i += stride)
        y[i] = x[i] + y[i];
}
```

Launch with:
```cpp
int blockSize = 256;
int numBlocks = (N + blockSize - 1) / blockSize;
add<<<numBlocks, blockSize>>>(N, x, y);
cudaDeviceSynchronize();
```

### Compiling and Running CUDA Code
Save the code as `add.cu` and compile using the CUDA compiler:
```sh
nvcc add.cu -o add_cuda
./add_cuda
```

## Performance Profiling
To measure performance, use `nvprof`:
```sh
nvprof ./add_cuda
```
This provides execution time and resource utilization.

## Summary of Performance Gains
| Version            | Laptop (GT 750M) | Server (Tesla K80) |
|--------------------|-----------------|---------------------|
| 1 CUDA Thread     | 411ms (30.6 MB/s) | 463ms (27.2 MB/s)   |
| 1 CUDA Block      | 3.2ms (3.9 GB/s)  | 2.7ms (4.7 GB/s)    |
| Many CUDA Blocks  | 0.68ms (18.5 GB/s)| 0.094ms (134 GB/s)  |

## Next Steps
To deepen your knowledge, explore the following:
- **CUDA Toolkit Documentation**: Programming Guide, Best Practices Guide
- **Advanced Topics**:
  - Performance Metrics in CUDA
  - Efficient Memory Access Patterns
  - Shared Memory Optimization
  - Multi-GPU Programming
- **Online Courses**:
  - NVIDIA Deep Learning Institute (DLI)
  - Udacity CUDA Programming Course

CUDA is a powerful tool for accelerating computation-intensive applications like deep learning, simulations, and image processing. Experiment with the provided code and optimize for better performance!

---
*Original content adapted from "An Even Easier Introduction to CUDA" by Mark Harris (NVIDIA).*

