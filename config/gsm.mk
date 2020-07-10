# Carrier Settings.
PRODUCT_PACKAGES += \
    CarrierSettings

PRODUCT_COPY_FILES += \
    $(call find-copy-subdir-files,*,vendor/custom/prebuilt/product/etc/CarrierSettings,$(TARGET_COPY_OUT_PRODUCT)/etc/CarrierSettings)

# SIM Toolkit.
PRODUCT_PACKAGES += \
    CellBroadcastReciever \
    Stk

# Telephony
PRODUCT_PACKAGES += \
    telephony-ext \
    ims-ext-common \
    ims_ext_common.xml \
    qti-telephony-hidl-wrapper \
    qti_telephony_hidl_wrapper.xml \
    qti-telephony-utils \
    qti_telephony_utils.xml

PRODUCT_BOOT_JARS += \
    telephony-ext
