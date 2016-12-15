import os
import sys
import importlib
import inspect
import json

file_dir = os.path.dirname(os.path.realpath(__file__))
repo_dir = "%s/repo_django" % file_dir
sys.path = [repo_dir] + sys.path


def update_conv(member, path, convs):
    if member not in convs:
        convs[member] = path
    else:
        if len(convs[member]) > len(path):
            convs[member] = path
    return convs


def describe(module, convs):
    objs = {}
    for name, obj in inspect.getmembers(module):
        if name.startswith("__"):
            continue

        if inspect.isbuiltin(obj):
            continue

        o_type = None
        if inspect.isclass(obj):
            o_type = "c"
        elif inspect.isfunction(obj):
            o_type = "f"

        if not o_type:
            continue

        try:
            lines, start = inspect.getsourcelines(obj)
        except (TypeError, OSError) as e:
            continue
            print(e)

        key = "{}.{}".format(obj.__module__, obj.__name__)
        if module.__name__ == obj.__module__:
            objs[key] = {
                'name': obj.__name__,
                'module': obj.__module__,
                'short_import': "",
                'docstring': inspect.getdoc(obj) or "",
                'code': "".join(lines),
                'line': start,
                'type': o_type,
            }
            convs = update_conv(key, obj.__module__, convs)
        else:
            key = "%s.%s" % (obj.__module__, obj.__name__)
            if not hasattr(module, "__all__"):
                convs = update_conv(key, module.__name__, convs)
    return objs, convs


def inspect_code(tag):
    from git import Git
    g = Git("/home/kviktor/Python/dj-import/dilu/repo_django")
    g.checkout(tag)
    import django
    importlib.reload(django)
    os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
    if hasattr(django, "setup"):
        django.setup()
    print("tag: {}, imported: {}".format(tag, django.get_version()))

    objs = {}
    convs = {}
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
            partial_objs, convs = describe(module, convs)
            objs.update(partial_objs)
            modules.append({
                'path': module.__name__,
                'filename': os.path.basename(os.path.relpath(module.__file__,
                                                             repo_dir)),
            })

    for full, short in convs.items():
        try:
            objs[full]['short_import'] = short
        except KeyError as e:
            print("Key not found: %s" % e)

    return {'modules': modules, 'objects': objs}


if __name__ == "__main__":
    if len(sys.argv) == 3:
        name, tag = sys.argv[1:]
        data = inspect_code(tag)

        with open("vv.json", "w") as f:
            json.dump({'name': name, 'tag': tag, 'data': data}, f)
    else:
        print("Missing Django version and/or tag name")
