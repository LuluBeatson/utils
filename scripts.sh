
# This file contains bash function wrappers for Poetry-script commands in this project.
# Copy and paste the contents of this file into your .bashrc or .bash_profile to use

export UTILS_PYTHON_PATH=/Users/lulu/Library/Caches/pypoetry/virtualenvs/utils-_51JIu6g-py3.11/bin/python


function tts {
    $UTILS_PYTHON_PATH -m utils.tts "$@"
}


function youtube {
    $UTILS_PYTHON_PATH -m utils.youtube "$@"
}


function image {
    $UTILS_PYTHON_PATH -m utils.image "$@"
}


function summary {
    $UTILS_PYTHON_PATH -m utils.langchain.summary "$@"
}


function dalle {
    $UTILS_PYTHON_PATH -m utils.dalle "$@"
}

