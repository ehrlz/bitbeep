echo "Putting the relevant files into the Buildroot context to generate the final image"

cp .config buildroot/.config

mkdir -p buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/etc/ssh
cp buildroot_aux_files/sshd_config buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/etc/ssh/sshd_config
cp bitbeep.py buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/bitbeep.py

mkdir -p buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/usr/share/bitbeep
cp -r songs buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/usr/share/bitbeep/songs

echo "Files copied to Buildroot context"