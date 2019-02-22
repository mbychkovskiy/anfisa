import numbers

#===============================================
class Types:
    sTypes = [None, "null", "list", "dict", "empty", "link", "string",
        "int", "numeric"]
    # and "undef", "json"

    @staticmethod
    def _detectValTypes(value):
        if value is None:
            return [1]
        elif isinstance(value, list):
            return [2]
        elif isinstance(value, dict):
            return [3]
        elif isinstance(value, basestring):
            if not value:
                return [4, 5, 6]
            elif value.startswith("http"):
                if value.startswith("https:") or value.startswith("http:"):
                    return [5, 6]
            return [6]
        elif isinstance(value, int):
            return [7, 8]
        elif isinstance(value, numbers.Number):
            return [8]
        # convert everything another to string
        return [6]

    @classmethod
    def typeIdx(cls, value):
        return cls.sTypes.index(value)

    @classmethod
    def detectValTypes(cls, value):
        kind_idxs = cls._detectValTypes(value)
        ret = set()
        if kind_idxs:
            for idx in kind_idxs:
                if cls.sTypes[idx]:
                    ret.add(cls.sTypes[idx])
        return ret

    @classmethod
    def filterTypeKind(cls, kinds):
        for kind in kinds:
            if kind in cls.sTypes:
                return kind
        return None

#===============================================
class TypeCounter:
    def __init__(self, req_type = None):
        self.mCounts = [0] * 9
        self.mReqType = Types.typeIdx(req_type)

    def regValue(self, value):
        cnt0 = self.mCounts[1] + self.mCounts[self.mReqType]
        self.mCounts[0] += 1
        for idx in Types._detectValTypes(value):
            self.mCounts[idx] += 1
        return (self.mCounts[1] + self.mCounts[self.mReqType]) != cnt0

    def _checkType(self, idx, with_optional):
        cnt = self.mCounts[idx]
        if with_optional:
            cnt += self.mCounts[1]
        if cnt == self.mCounts[0]:
            return Types.sTypes[idx]

    def detect(self, with_optional = True):
        if self.mCounts[0] == 0:
            return "undef"
        if self.mReqType > 0:
            ret = self._checkType(self.mReqType, with_optional)
            if ret:
                return ret
        for idx in range(2, 9):
            ret = self._checkType(idx, with_optional)
            if ret:
                return ret
        return "json"

    def empty(self):
        return self.mCounts[0] == self.mCounts[1]

    def getTotalCount(self):
        return self.mCounts[0]

    def getEmptyCount(self):
        return self.mCounts[1]

