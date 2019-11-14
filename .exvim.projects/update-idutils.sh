#!/bin/bash
export DEST="./.exvim.projects"
export TOOLS="/home/joshtrick/.vim/tools/"
export TMP="${DEST}/_ID"
export TARGET="${DEST}/ID"
sh ${TOOLS}/shell/bash/update-idutils.sh
