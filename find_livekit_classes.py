import livekit.agents
import inspect
import pkgutil

def find_classes(module):
    try:
        path = module.__path__
    except AttributeError:
        return

    for _, name, ispkg in pkgutil.iter_modules(path):
        try:
            full_name = module.__name__ + '.' + name
            submod = __import__(full_name, fromlist=['*'])
            for cls_name, cls in inspect.getmembers(submod, inspect.isclass):
                if 'Agent' in cls_name or 'Assistant' in cls_name:
                    print(f"{full_name}.{cls_name}")
            if ispkg:
                find_classes(submod)
        except Exception:
            pass

print("Searching for classes...")
find_classes(livekit.agents)
