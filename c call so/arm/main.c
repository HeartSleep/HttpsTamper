#include <stdio.h>  
#include <stdlib.h>   // EXIT_FAILURE
#include <dlfcn.h>    // dlopen, dlerror, dlsym, dlclose

typedef char *(* FUNC_getmd5)(); // 定义函数指针类型的别名
const char* dllPath = "./libMovieController_arm7.so";

int main()
{
    void* handle = dlopen( dllPath, RTLD_LAZY );

    if( !handle )
    {
        fprintf( stderr, "[%s](%d) dlopen get error: %s\n", __FILE__, __LINE__, dlerror() );
        exit( EXIT_FAILURE );
    }
 printf( "1111\n");
   
    FUNC_getmd5 func_getmd5 = (FUNC_getmd5)dlsym( handle, "getmd5" );
    printf( "222\n");
    printf( " %s \n", func_getmd5());
   
    dlclose( handle );
}