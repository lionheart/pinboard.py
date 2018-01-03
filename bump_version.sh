#!/bin/bash

# Copyright 2014-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ "$1" != "" ]; then
  sed -i "" "s/\(__version__[ ]*=\).*/\1 \"$1\"/g" pinboard/metadata.py
  git add .
  git commit -m "bump version to $1"
  git tag $1
  git push origin master
  git push --tags
  make publish
fi
