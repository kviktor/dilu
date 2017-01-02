import json
import os

import django
os.environ["DJANGO_SETTINGS_MODULE"] = "dilu.settings"
django.setup()

from dilu.models import Version, Object, Module  # noqa


def load_version(name, tag, data):
    version, created = Version.objects.get_or_create(
        name=name, tag=tag)
    Object.objects.filter(module__version=version).delete()
    Module.objects.filter(version=version).delete()

    Module.objects.bulk_create([
        Module(version=version, **value)
        for value in data['modules']
    ], batch_size=500)

    tmp = []
    for key, value in data['objects'].items():
        module_path = value.pop("module")
        module = Module.objects.get(path=module_path, version=version)
        tmp.append(Object(module=module, **value))
    Object.objects.bulk_create(tmp, batch_size=500)


if __name__ == "__main__":
    with open("vv.json", "r") as f:
        data = json.load(f)

    load_version(data['name'], data['tag'], data['data'])
