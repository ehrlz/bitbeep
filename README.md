# BitBeep

Minimal application that allows an OrangePiZero3 board to play music with a buzzer in the PC5 pin.


For that purpose, a minimal linux image is built using [Buildroot](https://github.com/buildroot/buildroot) that contains the necessary components.

## Buildroot image
Features:
- root login with password `123`
- ssh server that only accepts root login with password
- Python3
- libgpiod to manage gpio pins
- Singer python script

## Install

The image can be downloaded from the last release or can be built

## Use
Connecting through ssh to the board, execute the python script

```
cd /
python3 bitbeep.py <song_file.txt>
```
> There are songs available at `/usr/share/bitbeep/songs`

## Build

### 1. Download buildroot
```
git pull git@github.com:buildroot/buildroot.git
```
> Check carefully buildroot requirements. Unix system is recommended

### 2. Copy relevant files in buildroot to generate the final image
```
./utilities/files_to_buildroot.sh
```
> Utilities must be executed from bitbeep root directory

### 3. Generate the linux image
```
cd buildroot
make
```

### 4. Add the GPIO config to the device-tree configuration and rebuild
```
cd ..
cp buildroot_aux_files/sun50i-h618-orangepi-zero3.dts buildroot/output/build/linux-6.12.6/arch/arm64/boot/dts/allwinner/sun50i-h618-orangepi-zero3.dts
cd buildroot
make
```
> This configuration activates the PC5 GPIO pin. Minor adjustments to the [linux kernel file](https://github.com/torvalds/linux/blob/master/arch/arm64/boot/dts/allwinner/sun50i-h618-orangepi-zero3.dts)

### 5. Flash the buildroot generated image in a portable memory (SD card, USB, etc...)
```
sudo dd if=output/images/sdcard.img of=/dev/sdX bs=1M conv=fsync status=progress
sudo sync
```
> Check which sdX device is the portable memory with `lsblk`
