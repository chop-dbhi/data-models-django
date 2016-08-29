import setuptools
import sys

from dmdj import __version__

if sys.version_info < (2, 7):
    raise EnvironmentError('Python 2 < 2.7 is not supported')

if sys.version_info >= (3,) and sys.version_info < (3, 4):
    raise EnvironmentError('Python 3 < 3.4 is not supported.')

if sys.version_info >= (3, 6):
    raise EnvironmentError('Python 3 >= 3.6 is not yet supported.')

with open('README.md') as f:
    long_description = f.read()

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
    ]
)
