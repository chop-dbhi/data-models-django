#!/bin/bash
ver=$(python -c "from dmdj import get_version; print(get_version(True))")
lvl=$(python -c "from dmdj import __version_info__; print(__version_info__['releaselevel'])")
if [ "${lvl}" != "final" ]; then
    sha="${GIT_SHA}"
    test -z "${sha}" && sha=$(git log -1 --pretty=format:"%h")
    test -z "${sha}" && sha=0
    sha="${sha:0:8}"
    serial="${BUILD_NUM:-0}"
    ver="${ver}-${lvl}+${serial}.${sha}"
fi
printf "${ver}"
