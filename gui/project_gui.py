import tkinter
import tkinter.ttk as ttk
import autofill
from search import search
from PIL import ImageTk, Image

DEFAULT_FONT = ('Helvetica', 20)
title_font = ('Helvetica', 10, 'bold')

class SexTable:
    def __init__(self, root):
        sex_label = tkinter.Label(master=root, text="Sex", font=('Helvetica', 20, 'bold'))
        sex_label.grid(row=7, column=1)

        male_label = tkinter.Label(master=root, text="Male", font=DEFAULT_FONT)
        male_label.grid(row=8, column=0)

        female_label = tkinter.Label(master=root, text="Female", font=DEFAULT_FONT)
        female_label.grid(row=9, column=0)

        un_label = tkinter.Label(master=root, text="Unknown", font=DEFAULT_FONT)
        un_label.grid(row=10, column=0)


        self.male_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.male_e.grid(row=8, column=1)

        self.female_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.female_e.grid(row=9, column=1)

        self.un_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.un_e.grid(row=10, column=1)
    
    def update(self, summary):
        self.male_e.config(text = summary["Sex"]["male"])
        self.female_e.config(text = summary["Sex"]["female"])
        self.un_e.config(text = summary["Sex"]["unknown"])

class AgeTable:
    def __init__(self, root):
        age_label = tkinter.Label(master=root, text="Age", font=('Helvetica', 20,'bold'))
        age_label.grid(row=2, column=1)

        adult_label = tkinter.Label(master=root, text="Adult", font=DEFAULT_FONT)
        adult_label.grid(row=3, column=0)

        juv_label = tkinter.Label(master=root, text="Juvenile", font=DEFAULT_FONT)
        juv_label.grid(row=4, column=0)

        un_label = tkinter.Label(master=root, text="Unknown", font=DEFAULT_FONT)
        un_label.grid(row=5, column=0)


        self.adult_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.adult_e.grid(row=3, column=1)

        self.juv_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.juv_e.grid(row=4, column=1)

        self.un_e = tkinter.Label(master=root, text="0", font=DEFAULT_FONT)
        self.un_e.grid(row=5, column=1)

    def update(self, summary):
        self.adult_e.config(text = summary["Age"]["adult"])
        self.juv_e.config(text = summary["Age"]["juvenile"])
        self.un_e.config(text = summary["Age"]["unknown"])

