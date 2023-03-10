import tkinter as tk
import pandas as pd
from tkinter import ttk


class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        # horizontal and vertical scrollbars
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")

        # Empty Dataframe object for the treeview to use later
        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):
        # takes the empty dataframe and stores it in the "dataframe" attribute
        self.stored_dataframe = dataframe
        # draws the dataframe in the treeview using the function _draw_table
        self._draw_table(dataframe)

    def _draw_table(self,dataframe):
        # clear any item in the treeview
        self.delete(*self.get_children())
        # create list of columns
        columns = list(dataframe.columns)
        # set attributes of the treeview widget
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        # insert the headings based on the list of columns
        for col in columns:
            self.heading(col, text=col)
        
        # convert the dataframe to numpy array then convert to list to make the data compatible for the Treeview
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
        # takes the empty dataframe and stores it in a property
        new_df = self.stored_dataframe
        
        # inputs each matched dataframe row in the stored dataframe based on entry box pair value
        for col, value in pairs.items():
            # query expression that checks if the column contains the inputted value
            query_string = f"{col}.str.contains('{value}', na=False)"
            # dataframe generated by query function to evaluate the columns with matched expression
            new_df = new_df.query(query_string, engine="python")
        # draws the dataframe in the treeview 
        self._draw_table(new_df)

    def reset_table(self):
        # resets the treeview by drawing the empty dataframe in the treeview
        self._draw_table(self.stored_dataframe)