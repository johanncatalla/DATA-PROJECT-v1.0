import tkinter as tk
from tkinterdnd2 import DND_FILES
import pandas as pd
import hvplot.pandas
from tkinter import ttk

class CSVView(tk.Frame):
    # object that will be the frame of the gui that will contain the widgets 
    def __init__(self, parent, controller):
        super().__init__(parent)
        # creating the listbox then binding to the different events
        self.controller = controller
        self.file_name_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray")
        self.file_name_listbox.place(relheight=0.5, relwidth=0.25)
        # registers the listbox on the drag-and-drop functionality using DnD2
        self.file_name_listbox.drop_target_register(DND_FILES)
        # binds the listbox to dnd
        self.file_name_listbox.dnd_bind("<<Drop>>", self.controller.drop_inside_list_box)
        # binds the lsitbox to double click to open the file
        self.file_name_listbox.bind("<Double-1>", self.controller._display_file)
        
        # creates the entry box and binds it to the enter/return key
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.65, height=20, anchor=tk.NW)
        self.search_entrybox.bind("<Return>", self.controller.search_table)

        # Connect data table to search page // Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(y=25, relx=0.25, relwidth=0.75, relheight=0.47)
    
        self.input_tree = VizTable(parent)
        self.input_tree.place(rely=0.5, relheight=0.5, relwidth=0.25)
         # dictionary of filename: filepath pair to display in the listbox and treeview

        self.visual = CanvasViz(parent)
        self.visual.place(rely=0.5, relx=0.25, relwidth=0.75, relheight=0.47,)

        # Options list for search bar
        self.search_options = ["Display All Columns", "Display Inputted Columns"]
        
        # Stringvar to interact with the option menu
        self.search_val = tk.StringVar(parent)
        # Set dafault behavior to ignore case
        self.search_val.set("Display All Columns") 
        
        # Option menu for the search bar // change behavior of search
        self.option_menu = tk.OptionMenu(parent, self.search_val, *self.search_options)
        self.option_menu.place(width=190, relx=1, height=24, anchor=tk.NE)

        self.path_map = {}

class DataTable(ttk.Treeview):
    # Treeview object to display dataframe
    def __init__(self, parent):
        super().__init__(parent)
        
        self.master = parent
        # horizontal and vertical scrollbars
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        # Change style of treeview
        style = ttk.Style(self)
        style.theme_use("default")
        style.map("Treeview")

        # Empty Dataframe object for the treeview to use later
        self.stored_dataframe = pd.DataFrame()

class CanvasViz(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)

class VizTable(ttk.Treeview):
    def __init__(self,parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")    
