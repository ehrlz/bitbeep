#include <linux/init.h>
#include <linux/module.h>
#include <linux/version.h>
#include <linux/kfifo.h>
#include <linux/i8253.h>
#include <linux/cdev.h>
#include <linux/device.h>
#include <linux/fs.h>
#include <linux/wait.h>
#include <linux/sched.h>
#include <linux/ioctl.h>
#include <linux/io.h>
#include <asm/uaccess.h>

// hw mem region adresses
#define PWM 0x0300A000

// hw mem region offsets
#define PCCR01 0x0020 // PWM01 Clock Configuration Register
#define PER 0x0040 // PWM Enable Register
#define PCR1 0x0080 // PWM Control Register
#define PPR1 0x0084 // PWM Period Register
#define PCNTR 0x0088 // PWM Counter Register

// hw mem region pointers
void *pwm;
void *pccr01;
void *per;
void *pcr1;
void *ppr1;
void *pcntr;

void hw_init(void);
void hw_exit(void);
void set_spkr_frequency(unsigned int frequency);
void spkr_on(void);
void spkr_off(void);

__u32 pins;

static int __init bitbip_init(void)
{
	hw_init();
	//set_spkr_frequency(440); // Establecer frecuencia a 440 Hz (La)
	spkr_on();

	printk(KERN_INFO "Module loaded\n");
	return 0;
}

static void __exit bitbip_exit(void)
{
	spkr_off();
	hw_exit();
	printk(KERN_INFO "Module unloaded\n");
}

void hw_init(void)
{
	pwm = ioremap(PWM, 1024); // PWM mem region
	if (pwm == NULL) {
		printk(KERN_ERR "Couldn't remap PWM\n");
	}

	pccr01 = pwm + PCCR01;
	per = pwm + PER;
	pcr1 = pwm + PCR1;
	ppr1 = pwm + PPR1;
	pcntr = pwm + PCNTR;

	// clock config
	// ...0 01.1 0100 -> clock source OSC24M (24MHz) | PWM1 clock bypassed to PWM1 output | PWM1 clock gating enabled | clock divide by 16
	iowrite32(0x0000000C, pccr01);
	iowrite32(0x00000000, pcr1); // PWM prescal to 1

	// pwm config
	iowrite32(0x00000000, pcr1); // PWM mode cycle | PWM high mode
	iowrite32(0x0D5006A8, ppr1); // PWM duty cycle (A4 -> 24MHz/16 / 440Hz is entire cycle: active cycle is 50%)
}

void hw_exit(void)
{
	iounmap(pwm);
	printk(KERN_INFO "hw resources unloaded\n");
}

void spkr_on(void)
{
    pins = ioread32(per);
    iowrite32(pins | 0x00000001, per); // PWM1 enable
}

void spkr_off(void)
{
    pins = ioread32(per);

	iowrite32(pins & 0xFFFFFFFE, per); // PWM1 disable
}

module_init(bitbip_init);
module_exit(bitbip_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Elías Herrero");
