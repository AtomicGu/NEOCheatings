import xml.etree.ElementTree as ET
import tkinter as TK
from PIL import Image as IM, ImageTk as IMTK
import os as OS

#GLOBAL VARS
DB_PATH = "../data/itemtypes.xml"
DB_PATH = r"F:\GAMES\0-SteamGames\steamapps\common\NEO Scavenger\data\itemtypes.xml"
IMG_PATH = "F:\\GAMES\\0-SteamGames\\steamapps\\common\\NEO Scavenger\\img\\"
TABLE_PATH = "./0/data/treasuretable.xml"
TABLE_PATH = r"F:\GAMES\0-SteamGames\steamapps\common\NEO Scavenger\DetoritShopping\0\data\treasuretable - 副本.xml"
TABLE_BEGIN = None
TABLE_MID = None
TABLE_END = None
DB = None #type: database
TREASURES = None

#PUBLIC CLASSES
class table:
    def __init__(self,id,group_id,sub_group_id,name,description,image_list):
        self.id = id
        self.nGroupID = group_id
        self.nSubgroupID = sub_group_id
        self.strName = name
        self.strDesc = description
        for i in image_list:
            if "Stored" in i:
                self.vImageList = i
                break
        else:
            self.vImageList = image_list[0]
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

    def size(self) -> int:
        return len(self._data_tab)

    def search(self,token):
        return self._search_tab[token]

    def tokens(self):
        return self._search_tab.keys()

#PUBLIC FUNCTIONS
def __init__():
    global DB
    global TABLE_BEGIN
    global TABLE_MID
    global TABLE_END
    global listbox_items
    DB = import_database(DB_PATH)
    ch_itm(DB["1"])
    TABLE_BEGIN = []
    TABLE_MID = []
    TABLE_END = []
    fin = open(TABLE_PATH)
    for i in fin:
        if "aTreasures" in i:
            a = i.find("aTreasures")
            TABLE_MID.append(i[:a + 12:])
            i = i[a + 12::]
            b = i.find("</")
            TABLE_MID.append(i[:b:])
            TABLE_MID.append(i[b::])
            break
        else:
            TABLE_BEGIN.append(i)
    for i in fin:
        TABLE_END.append(i)
    fin.close()
    for i in TABLE_MID[1].split(","):
        listbox_items.insert("end",i)
    return

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

def image_png(png_name: str) -> IMTK.PhotoImage:
    img = IM.open(IMG_PATH + png_name)
    return IMTK.PhotoImage(img)

def get_itm(id: str) -> table:
    id = id.split("x")[0].split(".")
    return DB[DB.search(id[0])[id[1]]]

def ch_itm(item: table):
    global lable_pic_pic
    global lable_pic
    global lable_desc
    global entry_searchbox
    lable_pic_pic = image_png(item.vImageList)
    lable_pic["image"] = lable_pic_pic
    lable_desc["text"] = "strDesc: " + item.strDesc
    return

#TOP window
TOP = TK.Tk()
TOP.geometry("370x400")
TOP.title(OS.path.abspath(TABLE_PATH))
TOP.resizable(0,0)

#frame left
frame_left = TK.Frame(TOP)
frame_left.pack(side="left",fill="y")

#---frame list&del
frame_lt = TK.Frame(frame_left)
frame_lt.pack(side="top")

#-------scrollbar
scrollbar_items = TK.Scrollbar(frame_lt)
scrollbar_items.pack(side = "left",fill="y")

#-------item list
def listbox_items_f(event):
    '''select an item'''
    global listbox_items
    cur = listbox_items.curselection()
    if cur != tuple():
        ch_itm(get_itm(listbox_items.get(cur)))
    return
listbox_items = TK.Listbox(frame_lt,height=20,yscrollcommand=scrollbar_items.set)
scrollbar_items["command"] = listbox_items.yview
listbox_items.bind("<ButtonRelease-1>",listbox_items_f)
listbox_items.pack(side="left")

#-------del button
def button_del_f():
    global listbox_items
    cur = listbox_items.curselection()
    if cur != tuple():
        listbox_items.delete(cur)
    return
button_del = TK.Button(frame_lt,command=button_del_f,text="del")
button_del.pack(side="bottom")

#---frame entry&add
frame_lb = TK.Frame(frame_left)
frame_lb.pack(side="bottom")

#-------save button
def button_save_f():
    '''save'''
    global listbox_items
    global TABLE_MID
    TABLE_MID[1] = listbox_items.get(0)
    for i in range(1,listbox_items.size()):
        TABLE_MID[1] += "," + listbox_items.get(i)
    fout = open(TABLE_PATH,"w")
    fout.writelines(TABLE_BEGIN)
    fout.writelines(TABLE_MID)
    fout.writelines(TABLE_END)
    fout.close()
    return
button_save = TK.Button(frame_lb,command=button_save_f,text="save")
button_save.pack(side="left")

#-------add entry
entry_add = TK.Entry(frame_lb,width=17)
entry_add.pack(side="left")

#-------add button
def button_add_f():
    def check(input: str) -> bool:
        ok = True
        try:
            id,sta,amt = input.split("x")
            gid,sid = id.split(".")
        except:
            ok = False
        return ok
    new = entry_add.get()
    if check(new):
        listbox_items.insert("end",new)
    return
button_add = TK.Button(frame_lb,command = button_add_f,text="add")
button_add.pack(side="right")

#---picture box
lable_pic = TK.Label(TOP)
lable_pic_pic = None
lable_pic.place(x=275,y=150,anchor="c")

#---desc
lable_desc = TK.Label(TOP,wraplength=150,justify="left")
lable_desc.place(x=200,y=300)

#mainloop
__init__()
TOP.mainloop()
