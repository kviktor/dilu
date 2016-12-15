#!/bin/sh

test -d repo_django/ || git clone https://github.com/django/django.git repo_django
git -C "repo_django/" fetch

for i in "1.9.2" "1.8.9" "1.7.2" "1.6.5"
do
    python -B dump_version.py $i $i
    python -B load_version.py
done

rm -f vv.json
