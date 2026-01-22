obj-m += hello_kernel.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean

test:
	sudo insmod hello_kernel.ko
	dmesg | tail
	sudo rmmod hello_kernel
	dmesg | tail

install:
	sudo insmod hello_kernel.ko

uninstall:
	sudo rmmod hello_kernel
