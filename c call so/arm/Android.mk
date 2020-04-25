    LOCAL_PATH := $(call my-dir)  
    include $(CLEAR_VARS)  
    LOCAL_CFLAGS += -pie -fPIE
    LOCAL_LDFLAGS += -pie -fPIE
    LOCAL_MODULE    := helloworld  
    LOCAL_SRC_FILES := main.c  
      
    #include $(BUILD_SHARED_LIBRARY)  
    include $(BUILD_EXECUTABLE)  