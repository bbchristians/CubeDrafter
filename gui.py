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
CARD_PAD_X = 5
CARD_PAD_Y = 5
MAX_POSSIBLE_ROWS = 3
RANDOM_LEFT_PADDING = 25
LEFT_PADDING = 228
DRAFT_WINDOW_HEIGHT = 637

class Application(tk.Frame):

  draft = None
  pick_buttons = []

  def __init__(self, master=None, draft=None):
    super().__init__(master)
    self.draft = draft
    
    # Add self to the draft's observer
    self.draft.add_gui(self)
    
    # Pack self
    self.pack()
    
    # Define and pack scrollbar
    scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
    scrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
    
    # Define and pack card canvas
    self.canvas = tk.Canvas(self, bd=1, highlightthickness=0, yscrollcommand=scrollbar.set, height=DRAFT_WINDOW_HEIGHT)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
    scrollbar.config(command=self.canvas.yview)
    
    # Calculate the canvas window width and height
    draft_width = (CARD_WIDTH+(2*CARD_PAD_X))*NO_DRAFT_COL
    draft_height = (CARD_HEIGHT+(2*CARD_PAD_Y))*MAX_POSSIBLE_ROWS
    
    # Define the interior frame that will be scrolled
    self.interior = interior = tk.Frame(self.canvas, width=draft_width, height=draft_height)
    self.interior.pack_propagate(0)
    interior_id = self.canvas.create_window(0, 0, window=interior, anchor=tk.NW)
    
    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(event):
    
      # update the scrollbars to match the size of the inner frame
      size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
      
      self.canvas.config(scrollregion="0 0 %s %s" % size)
      
      if interior.winfo_reqwidth() != self.canvas.winfo_width()
        # update the canvas's width to fit the inner frame
        self.canvas.config(width=interior.winfo_reqwidth())

    interior.bind('<Configure>', _configure_interior)

    def _configure_canvas(event):
      if interior.winfo_reqwidth() != self.canvas.winfo_width():
        # update the inner frame's width to fill the canvas
        self.canvas.itemconfigure(interior_id, width=self.canvas.winfo_width())
        
    self.canvas.bind('<Configure>', _configure_canvas)
    
    # Add mouse wheel scroll
    def _on_mousewheel(event):
      self.canvas.yview_scroll(-1*int(event.delta/70), "units")
      
    self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Render the first pack
    if self.draft is not None:
    
      self.render_humans_pack()

    
  def render_pack(self, cards):
  
    # Remove all the old cards
    for button in self.pick_buttons:
    
      button.destroy()
      
    # clear pick_buttons
    self.pick_buttons = []

    # Define row, col, and count vars
    r = 0
    c = 0
    card_num = 0
    
    for card in cards:
    
      # Try to create a button that correlates to picking the imposed card
      try:
        b=tk.Button(self.interior,relief=tk.FLAT, command=lambda i=card_num: self.draft.make_player_pick(i))
        
        # Store a reference to the button later to easily delete it
        self.pick_buttons += [b]
        
        # Get the Multiverse ID which is the filename of the image
        mvid = extract_multiverseid(card.image_url)
        image_path = IMAGE_DIR + mvid + IMAGE_EXT
        
        # Try to load the image locally, if not found, then retrieve it
        try:
        
          image = Image.open(image_path)
          
        except FileNotFoundError:
        
          urllib.request.urlretrieve(card.image_url, image_path)
          image = Image.open(image_path)

        #image = image.crop((0,0,CARD_WIDTH,32))
        photo = ImageTk.PhotoImage(image)
        
        # Add the image to the button
        b.config(image=photo,width=CARD_WIDTH,height=CARD_HEIGHT)
        b.image = photo
        
        # Place the card on the canvas according to its position in the sorted pack
        card_x = LEFT_PADDING + CARD_PAD_X + c*((2*CARD_PAD_X)+CARD_WIDTH)
        card_y = CARD_PAD_Y + r*((2*CARD_PAD_Y)+CARD_HEIGHT)
        b.place(x=card_x, y=card_y, anchor=tk.NE)
        
        # Increment counting vars
        c += 1
        if c >= NO_DRAFT_COL:
        
          r += 1
          c = 0
          
        card_num += 1
        
      # Generic error report
      except tk.TclError as err:
      
        print("oops: " + str(err))
        
    
  def render_humans_pack(self):
  
    #Renders the Human player's pack
  
    self.render_pack(self.draft.get_players_pack())

    
def extract_multiverseid(url):

  return (((url.split("multiverseid="))[1]).split("&type=card"))[0]
  
  
def make_draft(pool):

  # Make Packs
  packs = CardPack.create_packs(pool, no_packs=24, no_rare=2, no_uncommon=4, no_common=9)

  draft = Draft()

  player = HumanDrafter("me", packs[0:3], draft, gui=True)
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
  root.resizable(0,0)
  
  app = Application(master=root, draft=draft)
  app.mainloop()
  
  
  
if __name__ == "__main__":

  main()