import xml.etree.ElementTree as ET

class table:
    def __init__(self,id,group_id,sub_group_id,name,description,image_list):
        self.id = id
        self.nGroupID = group_id
        self.nSubgroupID = sub_group_id
        self.strName = name
        self.strDesc = description
        self.vImageList = image_list
        return

class database:
    def __init__(self):
        self._data_tab = dict()
        self._search_tab = dict()
        return

    def __getitem__(self,key):
        return self._data_tab[key]

    def insert(self,tab: table):
        self._data_tab[tab.id] = tab
        try:
            self._search_tab[tab.nGroupID][tab.nSubgroupID] = tab.id
        except KeyError:
            self._search_tab[tab.nGroupID] = dict()
            self._search_tab[tab.nGroupID][tab.nSubgroupID] = tab.id
        return

    def size(self)->int:
        return len(self._data_tab)

    def search(self,token):
        return self._search_tab[token]

    def tokens(self):
        return self._search_tab.keys()

def import_database(file_path: str) -> database:
    DB = database()
    root = ET.parse(file_path)
    r_database = root.find("database")
    for rd_table in r_database.iter("table"):
        temp = dict()
        for rdt_column in rd_table.iter("column"):
            temp[rdt_column.attrib["name"]] = rdt_column.text
        DB.insert(table(temp["id"],
                        temp["nGroupID"],
                        temp["nSubgroupID"],
                        temp["strName"],
                        temp["strDesc"],
                        temp["vImageList"].split(",")))
    return DB

if __name__ == "__main__":
    PATH = r"F:\GAMES\0-SteamGames\steamapps\common\NEO Scavenger\data\itemtypes.xml"
    DB = import_database(PATH)
    self = DB["1"]
    print(self.id)
    print(self.nGroupID)
    print(self.nSubgroupID)
    print(self.strName)
    print(self.strDesc)
    print(self.vImageList)
