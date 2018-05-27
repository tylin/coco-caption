#!/usr/bin/env sh
# This script downloads the Google News word2vec negative 300 model.
# Script code was taken from https://gist.github.com/yanaiela/cfef50380de8a5bfc8c272bb0c91d6e1

WMDDATA=pycocoevalcap/wmd/data
MODEL=GoogleNews-vectors-negative300

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

if [ -f $WMDDATA/$MODEL.bin ]; then
  echo "Found Google news word2vec model."
else
  echo "Downloading..."
  OUTPUT=$( wget --save-cookies $WMDDATA/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=0B7XkCwpI5KDYNlNUTTlSS21pQmM' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/Code: \1\n/p' )
  CODE=${OUTPUT##*Code: }
  echo Code: $CODE
  wget --load-cookies $WMDDATA/cookies.txt 'https://docs.google.com/uc?export=download&confirm='$CODE'&id=0B7XkCwpI5KDYNlNUTTlSS21pQmM' -O $WMDDATA/$MODEL.bin.gz
  rm $WMDDATA/cookies.txt
  echo "Unzipping..."
  gzip -d $WMDDATA/$MODEL.bin.gz $WMDDATA/
  echo "Done."
fi