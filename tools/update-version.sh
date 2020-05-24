#/bin/bash
#
# Update version info in dbloc/versioninfo.py
#

function set_info {
    KEY=$1
    VAL=$2

    echo "Setting ${KEY} = '${VAL}'"

    sed -i -e "/^${KEY} = /c ${KEY} = '${VAL}' " dbloc_project/versioninfo.py
}

GIT_HASH=$(git rev-parse HEAD)
GIT_TAG=$(git tag --points-at HEAD | tr '\n' ' ')

# Add 'unclean' mark if there are modified files in the working copy
git diff --quiet
if [ $? -ne 0 ];
then
    GIT_HASH="${GIT_HASH} (+ local modifications)"
    GIT_TAG="${GIT_TAG} (+ local modifications)"
fi

set_info GIT_HASH "${GIT_HASH}"
set_info GIT_TAG "${GIT_TAG}"
set_info BUILD_DATE "$(TZ=UTC date)"
set_info BUILD_HOST "$(hostname -f) "
