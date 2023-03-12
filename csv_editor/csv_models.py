import tkinter as tk
import pandas as pd
from tkinter import ttk
import csv

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

    def save_file_as(self, filename: str): # TODO write treeview
        """Saves the csv file as new file / write mode

        Args:
            filename (str): _description_
        """
        file = open(filename, 'w', newline='')
        csv_writer = csv.writer(file)
        header = columns
        csv_writer.writerow(header)

        for row in df_rows:
            csv_writer.writerow(row)
            

    def set_datatable(self, dataframe):
        """Copies the string version of the original dataframe to the spare dataframe for string query
        then draws the original dataframe to the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # takes the empty dataframe and stores it in the "dataframe" attribute
        self.stored_dataframe = dataframe.astype(str)
        # draws the dataframe in the treeview using the function _draw_table
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        """Draws/Inserts the data in the dataframe on the treeview

        Args:
            dataframe (DataFrame): opened dataframe in read mode
        """
        # clear any item in the treeview
        self.delete(*self.get_children())
        # create list of columns
        
        global columns
        columns = list(dataframe.columns) # TODO Use this list as headings for write
        
        # set attributes of the treeview widget
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        # insert the headings based on the list of columns
        for col in columns:
            self.heading(col, text=col)
    
        # convert the dataframe to numpy array then convert to list to make the data compatible for the Treeview
        global df_rows
        df_rows = dataframe.to_numpy().tolist()
        
        # insert the rows based on the format of df_rows
        for row in df_rows:
            self.insert("", "end", values=row)
        return None
    
    def find_value(self, pairs: dict):
        """search table for every pair in entry widget

        Args:
            pairs (dict): pairs of column search in the entry widget {country: PH, year: 2020}
        """
        column_keys = pairs.keys()
        option_value = self.master.search_val.get()
        print(option_value)
        # takes the empty dataframe and stores it in a property
        
        new_df = self.stored_dataframe[column_keys] # TODO option menu to change behavior
        
        
        # inputs each matched dataframe row in the stored dataframe based on entry box pair value
        for col, value in pairs.items():
            # query expression that checks if the column contains the inputted value
            
            query_string = f"`{col}`.str.contains('{value}', na=False)"
            # dataframe generated by query function to evaluate the columns with matched expression
            new_df = new_df.query(query_string, engine="python")
        # draws the dataframe in the treeview 
        self._draw_table(new_df)

    def reset_table(self):
        # resets the treeview by drawing the empty dataframe in the treeview
        self._draw_table(self.stored_dataframe)