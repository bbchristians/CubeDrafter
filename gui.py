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
MAX_POSSIBLE_ROWS = 3
CARD_WIDTH = 223
CARD_HEIGHT = 311
CARD_PAD_X = 3
CARD_PAD_Y = 3
LEFT_PADDING = 228 # There is some random negative padding that happens to be one card width + 1 padding shifting the pack to the left
CARD_SCALE = .75
CARD_CROPPED_HEIGHT = 32
DRAFT_PICKS_PADDING = 15
WINDOW_HEIGHT = 1000
RIGHT_HAND_DISPLAY_WIDTH = 250
MAX_CARD_CMC = 6

class DraftWindow(tk.Frame):

  draft = None
  pick_buttons = []
  pick_labels = []
  end_of_pack_location = 0
  card_display_label = None

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
    
    # Calculate height of draft window
    draft_window_height = (CARD_HEIGHT * CARD_SCALE * 2) + (4 * CARD_PAD_Y)
    
    # Define and pack card canvas
    self.canvas = tk.Canvas(self, bd=1, highlightthickness=0, height=WINDOW_HEIGHT, yscrollcommand=scrollbar.set)
    self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
    scrollbar.config(command=self.canvas.yview)
    
    # Calculate the canvas window width and height
    draft_width = (get_image_scaled_width()+(2*CARD_PAD_X))*NO_DRAFT_COL + RIGHT_HAND_DISPLAY_WIDTH
    draft_height = WINDOW_HEIGHT
    
    # Define the interior frame that will be scrolled
    self.interior = tk.Frame(self.canvas, width=draft_width, height=draft_height)
    self.interior.pack_propagate(0)
    interior_id = self.canvas.create_window(0, 0, window=self.interior, anchor=tk.NW)
    
    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(event):
    
      # update the scrollbars to match the size of the inner frame
      size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
      
      self.canvas.config(scrollregion="0 0 %s %s" % size)
      
      if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
        # update the canvas's width to fit the inner frame
        self.canvas.config(width=self.interior.winfo_reqwidth())

    self.interior.bind('<Configure>', _configure_interior)

    def _configure_canvas(event):
      if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
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
  
    # If the last card of the last pack was just drafted, move the pool display up
    if len(cards) is 0:
    
      self.end_of_pack_location = 0
  
    # Remove all the old cards
    for button in self.pick_buttons:
    
      button.destroy()
      
    # Clear pick_buttons
    self.pick_buttons = []

    # Define row, col, and count vars
    r = 0
    c = 0
    card_num = 0
    
    for card in cards:
    
      # Try to create a button that correlates to picking the imposed card
      try:
        b=tk.Button(self.interior, relief=tk.FLAT, command=lambda i=card_num: self.draft.make_player_pick(i))
        
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

        # Calculate the scaled dimensions and resize the card images
        image_scaled_height = get_image_scaled_height()
        image_scaled_width = get_image_scaled_width()
        image = image.resize((image_scaled_width, image_scaled_height), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        
        # Add the image to the button
        b.config(image=photo,width=image_scaled_width,height=image_scaled_height)
        b.image = photo
        
        # Place the card on the canvas according to its position in the sorted pack
        card_x = (LEFT_PADDING*CARD_SCALE) + CARD_PAD_X + c*((2*CARD_PAD_X)+image_scaled_width)
        card_y = CARD_PAD_Y + r*((2*CARD_PAD_Y)+image_scaled_height)
        b.place(x=card_x, y=card_y, anchor=tk.NE)
        
        # Link the card button mouse overs so that mousing over highlights the card in the card display
        self.bind_widget_mouseover(b, card)
        
        # Set the end of pack location if it has increased (This is to for displaying the selected cards)
        self.end_of_pack_location = max(self.end_of_pack_location, card_y + (CARD_HEIGHT * CARD_SCALE) + CARD_PAD_Y)
        
        # Increment counting vars
        c += 1
        if c >= NO_DRAFT_COL:
        
          r += 1
          c = 0
          
        card_num += 1
        
      # Generic error report
      except tk.TclError as err:
      
        print("oops: " + str(err))
        
        
  def render_picks(self, cards):
  
    # Remove all old picks
    for label in self.pick_labels:
    
      label.destroy()
      
    self.pick_labels = []
  
    # Draw a line to separate draft picks and the pack TODO MAKE WORK
    self.canvas.create_line(self.end_of_pack_location + 5, 0, 0, 0)
    self.canvas.pack()
  
    # Define card CMC y positions
    cmc_heights = [DRAFT_PICKS_PADDING] * 100
  
    for card in cards:
    
      # Try to create a label that correlates to picking the imposed card
      try:
      
        # Get the Multiverse ID which is the filename of the image
        mvid = extract_multiverseid(card.image_url)
        image_path = IMAGE_DIR + mvid + IMAGE_EXT
        
        # Try to load the image locally, if not found, then retrieve it from the web
        try:
        
          image = Image.open(image_path)
          
        except FileNotFoundError:
        
          urllib.request.urlretrieve(card.image_url, image_path)
          image = Image.open(image_path)
          
        image_scaled_width = get_image_scaled_width()
        image_scaled_height = get_image_scaled_height()
        image_crop_height = CARD_CROPPED_HEIGHT*CARD_SCALE
          
        image = image.resize((image_scaled_width, image_scaled_height), Image.ANTIALIAS)
        #image = image.crop((0,0,CARD_WIDTH*CARD_SCALE,image_crop_height))
        photo = ImageTk.PhotoImage(image)
        
        # Create the label and add the image to the label
        label = tk.Label(self.interior, image=photo, bg="black", borderwidth=0, highlightthickness=0)
        label.image = photo
        self.pick_labels += [label]
        
        # Get the CMC of the card (For placement)
        card_cmc = 0
        try:
        
          card_cmc = min(MAX_CARD_CMC, int(card.cmc))
          
        except ValueError:
        
          print("Invalid CMC for card \"{}\": {}".format(card.name, card.cmc))
        
        
        # Determine the height at which the card should be placed
        height = cmc_heights[card_cmc]
        cmc_heights[card_cmc] = height + image_crop_height
        
        # Place the card on the canvas according to its position in the sorted pack
        card_x = (LEFT_PADDING*CARD_SCALE) + CARD_PAD_X + card_cmc*((2*CARD_PAD_X)+image_scaled_width)
        card_y = self.end_of_pack_location + height
        label.place(x=card_x, y=card_y, anchor=tk.NE)
        
        # Link the card label mouse overs so that mousing over highlights the card in the card display
        self.bind_widget_mouseover(label, card)
        
      # Generic error report
      except tk.TclError as err:
      
        print("oops: " + str(err))
        
    
  def render_humans_pack(self):
  
    #Renders the Human player's pack
  
    self.render_pack(self.draft.get_players_pack())
    
  def render_humans_picks(self):
  
    self.render_picks(self.draft.get_players_picks())
    
  def set_card_display(self, card):
  
    # Try to create a label that correlates to picking the imposed card
    try:
    
      # Get the Multiverse ID which is the filename of the image
      mvid = extract_multiverseid(card.image_url)
      image_path = IMAGE_DIR + mvid + IMAGE_EXT
      
      # Try to load the image locally, if not found, then retrieve it from the web
      try:
      
        image = Image.open(image_path)
        
      except FileNotFoundError:
      
        urllib.request.urlretrieve(card.image_url, image_path)
        image = Image.open(image_path)
      
      photo = ImageTk.PhotoImage(image)
      
      # Create the label and add the image to the label
      label = tk.Label(self.interior, image=photo, bg="black", borderwidth=0, highlightthickness=0)
      label.image = photo
      #self.pick_labels += [label]
      
      # Place the card label 
      pack_card_scaled_width = get_image_scaled_width()
      card_x = CARD_PAD_X + NO_DRAFT_COL*((2*CARD_PAD_X)+pack_card_scaled_width) + 10
      label.place(x=card_x, y=CARD_PAD_Y, anchor=tk.NW)
      
      # Preserve label reference for later
      self.card_display_label = label
      
    # Generic error report
    except tk.TclError as err:
    
      print("oops: " + str(err))
      
      
  def clear_card_display(self):
  
    self.card_display_label.destroy()
      
      
      
  def bind_widget_mouseover(self, widget, card):
  
    widget.bind("<Enter>", lambda e, card=card: self.set_card_display(card))
    widget.bind("<Leave>", lambda e : self.clear_card_display())
  

def get_image_scaled_height():

  return int(CARD_HEIGHT * CARD_SCALE)
  
  
def get_image_scaled_width():

  return int(CARD_WIDTH * CARD_SCALE)
  
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
  
  draft_window = DraftWindow(master=root, draft=draft)
  draft_window.mainloop()
  
  
  
if __name__ == "__main__":

  main()