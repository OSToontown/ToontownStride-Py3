from panda3d.core import *

import argparse, struct
import sys, glob
import os

sys.path.append('nirai/src')

from niraitools import *

parser = argparse.ArgumentParser()
parser.add_argument('--compile-cxx', '-c', action='store_true',
                    help='Compile the CXX codes and generate stride.exe into built.')
parser.add_argument('--make-nri', '-n', action='store_true',
                    help='Generate stride NRI.')
parser.add_argument('--make-mfs', '-m', action='store_true',
                    help='Make multifiles')
args = parser.parse_args()

if not os.path.exists('built'):
    os.mkdir('built')

def niraicall_obfuscate(code):
    # We'll obfuscate if len(code) % 4 == 0
    # This way we make sure both obfuscated and non-obfuscated code work.
    if len(code) % 4:
        return False, None

    # Reverse
    code = code[::-1]

    # AES
    key = ''.join(chr((i ^ (9 * i + 81)) % ((i + 193) * 11)) for i in xrange(16))
    iv = ''.join(chr((i ^ (5 * i + 170)) % ((i + 38) * 7)) for i in xrange(16))
    code = aes.encrypt(code, key, iv)

    return True, code

niraimarshal.niraicall_obfuscate = niraicall_obfuscate

class StridePackager(NiraiPackager):
    HEADER = 'TTSTRIDE'
    BASEDIR = '..' + os.sep

    def __init__(self, outfile):
        NiraiPackager.__init__(self, outfile)
        self.__manglebase = self.get_mangle_base(self.BASEDIR)
        self.add_panda3d_dirs()
        self.add_default_lib()

    def add_source_dir(self, dir):
        self.add_directory(self.BASEDIR + dir, mangler=self.__mangler)

    def add_data_file(self, file):
        mb = self.get_mangle_base('data/')
        self.add_file('data/%s.py' % file, mangler=lambda x: x[mb:])

    def __mangler(self, name):
        if name.endswith('AI') or name.endswith('UD') or name in ('ToontownAIRepository', 'ToontownUberRepository',
                                                                  'ToontownInternalRepository', 'ServiceStart'):
            if not 'NonRepeatableRandomSource' in name:
                return ''

        return name[self.__manglebase:].strip('.')

    def generate_niraidata(self):
        print 'Generating niraidata'
        # Config
        config = self.get_file_contents('../deployment/public_client.prc')

        config_iv = self.generate_key(16)
        config_key = self.generate_key(16)
        config = config_iv + config_key + aes.encrypt(config, config_key, config_iv)
        niraidata = 'CONFIG = %r' % config
        
        # DC
        niraidata += '\nDC = %r' % self.get_file_contents('../dependencies/astron/dclass/stride.dc', True)
        self.add_module('niraidata', niraidata, compile=True)

    def process_modules(self):
        # TODO: Compression
        dg = Datagram()
        dg.addUint32(len(self.modules))
        for moduleName in self.modules:
            data, size = self.modules[moduleName]

            dg.addString(moduleName)
            dg.addInt32(size)
            dg.appendData(data)

        data = dg.getMessage()
        #compressed = compress_string(data, 9)
        iv = self.generate_key(16)
        key = self.generate_key(16)
        fixed_key = ''.join(chr((i ^ (7 * i + 16)) % ((i + 5) * 3)) for i in xrange(16))
        fixed_iv = ''.join(chr((i ^ (2 * i + 53)) % ((i + 9) * 6)) for i in xrange(16))
        securekeyandiv = aes.encrypt(iv + key, fixed_key, fixed_iv)
        return securekeyandiv + aes.encrypt(data, key, iv)

# Compile the engine
if args.compile_cxx:
    compiler = NiraiCompiler('stride.exe', libs=set(glob.glob('libpandadna/libpandadna.dir/Release/*.obj')))

    compiler.add_nirai_files()
    compiler.add_source('src/stride.cxx')

    compiler.run()

# Compile the game data
if args.make_nri:
    pkg = StridePackager('built/TTSData.bin')

    pkg.add_source_dir('otp')
    pkg.add_source_dir('toontown')

    pkg.add_data_file('NiraiStart')

    pkg.generate_niraidata()

    pkg.write_out()

if args.make_mfs:
    os.chdir('../resources')
    cmd = ''
    for phasenum in ['3', '3.5', '4', '5', '5.5', '6', '7', '8', '9', '10', '11', '12', '13']:
        print 'phase_%s' % (phasenum)
        cmd = 'multify -cf ../build/built/resources/default/phase_%s.mf phase_%s' % (phasenum, phasenum)
        p = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
        v = p.wait()

        if v != 0:
            print 'The following command returned non-zero value (%d): %s' % (v, cmd[:100] + '...')
            sys.exit(1)
