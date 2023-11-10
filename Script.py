import tkinter, os, shutil, re


class main_app(tkinter.Frame):
    def __init__(self, master=None):
        # -- CREATE FRAME
        # @description: creates the overarching frame for the save manager
        # @params: master: tk interpreter, by default, none, but nominally a tkinter.Tk() object
        # @return: None
        super().__init__(master)                                            # -- create proxy object based on tk interpreter
        self.master = master                                                # -- assign tk interpreter to master property
        self.grid()                                                         # -- configure frame for grid layout
        self.master.title("Spirit Island Saves")                            # -- give the window a recognizable name
        self.main_folder=None                                               # -- create main_folder (site of active save) attribute
        self.save_folder=None                                               # -- create save_folder (storage location for saves) attribute
        self.active_save=None                                               # -- create active_save (the name of active save files) attribute
        self.full_save_path=None                                            # -- create full_save_path (full path to the active save file) attribute
        self.get_paths()                                                    # -- populate file paths
        self.save_window()                                                  # -- populate frame with widgets

    def get_paths(self):
    # -- POPULATE COMMON FILE PATHS
    # @description: reads the config.txt file for data
    # @params: None
    # @return: None
        with open('config.txt') as config:                                  # -- Open config file
            config_parse = config.read()                                    # -- read the file
            config_parse = re.split("\n", config_parse)                     # -- split the contents into lines
            for item in config_parse:                                       # -- itterate through each line
                key, value = re.split("=", item)                            # -- split each line into sets of keys and values
                if key == "main_folder":                                    # -- check if line identifies the main_folder path
                    self.main_folder = value                                # -- store the main_folder value
                if key == "save_folder":                                    # -- check if line identifies the save_folder
                    self.save_folder = value                                # -- store the save_folder value
                if key == "active_save":                                    # -- check if line identifies the name of the active save
                    self.active_save = value                                # -- store the value of the active save
            self.full_save_path = self.main_folder + "/" + self.active_save # -- create the full file path of the active save file

    def save_window(self):
        # -- POPULATE FRAME
        # @description: creats a variety of widgets and labels for managing saves
        # @params: None
        # @return: None
        self.new_name = tkinter.StringVar()                                 # -- CREATE INPUT BUFFER

        # -- CREATE SAVE BUTTON
        self.save_button = tkinter.Button(self,                             # -- CREATE SAVE BUTTON
                                          text="Save",                      # -- label as "Save"
                                          command=self.create_save,         # -- Associate button with create_save method
                                          width=10)                         # -- increased width for visual appearance
        self.save_button.grid(column=0, row=0)                              # -- place button on top row, left side

        # -- CREATE LOAD BUTTON
        self.load_button = tkinter.Button(self,                             # -- CREATE LOAD BUTTON
                                          text="Load",                      # -- label as "Load"
                                          command=self.load_save,           # -- associate button with load_save method
                                          width=10)                         # -- increased width for visual appearance
        self.load_button.grid(column=1, row=0)                              # -- place button on top row, middle

        # -- CREATE DELETE BUTTON
        self.delete_button = tkinter.Button(self,                           # -- CREATE DELETE BUTTON
                                            text="Delete",                  # -- label as "Load"
                                            command=self.delete_save,       # -- associate button with delete_save method
                                            width=10)                       # -- increased width for visual appearance
        self.delete_button.grid(column=2, row=0)                            # -- place button on top row, right

        # -- CREATE OUTPUT FIELD
        self.out_line = tkinter.Entry(self)                                 # -- CREATE OUTPUT FIELD
        self.out_line.grid(column=0, row=1, columnspan=3, sticky='WE')      # -- make field span full width
        if os.path.exists(self.full_save_path) == False:                    # -- Check if save file exits
            self.out_line.insert(0, "No Save Found")                        # -- warn user if no save is located
        else:                                                               # -- otherwise
            self.out_line.insert(0, "Hello")                                # -- Greet user
        self.out_line["state"] = 'disable'                                  # -- disable filed to prevent overwrite by user

        # -- CREATE INPUT FIELD LABEL
        self.name_label = tkinter.Label(self, text="New Save Name")         # -- CREATE INPUT FIELD LABEL
        self.name_label.grid(column=0, row=2, columnspan=3)                 # -- make label span full width

        # -- CREATE INPUT FIELD
        self.input_name = tkinter.Entry(self,                               # -- CREATE INPUT FIELD
                                        textvariable=self.new_name,         # -- associate field with input buffer
                                        width=40)                           # -- size field for full width
        self.input_name.grid(column=0, row=3, columnspan=3)                 # -- make field span full width

        # -- CREATE SAVE LIST LABEL
        self.list_label = tkinter.Label(self, text="Save File List")        # -- CREATE SAVE LIST LABEL
        self.list_label.grid(column=0, row=4, columnspan=3)                 # -- make label span full width
        

        # -- CREATE SAVE LIST BOX
        self.save_list = tkinter.Listbox(self, selectmode="SINGLE")         # -- CREATE SAVE LIST BOX
        self.save_list.grid(column=0, row=5, columnspan=3, sticky='WE')     # -- Make listbox span full width
        for files in os.listdir(self.save_folder):                          # -- check save folder
            self.save_list.insert(self.save_list.size(), files)             # -- add each save to list


    def update_output(self, new_output):
        # -- UPDATE out_line WIDGET
        # @description: performs tasks needed to consistently update out_line as needed
        # @params: new_output: string, text to be communicated to user
        # @return: None
        self.out_line["state"] = 'normal'                                   # -- set field to updatable state
        self.out_line.delete(0, 50)                                         # -- clear any contents in the field
        self.out_line.insert(0, new_output)                                 # -- write new_output to field
        self.out_line["state"] = 'disable'                                  # -- return field to protected state

    def create_save(self):
        # -- CREATE BACKUP OF SAVE FILE
        # @description: locates an active save file, and create a custom named backup
        # @params: None
        # @return: None
        new_save_name = self.new_name.get()                                 # -- reteive name from name_label
        if bool(new_save_name) == False:                                    # -- verify a name was provided
            self.update_output("Please provide a save name")                # -- warn user if no name was provided
            return                                                          # -- exit process to allow user to update
        if os.path.exists(self.full_save_path) == False:                    # -- check if a current save file exists
            self.update_output("No Save Found")                             # -- warn user if no save located
        else:                                                               # -- otherwise, a save was located
            full_new_save = self.save_folder + "/" + new_save_name          # -- format new save file name/path
            self.save_list.insert(self.save_list.size(), new_save_name)     # -- add save to the save list
            shutil.copyfile(self.full_save_path, full_new_save)             # -- copy the save file to the save folder
            self.update_output("{} Save Created".format(new_save_name))     # -- confirm successful save to user

    def load_save(self):
        # -- LOAD A SAVE FILE TO ACTIVE SAVE
        # @description: take the save file selected by the user, and make it the active save file
        # @params: None
        # @return: None
        sel = self.save_list.curselection()                                 # -- retrieve user selection from save list
        if not sel:                                                         # -- verify a selection was made
            self.update_output("Please select a save to load")              # -- if no selection was made, warn user
            return                                                          # -- end process so user can update
        file = self.save_list.get(sel)                                      # -- retrive save name from selection
        save_path = self.save_folder + "/" + file                           # -- format save file path
        shutil.copyfile(save_path, self.full_save_path)                     # -- copy backup save to active save
        self.update_output("{} loaded".format(file))                        # -- confirm successful load

    def delete_save(self):
        # -- REMOVE SAVE FILE
        # @description: delete the selected save file
        # @params: None
        # $return: None
        sel = self.save_list.curselection()                                 # -- retrieve user selection from save list
        if not sel:                                                         # -- verify a selection was made
            self.update_output("Please select a save to load")              # -- if no selection was made, warn user
            return                                                          # -- end process so user can update
        file = self.save_list.get(sel)                                      # -- retrive save name from selection
        save_path = self.save_folder + "/" + file                           # -- format save file path
        os.remove(save_path)                                                # -- delete the save file
        self.save_list.delete(sel)                                          # -- remove the save file from save list
        self.update_output("{} Deleted".format(file))                       # -- confirm successful deletion

if __name__ == '__main__':                                                  # -- main loop
    root = tkinter.Tk()                                                     # -- create a tk interpreter
    app = main_app(master=root)                                             # -- create instance of the main_app object, passing tk interpreter
    app.mainloop()                                                          # -- call app through mainloop event manager
