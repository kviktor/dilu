#!/bin/sh

gitroot=$(git rev-parse --show-toplevel)
test -d $gitroot/dilu/repo_django || git clone https://github.com/django/django.git $gitroot/dilu/repo_django
git -C $gitroot/dilu/repo_django fetch

for i in "1.9.2" "1.8.9" "1.7.2" "1.6.5"
do
    python -B dump_version.py $i $i
    python -B load_version.py
done

rm -f vv.json
