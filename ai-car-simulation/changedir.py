import os

class Changedir:
    def __init__(self, newdir, path=None):

        self.olddir = os.getcwd()
        if not path is None:
            self.olddir = os.path.abspath(path)

        self.newdir = newdir

    def __enter__(self):
        os.chdir(self.newdir)
        return self

    def __exit__(self, *args, **kwargs):
        os.chdir(self.olddir)

if __name__ == "__main__":
    origdir = os.getcwd()
    change_to = os.path.abspath(os.path.join(origdir, ".."))

    with Changedir(change_to) as changed:
        # print(changed.newdir, changed.path)
        assert change_to == os.getcwd()
    assert os.getcwd() == origdir