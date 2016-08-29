import os

serial = os.environ.get('BUILD_NUM') or '0'
sha = os.environ.get('GIT_SHA') or '0'
if sha:
    sha = sha[0:8]

__version_info__ = {
    'major': 0,
    'minor': 4,
    'micro': 0,
    'releaselevel': 'final',
    'serial': serial,
    'sha': sha
}


def get_version(short=False):
    assert __version_info__['releaselevel'] in ('alpha', 'beta', 'final')
    vers = ['%(major)i.%(minor)i.%(micro)i' % __version_info__, ]
    if __version_info__['releaselevel'] != 'final' and not short:
        __version_info__['lvlchar'] = __version_info__['releaselevel'][0]
        vers.append('%(lvlchar)s%(serial)s+%(sha)s' % __version_info__)
    return ''.join(vers)

__version__ = get_version()

SERVICE = os.environ.get('DMDJ_SERVICE') or \
    'https://data-models-service.research.chop.edu/'
