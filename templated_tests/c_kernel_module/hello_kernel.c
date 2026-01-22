#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/proc_fs.h>
#include <linux/uaccess.h>

#define PROC_NAME "hello_kernel"
#define BUFFER_SIZE 256

static char proc_buffer[BUFFER_SIZE];
static int proc_buffer_size = 0;

static int add_numbers(int a, int b) {
    return a + b;
}

static int multiply_numbers(int a, int b) {
    return a * b;
}

static ssize_t proc_read(struct file *file, char __user *user_buf, size_t count, loff_t *pos) {
    if (*pos > 0 || proc_buffer_size == 0)
        return 0;
    
    if (copy_to_user(user_buf, proc_buffer, proc_buffer_size))
        return -EFAULT;
    
    *pos += proc_buffer_size;
    return proc_buffer_size;
}

static ssize_t proc_write(struct file *file, const char __user *user_buf, size_t count, loff_t *pos) {
    char input_buffer[BUFFER_SIZE];
    int a, b;
    char operation;
    
    if (count >= BUFFER_SIZE)
        return -EINVAL;
    
    if (copy_from_user(input_buffer, user_buf, count))
        return -EFAULT;
    
    input_buffer[count] = '\0';
    
    if (sscanf(input_buffer, "%c %d %d", &operation, &a, &b) == 3) {
        int result;
        switch (operation) {
            case '+':
                result = add_numbers(a, b);
                break;
            case '*':
                result = multiply_numbers(a, b);
                break;
            default:
                proc_buffer_size = snprintf(proc_buffer, BUFFER_SIZE, "Invalid operation\n");
                return count;
        }
        proc_buffer_size = snprintf(proc_buffer, BUFFER_SIZE, "%d %c %d = %d\n", a, operation, b, result);
    } else {
        proc_buffer_size = snprintf(proc_buffer, BUFFER_SIZE, "Usage: <+|*> num1 num2\n");
    }
    
    return count;
}

static const struct proc_ops proc_ops = {
    .proc_read = proc_read,
    .proc_write = proc_write,
};

static int __init hello_init(void) {
    proc_create(PROC_NAME, 0666, NULL, &proc_ops);
    proc_buffer_size = snprintf(proc_buffer, BUFFER_SIZE, "Hello Kernel Module loaded!\nUsage: echo \"+ 5 3\" > /proc/hello_kernel\n");
    printk(KERN_INFO "Hello kernel module loaded\n");
    return 0;
}

static void __exit hello_exit(void) {
    remove_proc_entry(PROC_NAME, NULL);
    printk(KERN_INFO "Hello kernel module unloaded\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Coverage AI");
MODULE_DESCRIPTION("A simple kernel module for testing");
MODULE_VERSION("0.1");
