# C Kernel Module

A simple Linux kernel module that provides a proc interface for basic arithmetic operations.

## Prerequisites

Install kernel headers and development tools:

```bash
# On Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential linux-headers-$(uname -r)

# On CentOS/RHEL
sudo yum install kernel-devel kernel-headers gcc make

# On Fedora
sudo dnf install kernel-devel kernel-headers gcc make
```

## Build and Load

Build the kernel module:

```bash
make
```

Load and test the module:

```bash
# Load the module
sudo insmod hello_kernel.ko

# Check kernel messages
dmesg | tail

# Test the module
echo "+ 5 3" | sudo tee /proc/hello_kernel
cat /proc/hello_kernel

echo "* 4 7" | sudo tee /proc/hello_kernel
cat /proc/hello_kernel

# Unload the module
sudo rmmod hello_kernel
```

Or use the convenience target:

```bash
make test
```

## Testing

Run unit tests:

```bash
gcc -o test_kernel_module test_kernel_module.c
./test_kernel_module
```

Run tests with coverage:

```bash
gcc -o test_kernel_module test_kernel_module.c --coverage
./test_kernel_module
gcov test_kernel_module.c
```

This will generate coverage information showing which parts of the code were tested.

## Clean

Clean build artifacts:

```bash
make clean
```
