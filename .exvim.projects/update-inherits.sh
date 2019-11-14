#!/bin/bash
export DEST="./.exvim.projects"
export TOOLS="/home/joshtrick/.vim/tools/"
export TMP="${DEST}/_inherits"
export TARGET="${DEST}/inherits"
sh ${TOOLS}/shell/bash/update-inherits.sh
