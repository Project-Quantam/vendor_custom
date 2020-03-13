# Carrier Settings.
PRODUCT_PACKAGES += \
    CarrierSettings

PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,*,vendor/custom/prebuilt/product/etc/CarrierSettings,$(TARGET_COPY_OUT_PRODUCT)/etc/CarrierSettings)

# SIM Toolkit.
PRODUCT_PACKAGES += \
    CellBroadcastReciever \
    Stk
