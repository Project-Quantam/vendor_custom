package android
type Product_variables struct {
	Target_init_vendor_lib struct {
		Whole_static_libs []string
	}
	Target_shim_libs struct {
		Cppflags []string
	}
	Target_surfaceflinger_fod_lib struct {
		Cflags []string
		Whole_static_libs []string
	}
	Target_uses_prebuilt_dynamic_partitions struct {
		Cflags []string
	}
}

type ProductVariables struct {
	Target_init_vendor_lib  *string `json:",omitempty"`
	Target_shim_libs  *string `json:",omitempty"`
	Target_surfaceflinger_fod_lib  *string `json:",omitempty"`
	Target_uses_prebuilt_dynamic_partitions  *bool `json:",omitempty"`
}
