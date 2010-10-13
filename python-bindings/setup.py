# encoding: utf-8
from distutils.core import setup, Command
from distutils.extension import Extension
from Cython.Distutils import build_ext

# Import for unit tests
from os.path import splitext, basename, join as pjoin, walk
from unittest import TextTestRunner, TestLoader
from glob import glob    
import os


srcpath = 'sha3lib/'
hashpath = srcpath + 'hash_functions/'

ext_modules = [
    Extension("sha3lib.hash_functions.bmw.bmw",
        [hashpath+"bmw/bmw.pyx", hashpath+'bmw/BlueMidnightWish.c'],),
    Extension("sha3lib.hash_functions.groestl.groestl",
        [hashpath+"groestl/groestl.pyx", hashpath+'groestl/Groestl-opt.c'],),
    Extension("sha3lib.hash_functions.echo.echo",
        [hashpath+"echo/echo.pyx", hashpath+'echo/echo32.c'],),
    Extension("sha3lib.hash_functions.blake.blake",
        [hashpath+"blake/blake.pyx", hashpath+'blake/blake_opt32.c'],),
    Extension("sha3lib.hash_functions.skein.skein_hash",
        [hashpath+"skein/skein_hash.pyx", hashpath+'skein/SHA3api_ref.c',
        hashpath+"skein/skein_block.c",hashpath+"skein/skein.c"],),
    Extension("sha3lib.hash_functions.luffa.luffa",
        [hashpath+"luffa/luffa.pyx", hashpath+'luffa/luffa_for_32.c'],),
    Extension("sha3lib.hash_functions.shavite3.shavite3",
        [hashpath+"shavite3/shavite3.pyx", hashpath+'shavite3/SHAvite3.c'],),
    Extension("sha3lib.hash_functions.simd.simd",
        [hashpath+"simd/simd.pyx",hashpath+"simd/optimized.c",
        hashpath+"simd/nist.c"],),
    Extension("sha3lib.hash_functions.keccak.keccak",
        [hashpath+"keccak/keccak.pyx",hashpath+"keccak/KeccakF-1600-opt32.c",
        hashpath+"keccak/KeccakSponge.c"],),
    Extension("sha3lib.hash_functions.jh.jh",
        [hashpath+"jh/jh.pyx"],),
    Extension("sha3lib.hash_functions.fugue.fugue_hash",
        [hashpath+"fugue/fugue_hash.pyx",hashpath+"fugue/SHA3api_ref.c",
            hashpath+"fugue/fugue.c", hashpath+"fugue/fugue_256.c",
            hashpath+"fugue/fugue_384.c",hashpath+"fugue/fugue_512.c"],),
    ]
#fugue_256.c  fugue_384.c  fugue_512.c
class RunTests(Command):
    
    user_options = []

    def initialize_options(self):
        print "Warning: You need to run python setup.py build_ext -i before\
        running tests, or they will fail"
        self._dir = os.getcwd()
        # FIXME: Is there a better way of running build_ext -i than with the
        # setup.cfg file?
        #self.distribution.script_args = '-i'
        #import sys
        #sys.argv[1] = "-i"
        #self.run_command('build_ext')


    def finalize_options(self):
        pass

    def run(self):
        '''
        Runs all unit tests
        '''
        testfiles = []
        all_testfiles = glob(pjoin(self._dir, 'tests', '*.py'))
        excluded_files = ['__init__.py',
        'katparser.py',]
        excluded_files_full_path = []
        for f in excluded_files:
            excluded_files_full_path.append(pjoin(self._dir,'tests',f))

        for f in all_testfiles:
            if f not in excluded_files_full_path:
                testfiles.append('.'.join(['tests',splitext(basename(f))[0]]))
        
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity = 3)
        t.run(tests)

class RealClean(Command):
    user_options = []

    def initialize_options(self):
        print ""
        self._dir = os.getcwd()
        self._clean_me = []
        for root, dirs, files in os.walk('.'):
            for f in files:
                if f.endswith('.pyc') or f.endswith('.so'):
                    self._clean_me.append(pjoin(root,f))
        self._clean_me.append('./build')
        manual_files = [
                './sha3lib/hash_functions/bmw/bmw.c',
                './sha3lib/hash_functions/luffa/luffa.c',
                './sha3lib/hash_functions/groestl/groestl.c',
                './sha3lib/hash_functions/skein/skein_hash.c',
                './sha3lib/hash_functions/echo/echo.c',
                './sha3lib/hash_functions/shavite3/shavite3.c',
                './sha3lib/hash_functions/blake/blake.c',
                './sha3lib/hash_functions/simd/simd.c',
                './sha3lib/hash_functions/keccak/keccak.c',
                './sha3lib/hash_functions/jh/jh.c',
                './sha3lib/hash_functions/fugue/fugue_hash.c',
                ]
        self._clean_me.extend(manual_files)


    def finalize_options(self):
        pass

    def run(self):
        import shutil
        for clean_me in self._clean_me:
            if os.path.isfile(clean_me):
                try:
                    os.unlink(clean_me)
                except Exception,e:
                    print e
            elif os.path.isdir(clean_me): 
                try:
                    shutil.rmtree(clean_me)
                except Exception,e:
                    print e
            else:
                pass


setup(
    name='SHA3lib',
    version='0.1',
    description='Python bindings for SHA3-256 using Cython',
    author='Eirik Haver and Pål Ruud',
    cmdclass = {'build_ext': build_ext, 'test': RunTests, 'realclean':RealClean},
    ext_modules = ext_modules,
    packages =
        ['sha3lib',
        'sha3lib.hash_functions',
        'sha3lib.hash_functions.bmw',
        'sha3lib.hash_functions.echo', 
        'sha3lib.hash_functions.groestl',
        'sha3lib.hash_functions.blake', 
        'sha3lib.hash_functions.skein', 
        'sha3lib.hash_functions.luffa', 
        'sha3lib.hash_functions.shavite3',
        'sha3lib.hash_functions.simd',
        'sha3lib.hash_functions.keccak',
        'sha3lib.hash_functions.jh',
        'sha3lib.hash_functions.fugue',
        ],
    #py_modules = ['sha3lib'],    
)
