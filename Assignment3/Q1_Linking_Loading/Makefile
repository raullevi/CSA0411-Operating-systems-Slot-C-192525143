CC = gcc
CFLAGS = -std=c11 -Wall -Wextra -O2
UNAME_S := $(shell uname -s)

ifeq ($(UNAME_S),Darwin)
    SO_EXT = dylib
    SHARED_FLAGS = -dynamiclib -install_name @rpath/libencrypt.dylib
    LDFLAGS = -L. -lencrypt -Wl,-rpath,@executable_path/.
else
    SO_EXT = so
    SHARED_FLAGS = -shared -fPIC -Wl,-soname,libencrypt.so
    LDFLAGS = -L. -lencrypt -Wl,-rpath,'$$ORIGIN'
    DL_LIB = -ldl
endif

all: static_lib shared_libs static_app dynamic_app dlopen_app

static_lib:
	$(CC) $(CFLAGS) -c libencrypt_v1.c -o libencrypt_v1.o
	ar rcs libencrypt.a libencrypt_v1.o

shared_libs:
	$(CC) $(CFLAGS) -fPIC $(SHARED_FLAGS) libencrypt_v1.c -o libencrypt_v1.$(SO_EXT)
	$(CC) $(CFLAGS) -fPIC $(SHARED_FLAGS) libencrypt_v2.c -o libencrypt_v2.$(SO_EXT)
	cp libencrypt_v1.$(SO_EXT) libencrypt.$(SO_EXT)

static_app: static_lib
	$(CC) $(CFLAGS) bank_app.c libencrypt.a -o bank_app_static

dynamic_app: shared_libs
	$(CC) $(CFLAGS) bank_app.c $(LDFLAGS) -o bank_app_dynamic

dlopen_app:
	$(CC) $(CFLAGS) bank_app_dlopen.c -o bank_app_dlopen $(DL_LIB)

clean:
	rm -f *.o *.a *.so *.dylib bank_app_static bank_app_dynamic bank_app_dlopen
