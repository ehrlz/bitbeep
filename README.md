# BitBip

## Buildroot image
Features:
- root login with password `123`
- ssh server that only accepts root login with password
- Kernel module compiling and manual loading

## Kernel module - Bitbip

Info. obtained from H6 User Manual.

### How to configure PWM functionality

#### GPIO 10 as PWM1 (pulse-width modulation channel 1)
- Port base dir: `0x0300B000`
- PG_CFG1 register controls PG8-PG15. Offset: `0x00CC`
- Each pin has 4 bits. PG10 are bits[11:8]
- Write the PWM1 asociated value: `0x3`

#### Configure PWM1 controller with frequency and duty-cycle
- PWM controller base dir: `0x0300A000`
- Each channel has 20b offset. PWM1: `0x0300A020`
- Control register offset: `0x00`
- Period register offset: `0x04`
- Duty-cycle register offset: `0x08`

## Build
### Install the kernel module with buildroot

1. Create a folder in `package/`
2. Fill it with: 
    - `Config.in`
    - kernel module C code
    - Makefile
    - `bitbip.mk`
3. Add the package to the menu, add `source "package/bitbip/Config.in"` in the most suitable location (recommended *Hardware handling*)
4. Select the package in the buildroot menu with `menu menuconfig`
5. Compile with `make`

### Copy the buildroot generated image in a portable memory (SD card, USB, etc...)
```
sudo dd if=output/images/sdcard.img of=/dev/sdX bs=1M conv=fsync status=progress
sudo sync
```
> Check which sdX device is the portable memory with `lsblk`
### Use

1. Install the kernel module
```
modprobe bitbip
```
2. Check that is loaded
```
lsmod
```
```
dmesg
```
> System is configured to login as root, so no sudo is needed

3. TO BE DOCUMENTED


4. Unload the module
```
modprobe -r bitbip
```