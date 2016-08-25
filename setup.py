import setuptools
import sys

from setuptools.command.test import test as TestCommand

from dmdj import __version__

if sys.version_info < (2, 7):
    raise EnvironmentError('Python 2 < 2.7 is not supported')

if sys.version_info >= (3,) and sys.version_info < (3, 4):
    raise EnvironmentError('Python 3 < 3.4 is not supported.')

if sys.version_info >= (3, 6):
    raise EnvironmentError('Python 3 >= 3.6 is not yet supported.')

with open('README.md') as f:
    long_description = f.read()


class Tox(TestCommand):
    user_options = [('tox-args=', 'a', "Arguments to pass to tox")]

    def initialize_options(self):
        super(Tox, self).initialize_options(self)
        self.tox_args = None

    def finalize_options(self):
        super(Tox, self).finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # Import here, because eggs aren't loaded before.
        import tox
        import shlex
        args = self.tox_args
        if args:
            args = shlex.split(self.tox_args)
        tox.cmdline(args=args)

setuptools.setup(
    name='dmdj',
    version=__version__,
    description='Django model generator for JSON metadata',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: Other/Proprietary License',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Code Generators',
        'Natural Language :: English'
    ],
    keywords=['healthcare', 'data models', 'Django', 'OMOP', 'OHDSI', 'i2b2',
              'PCORnet', 'PEDSnet'],
    url='https://github.com/chop-dbhi/data-models-django',
    download_url=('https://github.com/chop-dbhi/'
                  'data-models-django/tarball/%s' % __version__),
    author='The Children\'s Hospital of Philadelphia',
    author_email='cbmisupport@email.chop.edu',
    license='Other/Proprietary',
    packages=setuptools.find_packages(),
    install_requires=[
        'Django>=1.7,<1.11'
    ],
    tests_require=[
        'tox',
        'pytest'
    ],
    cmdclass={'test': Tox}
)
