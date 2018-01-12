import tkinter as tk;
import sys;
import mtgsdk as mtg;
import base64;
from LocalCardLoader import LocalCardLoader;
import urllib.request;
from PIL import Image, ImageTk;
import random;
from CardPack import CardPack;
from Draft import Draft;
from HumanDrafter import HumanDrafter;
from AIDrafter import AIDrafter;

IMAGE_DIR = "Images/"
IMAGE_EXT = ".png"

NO_DRAFT_COL = 6
CARD_WIDTH = 223
CARD_HEIGHT = 311

class Application(tk.Frame):

  draft = None
  pick_buttons = []

  def __init__(self, master=None, draft=None):
    super().__init__(master)
    self.draft = draft
    self.draft.add_gui(self)
    self.pack()
    
    # Define and pack scrollbar
    scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    
    # Define and pack button canvas
    canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
    scrollbar.config(command=canvas.yview)
    
    self.interior = interior = tk.Frame(canvas)
    interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

    #listbox = tk.Listbox(self.master, yscrollcommand=scrollbar.set)
    
    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(event):
      # update the scrollbars to match the size of the inner frame
      size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
      canvas.config(scrollregion="0 0 %s %s" % size)
      if interior.winfo_reqwidth() != canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        canvas.config(width=interior.winfo_reqwidth())

    interior.bind('<Configure>', _configure_interior)

    def _configure_canvas(event):
      if interior.winfo_reqwidth() != canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        
    canvas.bind('<Configure>', _configure_canvas)
    
    if self.draft is not None:
    
      self.render_humans_pack()

    
  def render_pack(self, cards):
  
    for button in self.pick_buttons:
    
      button.grid_forget()

    r = 0
    c = 0
    card_num = 0
    
    
    
    for card in cards:
    
      try:
        #b=tk.Button(self,justify = tk.LEFT, command=lambda i=card_num: self.draft.make_player_pick(i))
        b=tk.Button(self.interior,relief=tk.FLAT, command=lambda i=card_num: self.draft.make_player_pick(i))

        self.pick_buttons += [b]
        
        mvid = extract_multiverseid(card.image_url)
        image_path = IMAGE_DIR + mvid + IMAGE_EXT
        
        try:
        
          image = Image.open(image_path)
          
        except FileNotFoundError:
        
          urllib.request.urlretrieve(card.image_url, image_path)
          image = Image.open(image_path)

        #image = image.crop((0,0,CARD_WIDTH,32))
        photo = ImageTk.PhotoImage(image)
        
        b.config(image=photo,width=CARD_WIDTH,height=CARD_HEIGHT)
        b.image = photo
        
        #listbox.insert(tk.END, b.pack())
        
        #b.grid(row=r, column=c)
        b.pack(padx=10, pady=5, side=tk.TOP)
        
        c += 1
        
        if c >= NO_DRAFT_COL:
        
          r += 1
          c = 0
          
        card_num += 1
          
      except tk.TclError as err:
      
        print("oops: " + str(err))
        
    #listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    #scrollbar.config(command=listbox.yview)

    #self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
    #self.quit.pack(side="bottom")
    
  def render_humans_pack(self):
  
    self.render_pack(self.draft.get_players_pack())
    
    
  def scrollbartest(self):
  
    scrollbar = tk.Scrollbar(self.master)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox = tk.Listbox(self.master, yscrollcommand=scrollbar.set)
    for i in range(1000):
        listbox.insert(tk.END, str(i))
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)

    scrollbar.config(command=listbox.yview)

    
def extract_multiverseid(url):

  return (((url.split("multiverseid="))[1]).split("&type=card"))[0]
  
  
def make_draft(pool):

  # Make Packs
  packs = CardPack.create_packs(pool, no_packs=24, no_rare=2, no_uncommon=4, no_common=9)

  draft = Draft()

  player = HumanDrafter("me", packs[0:3], draft)
  del packs[0:3]
  
  draft.add_human_drafter(player)
  
  for i in range(7):
  
    ai = AIDrafter("AI{}".format(i), packs[0:3])
    
    del packs[0:3]
    
    draft.add_ai_drafter(ai)
    
  draft.start_draft()
  
  return draft
  

def main():

  
  c_import = LocalCardLoader("SampleCube.csv")
  pool = c_import.get_cards("cube1")
  
  draft = make_draft(pool)
  
  root = tk.Tk()
  root.title("CubeDrafter")
  
  app = Application(master=root, draft=draft)
  app.mainloop()
  
  
  
if __name__ == "__main__":

  main()