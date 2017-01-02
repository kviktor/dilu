import os
import sys
import importlib
import inspect
import json
import subprocess

from git import Git


file_dir = os.path.dirname(os.path.realpath(__file__))
repo_dir = os.path.join(file_dir, "repo_django")
sys.path = [repo_dir] + sys.path


def update_conv(member, path, convs):
    if member not in convs:
        convs[member] = path
    else:
        if len(convs[member]) > len(path):
            convs[member] = path
    return convs


def get_object_type(obj):
    if inspect.isclass(obj):
        return "c"
    elif inspect.isfunction(obj):
        return "f"


def describe(module, convs):
    objs = {}
    for name, obj in inspect.getmembers(module):
        if name.startswith("__") or inspect.isbuiltin(obj):
            continue

        o_type = get_object_type(obj)
        if not o_type:
            continue

        try:
            lines, start = inspect.getsourcelines(obj)
        except (TypeError, OSError) as e:  # noqa
            # print(e)
            continue

        key = "{}.{}".format(obj.__module__, name)
        if module.__name__ == obj.__module__:
            objs[key] = {
                'name': name,
                'module': obj.__module__,
                'short_import': "",
                'docstring': inspect.getdoc(obj) or "",
                'code': "".join(lines),
                'line': start,
                'type': o_type,
            }
            convs = update_conv(key, obj.__module__, convs)
        else:
            # TODO obj.__name__ vs name
            key = "%s.%s" % (obj.__module__, obj.__name__)
            convs = update_conv(key, module.__name__, convs)
    return objs, convs


def inspect_code(tag):
    g = Git(repo_dir)
    g.checkout(tag)
    subprocess.call(["py3clean", repo_dir])

    import django
    importlib.reload(django)
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    if hasattr(django, "setup"):
        django.setup()
    print("tag: {}, imported: {}".format(tag, django.get_version()))

    objs = {}
    convs = {}  # convenient import path
    modules = []
    for dirpath, dirnames, filenames in os.walk("repo_django/django/"):
        dirpath = dirpath.rstrip("/")
        for name in filenames:
            if not name.endswith(".py"):
                continue

            # it has a sys.exit() call in it
            if name.startswith("django-2to3"):
                continue

            if name == "__init__.py":
                import_path = dirpath.replace("/", ".")
            else:
                import_path = os.path.join(
                    dirpath.replace("/", "."),
                    name.replace(".py", "")
                ).replace("/", ".")

            import_path = import_path.replace("repo_django.", "")
            if import_path:
                try:
                    module = importlib.import_module(import_path)
                except Exception as e:
                    continue
            partial_objects, convs = describe(module, convs)
            objs.update(partial_objects)
            modules.append({
                'path': module.__name__,
                'filename': os.path.basename(os.path.relpath(module.__file__,
                                                             repo_dir)),
            })

    for full, short in convs.items():
        try:
            objs[full]['short_import'] = short
        except KeyError as e:  # noqa
            # print("Key not found: %s" % e)
            pass

    return {'modules': modules, 'objects': objs}


if __name__ == "__main__":
    if len(sys.argv) == 3:
        name, tag = sys.argv[1:]
        data = inspect_code(tag)

        with open("vv.json", "w") as f:
            json.dump({'name': name, 'tag': tag, 'data': data}, f)
    else:
        print("Missing Django version and/or tag name")
