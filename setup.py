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
    'description': 'PEDSnet Common Data Model Definitions',
    'long_description': long_description,
    'packages': find_packages(),
    'install_requires': install_requires,
    'download_url': ('https://github.com/chop-dbhi/'
                     'data-models-django/tarball/%s' % __version__),
}

setup(**kwargs)
