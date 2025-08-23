echo "Putting the relevant files into the Buildroot context to generate the final image"

cp .config buildroot/.config
cp bitbeep.py buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/bitbeep.py
cp buildroot_aux_files/sshd_config buildroot/board/orangepi/orangepi-zero3/rootfs-overlay/etc/ssh/sshd_config

echo "Files copied to Buildroot context"