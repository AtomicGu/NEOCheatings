import tkinter as TK
import tkinter.ttk as TTK
import XMLReader as XR
from PIL import Image as IM, ImageTk as IMTK

#GLOBAL VARS
XML_PATH = r"F:\GAMES\0-SteamGames\steamapps\common\NEO Scavenger\data\itemtypes.xml"
IMG_PATH = "F:\\GAMES\\0-SteamGames\\steamapps\\common\\NEO Scavenger\\img\\"
DB = XR.import_database(XML_PATH)
ALL_ITEMS = list()

#PUBLIC FUNCTIONS
def init():
    global DB
    global treeview_items
    global ALL_ITEMS
    for i in range(1,DB.size() + 1):
        itm = DB[str(i)]
        ALL_ITEMS.append(itm.nGroupID + "." + itm.nSubgroupID + "|" + itm.strName + "|" + itm.strDesc)
    ch_tree(ALL_ITEMS)
    ch_itm(["5","3"])
    return

def items_sort(x: str) -> tuple:
    id = x.split("|")[0]
    a,b = id.split(".")
    return (int(a),int(b))

def ch_tree(items: list):
    global treeview_items
    global DB
    treeview_items.delete(*treeview_items.get_children())
    items.sort(key=items_sort)
    for i in items:
        ID,strName,strDesc = i.split("|")
        nGroupID = ID.split(".")[0]
        try:
            treeview_items.insert(nGroupID,"end",ID,text=ID + " " + strDesc)
        except TK.TclError:
            treeview_items.insert("","end",nGroupID,text=nGroupID + " " + strName)
            treeview_items.insert(nGroupID,"end",ID,text=ID + " " + strDesc)
    return

def get_png(png_name: str) -> IMTK.PhotoImage:
    img = IM.open(IMG_PATH + png_name)
    return IMTK.PhotoImage(img)

def ch_itm(id: list):
    global lable_picbox_pic
    global lable_picbox
    global lable_name
    global lable_desc
    global entry_searchbox
    item = DB[DB.search(id[0])[id[1]]]
    lable_picbox_pic = get_png(item.vImageList[0])
    lable_picbox["image"] = lable_picbox_pic
    lable_name["text"] = "strName: " + item.strName
    lable_desc["text"] = "strDesc: " + item.strDesc
    entry_searchbox.delete(0,"end")
    entry_searchbox.insert(0,item.nGroupID + "." + item.nSubgroupID + "x1.0x1-1")
    return

#top window
TOP = TK.Tk()
TOP.geometry("550x500")
TOP.title("NEOAnalyzer")
TOP.resizable(0,0)

#search box
entry_searchbox = TK.Entry(TOP,width = 16)
entry_searchbox.place(x=330,y=255)

#search button
def search():
    id = entry_searchbox.get().split("x")[0].split(".")
    if id[0].startswith("id"):
        id = DB[id[0].split()[1]]
        ch_itm([id.nGroupID,id.nSubgroupID])
    return
    ch_itm(id)
    return
button_search = TK.Button(TOP,command=search,text="Analyze")
button_search.place(x=450,y=250)

#items frame
frame_items = TK.Frame(TOP)
frame_items.place(x=0,y=0)

#---treeview frame
frame_treeview = TK.Frame(frame_items)
frame_treeview.pack(side="top")

#-------item treeview
def select_itm(event):
    global treeview_items
    global search_box
    id = treeview_items.item(treeview_items.focus())["text"].split()[0]
    if "." in id:
        ch_itm(id.split("."))
    return
treeview_items = TTK.Treeview(frame_treeview,height=23,show="tree")
treeview_items.column("#0",width=300)
treeview_items.bind("<ButtonRelease-1>",select_itm)
treeview_items.pack(side="right")

#-------scrollbar
scrollbar_items = TK.Scrollbar(frame_treeview,command=treeview_items.yview)
treeview_items["yscrollcommand"] = scrollbar_items.set
scrollbar_items.pack(side = "left",fill="y")

#---filter frame
frame_filter = TK.Frame(frame_items)
frame_filter.pack(side="bottom")

#-------filter entry
entry_filter = TK.Entry(frame_filter,width=30)
entry_filter.pack(side="left")

#-------filter botton
def filter():
    temp = []
    token = entry_filter.get()
    if token == "":
        ch_tree(ALL_ITEMS)
        return
    for i in ALL_ITEMS:
        if token in i:
            temp.append(i)
    ch_tree(temp)
    return
button_filter = TK.Button(frame_filter,text="search",command=filter,width=7)
button_filter.pack(side="right")

#picbox
lable_picbox = TK.Label(TOP)
lable_picbox_pic = None
lable_picbox.place(x=430,y=100,anchor = "c")

#name
lable_name = TK.Label(TOP)
lable_name.place(x = 330,y = 280)

#desc
lable_desc = TK.Label(TOP,wraplength=170,justify="left")
lable_desc.place(x = 330,y = 300)

#mainloop
init()
TOP.mainloop()
