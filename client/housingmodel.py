from housingutils import *
import json
class StaticHousingModel:
    def __init__(self, housingname, uploader, housesize: int, tags, items, uploadtime):
        self.houisngname = housingname
        self.uploader = uploader
        self.housesize = housesize
        self.tags = tags
        self.items = items
        self.uploadtime = uploadtime
        self.itemshash = stringtomd5(self.items)

    def ToJsonStr(self) -> str:
        return json.dumps(self, default=lambda o: o.__dict__)

if __name__ == "__main__":
    with open("n.json", 'r') as _file:
        items = _file.read()
    housing = StaticHousingModel("John's housing", "Oliver", 0, ["tag1", "tag2"], items, GetToday())
    print(housing.ToJsonStr())
    with open(housing.itemshash, "w") as f:
        f.write(housing.ToJsonStr())
    