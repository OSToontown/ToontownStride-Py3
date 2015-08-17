#include "nirai.h"
#include <datagram.h>
#include <datagramIterator.h>
#include <algorithm>
#include <string>
#include <compress_string.h>

extern "C" __declspec(dllexport) void initlibpandadna();
void init_libpandadna();

const char* header = "TTSTRIDE";
const int header_size = 8;

const int key_and_iv_size = 16;

int niraicall_onPreStart(int argc, char* argv[])
{
    return 0;
}

int niraicall_onLoadGameData()
{
    fstream gd;

    // Open the file
    gd.open("TTSData.bin", ios_base::in | ios_base::binary);
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

    // Decrypt
    std::stringstream ss;
    
    ss << gd.rdbuf();
    gd.close();

    std::string brawdata = ss.str();

    // Decrypted the encrypted key and iv
    std::string enckeyandiv = brawdata.substr(0, (key_and_iv_size * 2) + key_and_iv_size);

    unsigned char* deckeyandiv = new unsigned char[enckeyandiv.size()];
    unsigned char* fixed_key = new unsigned char[key_and_iv_size];
    unsigned char* fixed_iv = new unsigned char[key_and_iv_size];

    // Create fixed key and iv

    for (int i = 0; i < key_and_iv_size; ++i)
        fixed_key[i] = (i ^ (7 * i + 16)) % ((i + 5) * 3);

    for (int i = 0; i < key_and_iv_size; ++i)
        fixed_iv[i] = (i ^ (2 * i + 53)) % ((i + 9) * 6);

    int deckeyandivsize = AES_decrypt((unsigned char*)enckeyandiv.c_str(), enckeyandiv.size(), fixed_key, fixed_iv, deckeyandiv);
    
    delete[] fixed_key;
    delete[] fixed_iv;
    
    unsigned char* key = new unsigned char[key_and_iv_size];
    unsigned char* iv = new unsigned char[key_and_iv_size];
    
    // Move the decrypted key and iv into their subsequent char
    
    for (int i = 0; i < key_and_iv_size; ++i)
        iv[i] = deckeyandiv[i];
    
    for (int i = 0; i < key_and_iv_size; ++i)
        key[i] = deckeyandiv[i + key_and_iv_size];
    
    // Decrypt the game data
    std::string rawdata = brawdata.substr((key_and_iv_size * 2) + key_and_iv_size);
    unsigned char* decrypted_data = new unsigned char[rawdata.size()];
    
    int decsize = AES_decrypt((unsigned char*)rawdata.c_str(), rawdata.size(), key, iv, decrypted_data); // Assumes no error

    delete[] key;
    delete[] iv;
 
    // Read

    // TODO: Compression

    Datagram dg(decrypted_data, decsize);
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

    delete[] decrypted_data;

    memset(&fzns[num_modules], 0, sizeof(_frozen));
    PyImport_FrozenModules = fzns;
    
    // libpandadna
    init_libpandadna();
    initlibpandadna();

    return 0;
}

extern "C" PyObject* niraicall_deobfuscate(char* code, Py_ssize_t size)
{
    // convert to string
    std::stringstream sss;
    sss << code;
    std::string codestr = sss.str();
    
    // AES
    unsigned char* aes_decrypt = new unsigned char[size];
    unsigned char* key = new unsigned char[16];
    unsigned char* iv = new unsigned char[16];
    
    for (int i = 0; i < 16; ++i)
        key[i] = (i ^ (9 * i + 81)) % ((i + 193) * 11);

    for (int i = 0; i < 16; ++i)
        iv[i] = (i ^ (5 * i + 170)) % ((i + 38) * 7);
    
    int decsize = AES_decrypt(reinterpret_cast<unsigned char*>(code), size, key, iv, aes_decrypt);
    
    std::string output(reinterpret_cast<char*>(aes_decrypt), decsize);
    // Reverse
    std::reverse(output.begin(), output.end());
    return PyString_FromStringAndSize(output.data(), decsize);
}
