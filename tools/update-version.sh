#/bin/bash
#
# Update version info in dbloc/versioninfo.py
#

function set_info {
    KEY=$1
    VAL=$2

    echo "Setting ${KEY}='${VAL}'"

    sed -ie "/^${KEY} = /c ${KEY} = '${VAL}' " dbloc/versioninfo.py
}

GIT_HASH=$(git rev-parse HEAD)
GIT_TAG=$(git tag --points-at HEAD | tr '\n' ' ')

if git diff --quiet;
then
    GIT_HASH=$(GIT_HASH) unclean
    GIT_TAG=$(GIT_TAG) unclean

fi

set_info GIT_HASH "${GIT_HASH}"
set_info GIT_TAG "${GIT_TAG}"
