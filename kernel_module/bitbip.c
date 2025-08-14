#include <linux/module.h>
#include <linux/kernel.h>

static int __init bitbip_init(void) {
    printk(KERN_INFO "Hola desde mi módulo\n");
    return 0;
}

static void __exit bitbip_exit(void) {
    printk(KERN_INFO "Adiós desde mi módulo\n");
}

module_init(bitbip_init);
module_exit(bitbip_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Elías Herrero");
