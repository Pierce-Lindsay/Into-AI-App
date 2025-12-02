import customtkinter as ctk
from PIL import Image
from poop import AddPlayer
from PlayerProfile import PlayerProfile
from TeamSummary import TeamSummary


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1200x600")

        self.page1 = AddPlayer(self, self.show_page2, self.show_page3)
        self.page2 = PlayerProfile(self, self.show_page1, self.show_page3)
        self.page3 = TeamSummary(self, self.show_page1, self.show_page2)

        #Start with only page 3
        self.page2.pack_forget()
        self.page1.pack_forget()


    def show_page1(self):
        print("Showing Page 1")
        self.page2.pack_forget()
        self.page3.pack_forget()
        self.page1.pack(fill="both", expand=True)

    def show_page2(self):
        print("Showing Page 2")
        self.page1.pack_forget()
        self.page3.pack_forget()
        self.page2.pack(fill="both", expand=True)

    def show_page3(self):
        print("Showing Page 3")
        self.page1.pack_forget()
        self.page2.pack_forget()
        self.page3.pack(fill="both", expand=True)



if __name__ == "__main__":
    app = App()
    app.mainloop()
