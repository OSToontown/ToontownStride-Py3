#include "nirai.h"
#include <datagram.h>
#include <datagramIterator.h>
#include <compress_string.h>

string rc4(const char* data, const char* key, int ds, int ks);

extern "C" __declspec(dllexport) void initlibpandadna();
void init_libpandadna();

const char* header = "STRIDETT";
const int header_size = 8;

const int keysize = 100;
const int fixedsize = 28;

int niraicall_onPreStart(int argc, char* argv[])
{
    return 0;
}

int niraicall_onLoadGameData()
{
    fstream gd;

    // Open the file
    gd.open("stride.dist", ios_base::in | ios_base::binary);
	if (!gd.is_open())
    {
        std::cerr << "Unable to open game file!" << std::endl;
		return 1;
    }

    // Check the header
	char* read_header = new char[header_size];
	gd.read(read_header, header_size);

    if (memcmp(header, read_header, header_size))
    {
        std::cerr << "Invalid header" << std::endl;
        return 1;
    }

    delete[] read_header;

    // Extract the key
    char* key = new char[keysize + fixedsize];
    char* fixed = new char[keysize];

    for (int i = 0; i < fixedsize; ++i)
        fixed[i] = (i ^ (5 * i + 7)) % ((i + 6) * 10);

    gd.read(key, keysize);
    memcpy(&key[keysize], fixed, fixedsize);

    std::stringstream ss;
    ss << gd.rdbuf();
    gd.close();

    // Decrypt
    std::string rawdata = ss.str();
    std::string decrypted_data = rc4(rawdata.c_str(), key, rawdata.size(),
                                     keysize + fixedsize);
    delete[] key;
    delete[] fixed;

    // Decompress and read
    std::string decompressed = decompress_string(decrypted_data);

    Datagram dg(decompressed);
    DatagramIterator dgi(dg);

    unsigned int num_modules = dgi.get_uint32();
    _frozen* fzns = new _frozen[num_modules + 1];
    std::string module, data;
    int size;

    for (unsigned int i = 0; i < num_modules; ++i)
    {
        module = dgi.get_string();
        size = dgi.get_int32();
        data = dgi.extract_bytes(abs(size));

        char* name = new char[module.size() + 1];
        memcpy(name, module.c_str(), module.size());
        memset(&name[module.size()], 0, 1);

        unsigned char* code = new unsigned char[data.size()];
        memcpy(code, data.c_str(), data.size());

        _frozen fz;
		fz.name = name;
		fz.code = code;
		fz.size = size;

        memcpy(&fzns[i], &fz, sizeof(_frozen));
    }

    nassertd(dgi.get_remaining_size() == 0)
    {
        std::cerr << "Corrupted data!" << std::endl;
        return 1;
    }

    memset(&fzns[num_modules], 0, sizeof(_frozen));
    PyImport_FrozenModules = fzns;

    // libpandadna
    init_libpandadna();
    initlibpandadna();

    return 0;
}