class SearchApplication:
    def __init__(self):
        self.search = search() # Initial data

        self._root_window = tkinter.Tk()

        fram = tkinter.Frame(self._root_window)

        tkinter.Label(master=fram, text="Please enter common or formal species name", font=('Helvetica', 16, 'bold')).pack(side=tkinter.LEFT)

        self.edit = autofill.AutocompleteEntry(fram)
        self.edit.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=2)
        self.edit.focus_set()

        search_button = tkinter.Button(fram, text="Search")
        search_button.pack(side=tkinter.RIGHT)
        fram.grid(row = 0, column=0, columnspan=10)


        search_button.config(command=self.find)

        self.agetable = AgeTable(self._root_window)
        self.sextable = SexTable(self._root_window)

        total_label = tkinter.Label(master=self._root_window, text="Total:", font=('Helvetica', 20,'bold'))
        total_label.grid(row=1, column=0)

        self.total_e = tkinter.Label(master=self._root_window, text="0", font=DEFAULT_FONT)
        self.total_e.grid(row=1, column=1)

        self.tab_main = ttk.Notebook(master=self._root_window)
        self.tab_main.grid(row=1, column=2, rowspan=12, columnspan=10, sticky=tkinter.NW)

        self.tab_map = tkinter.Frame(master=self.tab_main)
        self.tab_image = tkinter.Frame(master=self.tab_main)
        self.tab_table = tkinter.Frame(master=self.tab_main)
        self.initial_table()
        self.scorable_image()
        self.initial_map()

        self.tab_main.add(self.tab_map, text="Map")
        self.tab_main.add(self.tab_table, text="Table")
        self.tab_main.add(self.tab_image, text="Image")

        self._root_window.title("Wildlife diversity monitoring")
    
    def initial_map(self):
        img = Image.open("maps/initial.png")
        img = img.resize((760,400), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(img)

        self.map_canvas = tkinter.Canvas(master=self.tab_map, height=400, width=760)
        self.map_canvas.grid(row=0, column=0)
        
        self.map_image = self.map_canvas.create_image(5,5, image=tk_img, anchor=tkinter.NW)
        self.map_canvas.image = tk_img

    def update_map(self, name):
        #path = 'maps/"{}".png'.format(name)
        path = "maps/" + name + ".png"
        img = Image.open(path)
        img = img.resize((760, 400), Image.ANTIALIAS)
        tk_img = ImageTk.PhotoImage(img)
        #self.map_canvas.configure(image=tk_img)
        self.map_canvas.itemconfigure(self.map_image, image=tk_img)
        self.map_canvas.image = tk_img


    def initial_table(self):
        ybar = tkinter.Scrollbar(master=self.tab_table, orient="vertical")

        cols = ("ID", "Age", "Sex", "Camera ID", "Latitude", "Longitude", "Time")
        self.tree = ttk.Treeview(master=self.tab_table, show='headings', columns = cols, yscrollcommand=ybar.set, height=20)
        ybar['command'] = self.tree.yview

        for col in cols:
            self.tree.heading(col, text=col)
            if col == "Time":
                self.tree.column(col, width=160, anchor='w')
            else:
                self.tree.column(col, width=100, anchor='w')

        self.tree.grid(row=0, column=0)
        ybar.grid(row=0, column=1, sticky='ns')

    def find(self):
        word = self.edit.get()

        res, summary = self.search.search_data(word)

        self.draw_table(res)
        self.agetable.update(summary)
        self.sextable.update(summary)
        self.total_e.config(text = summary["Total"])

        for widget in self.scrollbar_frame.winfo_children():
            widget.destroy()

        check = True
        for img_id in res.keys():
            if check:
                self.update_map(res[img_id]["common name"])
                check = False
            ttk.Button(master=self.scrollbar_frame, text=img_id, width=105, command=lambda img_id=img_id:self.show_img(img_id)).pack()

    def show_img(self, image_id):
        path = image_id + ".jpg"
        img = self.search.search_img(path)

        root = tkinter.Toplevel()
        c = ttk.Frame(root)
        c.grid(row=0, column=0, sticky=tkinter.NSEW)

        canvas = tkinter.Canvas(master=c, width=1000, height=550)
        canvas.grid(row=0, column=0)
        
        canvas.create_image(5,5, image=img, anchor=tkinter.NW)
        canvas.image = img
    
        id_label = ttk.Label(master=c, text=image_id, font=('Helvetica', 20, 'bold'))
        id_label.grid(row=1, column=0)

    def scorable_image(self):
        canvas = tkinter.Canvas(master = self.tab_image)
        scrollbar = ttk.Scrollbar(master = self.tab_image, orient="vertical", command=canvas.yview)
        self.scrollbar_frame = ttk.Frame(canvas)

        self.scrollbar_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0,0), window=self.scrollbar_frame, anchor=tkinter.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.config(height=400, width=760)

        canvas.grid(row=0,column=0)
        scrollbar.grid(row=0, column=1, sticky='ns')

    
    def draw_table(self, res):
        key = list(res.keys())

        self.tree.delete(*self.tree.get_children())
        for i in range(len(res)):
            k = key[i]
            val = (k, res[k]['age'], res[k]['sex'], res[k]['camera_info']['ID'], res[k]['camera_info']['lat'], res[k]['camera_info']['long'], res[k]['time'])
            self.tree.insert("", "end", values=val)


    def run(self):
        self._root_window.mainloop()
        
        
if __name__ == "__main__":
    SearchApplication().run()