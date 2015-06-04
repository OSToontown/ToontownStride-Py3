from panda3d.core import *

import argparse, marshal, struct
import glob, sys, os
import rc4

parser = argparse.ArgumentParser()
parser.add_argument('--compile-cxx', '-c', action='store_true',
                    help='Compile the CXX codes and generate Nirai.exe into built.')
parser.add_argument('--make-nri', '-n', action='store_true',
                    help='Generate stride NRI.')
args = parser.parse_args()

# BEGIN (STRIPPED AND MODIFIED) COPY FROM niraitools.py 
class NiraiPackager:
    HEADER = 'NRI\n'
    
    def __init__(self, outfile):
        self.modules = {}
        self.outfile = outfile
        
    def __read_file(self, filename, mangler=None):
        with open(filename, 'rb') as f:
            data = f.read()
            
        base = filename.rsplit('.', 1)[0].replace('\\', '/').replace('/', '.')
        pkg = base.endswith('.__init__')
        moduleName = base.rsplit('.', 1)[0] if pkg else base
            
        name = moduleName
        if mangler is not None:
            name = mangler(name)
            
        if not name:
            return '', ('', 0)
         
        try:
            data = self.compile_module(name, data)
            
        except:
            print 'WARNING: Failed to compile', filename
            return '', ('', 0)
            
        size = len(data) * (-1 if pkg else 1)
        return name, (data, size)
        
    def compile_module(self, name, data):
        return marshal.dumps(compile(data, name, 'exec'))
        
    def add_module(self, moduleName, data, size=None, compile=False):
        if compile:
            data = self.compile_module(moduleName, data)
            
        if size is None:
            size = len(data)
            
        self.modules[moduleName] = (data, size)
        
    def add_file(self, filename, mangler=None):
        print 'Adding file', filename
        moduleName, (data, size) = self.__read_file(filename, mangler)
        if moduleName:
            moduleName = os.path.basename(filename).rsplit('.', 1)[0]
            self.add_module(moduleName, data, size)
    
    def add_directory(self, dir, mangler=None):
        print 'Adding directory', dir
        
        def _recurse_dir(dir):
            for f in os.listdir(dir):
                f = os.path.join(dir, f)
        
                if os.path.isdir(f):
                    _recurse_dir(f)
            
                elif f.endswith('py'):
                    moduleName, (data, size) = self.__read_file(f, mangler)
                    if moduleName:
                        self.add_module(moduleName, data, size)
                    
        _recurse_dir(dir)
        
    def get_mangle_base(self, *path):
        return len(os.path.join(*path).rsplit('.', 1)[0].replace('\\', '/').replace('/', '.')) + 1

    def write_out(self):
        f = open(self.outfile, 'wb')
        f.write(self.HEADER)
        f.write(self.process_modules())
        f.close()
        
    def generate_key(self, size=256):
        return os.urandom(size)
        
    def dump_key(self, key):
        for k in key:
            print ord(k),
        
        print
        
    def process_modules(self):
        # Pure virtual
        raise NotImplementedError('process_datagram')
        
    def get_file_contents(self, filename, keysize=0):
        with open(filename, 'rb') as f:
            data = f.read()
            
        if keysize:
            key = self.generate_key(keysize)
            rc4.rc4_setkey(key)
            data = key + rc4.rc4(data)
            
        return data
# END COPY FROM niraitools.py 

class StridePackager(NiraiPackager):
    HEADER = 'STRIDETT'
    BASEDIR = '..' + os.sep
    
    def __init__(self, outfile):
        NiraiPackager.__init__(self, outfile)
        self.__manglebase = self.get_mangle_base(self.BASEDIR)
        
    def add_source_dir(self, dir):
        self.add_directory(self.BASEDIR + dir, mangler=self.__mangler)
        
    def add_data_file(self, file):
        mb = self.get_mangle_base('data/')
        self.add_file('data/%s.py' % file, mangler=lambda x: x[mb:])
        
    def __mangler(self, name):         
        if name.endswith('AI') or name.endswith('UD') or name in ('ToontownAIRepository', 'ToontownUberRepository',
                                                                  'ToontownInternalRepository'):
            if not 'NonRepeatableRandomSource' in name:
                return ''

        return name[self.__manglebase:].strip('.')
        
    def generate_niraidata(self):
        print 'Generating niraidata'
        
        config = self.get_file_contents('../dependencies/config/release/en.prc')
        config += '\n\n' + self.get_file_contents('../dependencies/config/general.prc')
        key = self.generate_key(128)
        rc4.rc4_setkey(key)
        config = key + rc4.rc4(config)
        
        niraidata = 'CONFIG = %r' % config
        niraidata += '\nDC = %r' % self.get_file_contents('../dependencies/astron/dclass/stride.dc', 128)
        self.add_module('niraidata', niraidata, compile=True)
        
    def process_modules(self):
        with open('base.dg', 'rb') as f:
            basesize, = struct.unpack('<I', f.read(4))
            data = f.read()
            
        dg = Datagram()
        dg.addUint32(len(self.modules) + basesize)
        dg.appendData(data)
    
        for moduleName in self.modules:
            data, size = self.modules[moduleName]
        
            dg.addString(moduleName)
            dg.addInt32(size)
            dg.appendData(data)
            
        data = dg.getMessage()
        compressed = compressString(data, 9)
        key = self.generate_key(100)
        fixed = ''.join(chr((i ^ (5 * i + 7)) % ((i + 6) * 10)) for i in xrange(28))
        rc4.rc4_setkey(key + fixed)
        data = rc4.rc4(compressed)        
        return key + data
        
# 1. Make the NRI
if args.make_nri:
    pkg = StridePackager('built/stride.dist')
    
    pkg.add_source_dir('otp')
    pkg.add_source_dir('toontown')

    pkg.add_data_file('NiraiStart')
    
    pkg.generate_niraidata()
    pkg.write_out()
        
# 2. Compile CXX stuff
if args.compile_cxx:
    sys.path.append('../../../N2')
    from niraitools import NiraiCompiler
    
    compiler = NiraiCompiler('stride.exe', r'"C:\\Users\\Usuario\\workspace\\nirai-panda3d\\thirdparty\\win-libs-vc10"',
                             libs=set(glob.glob('libpandadna/libpandadna.dir/Release/*.obj')))
    compiler.add_nirai_files()
    compiler.add_source('src/stride.cxx')
    
    compiler.run()
