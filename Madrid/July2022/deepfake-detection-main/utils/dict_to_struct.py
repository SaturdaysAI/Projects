"""Convert a Dictionary into an Structure"""

class DictStructure(dict):
    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

if __name__ == "__main__":
    d = {'a': 1, 'b': 2}
    print(f"Initial Dictionary: {d}")

    ds = DictStructure(d)
    print(f"ds.a: {ds.a}")
    print(f"ds.b: {ds.b}")

    print("Adding a new attribute: {ds.c = 3}")
    ds.c = 3
    print(f"ds.c: {ds.c}")

    print("Overall structure:")
    print(ds)
