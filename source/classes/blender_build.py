class BlenderBuild:
    def __init__(self, link, date, _hash, size, branch=None):
        self.link = link
        self.date = date
        self._hash = _hash
        self.size = size
        self.branch = branch
