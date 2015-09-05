import sys
from setuptools import setup, find_packages
from dmdj import __version__

if sys.version_info < (2, 7):
    raise EnvironmentError('Python 2.7.x is required')

with open('README.md', 'r') as f:
    long_description = f.read()

install_requires = [
    'Django==1.7.9',
    'requests==2.7.0'
]

kwargs = {
    'name': 'dmdj',
    'version': __version__,
    'author': 'The Children\'s Hospital of Philadelphia',
    'author_email': 'cbmisupport@email.chop.edu',
    'url': 'https://github.com/chop-dbhi/data-models-django',
    'description': ('Django models for chop-dbhi/data-models-service style '
                    'JSON endpoints.'),
    'long_description': long_description,
    'license': 'Other/Proprietary',
    'packages': find_packages(),
    'install_requires': install_requires,
    'download_url': ('https://github.com/chop-dbhi/'
                     'data-models-django/tarball/%s' % __version__),
    'keywords': ['healthcare', 'data models', 'Django', 'OMOP', 'i2b2',
                 'PCORnet', 'PEDSnet'],
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'License :: Other/Proprietary License',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Code Generators',
        'Natural Language :: English'
    ]
}

setup(**kwargs)
