cd ../nirai/src

gcc -DNDEBUG -g -O3 -Wall -Wstrict-prototypes -fPIC -DMAJOR_VERSION=1 -DMINOR_VERSION=0 -I/usr/include -I/usr/include/python2.7 -lstdc++ -lssl -lcrypto  -c aes.cxx -c -o aes.o

gcc -shared aes.o -L/usr/local/lib -lstdc++ -lssl -lcrypto -o aes.so