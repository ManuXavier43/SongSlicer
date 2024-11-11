import customtkinter as ctk

class App():
    #Start the app
    def __init__(self):
        #Make app window called root
        self.root = ctk.CTk()
        #Get screen size of the user
        self.screen_height = self.root.winfo_screenheight()
        self.screen_width = self.root.winfo_screenwidth()
        #Color scheme
        ctk.set_appearance_mode('light')
        ctk.set_default_color_theme('green')
        #Set screen size
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")

        #Create a frame to animate app
        self.frame = ctk.CTkFrame(master=self.root)
        #Set the window to fullscreen mode on startup with a short delay to centre it
        #Define an anonymous function using lambda to expand screen after a 10ms delay
        self.root.after(10, lambda: self.root.state("zoomed"))
        self.frame.pack(expand=True, fill='both')

        self.root.mainloop()
    def draw(self):
        #This will draw all the buttons and screen elements
        pass #Remove this line after adding code
App().startApp()