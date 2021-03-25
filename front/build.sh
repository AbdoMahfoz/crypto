#!/bin/bash

yarn build
rm -rf ../static
rm -rf ../templates
mkdir -p ../static
mkdir -p ../templates
mv build/* ../static/
mv ../static/index.html ../templates/index.html
rm -rf build
