BITBIP_VERSION = 1.0
BITBIP_SITE = $(TOPDIR)/package/bitbip
BITBIP_SITE_METHOD = local

BITBIP_MODULE_MAKE_OPTS = \
    KERNELDIR=$(LINUX_DIR)

$(eval $(kernel-module))
$(eval $(generic-package))
