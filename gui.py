import tkinter as tk;
import sys;
import mtgsdk as mtg;
import base64;
from LocalCardLoader import LocalCardLoader;
import urllib.request;
from PIL import Image, ImageTk;
import random;

IMAGE_DIR = "Images/"
IMAGE_EXT = ".png"

class Application(tk.Frame):
  def __init__(self, master=None, cards=None):
    super().__init__(master)
    self.pack()
    self.create_widgets(cards)

  def create_widgets(self, cards):
  
    r = 0
    c = 0
    random.shuffle(cards)
    
    for card in cards:
    
      print("{}{}".format(r,c))
      print(card.image_url)
    
      if r >= 3:
      
        break
    
      try:
        b=tk.Button(self,justify = tk.LEFT)
        
        photo = None
        mvid = extract_multiverseid(card.image_url)
        image_path = IMAGE_DIR + mvid + IMAGE_EXT
        
        try:
        
          image = Image.open(image_path)
          
        except FileNotFoundError:
        
          urllib.request.urlretrieve(card.image_url, image_path)
          image = Image.open(image_path)

        #image_byt = urlopen(card.image_url).read()
        # TODO Cache and load
        #image_b64 = base64.encodestring(image_byt)
        #print(image_b64)
        photo = ImageTk.PhotoImage(image)
        
        b.config(image=photo,width="223",height="311")
        #b.pack(side=tk.LEFT, padx=5, pady=5)
        b.image = photo
        b.grid(row=r, column=c)
        
        c += 1
        
        if c >= 5:
        
          r += 1
          c = 0
          
      except tk.TclError as err:
      
        print("oops: " + str(err))

    #self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
    #self.quit.pack(side="bottom")

    
def extract_multiverseid(url):

  return (((url.split("multiverseid="))[1]).split("&type=card"))[0]
  

def main():

  
  c_import = LocalCardLoader("SampleCube.csv")
  pool = c_import.get_cards("cube1")
  
  root = tk.Tk()
  app = Application(master=root, cards=pool)
  app.mainloop()
  
  
  
if __name__ == "__main__":

  main()