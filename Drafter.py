import mtgsdk as mtg;
from CardPack import CardPack;

class Drafter:

  name = "anonymous"
  packs = []
  current_pack = [] # Array of cards
  picks = []

  def __init__(self, name, packs):
  
    self.name = name
    self.packs = packs
    
    
  def open_pack(self):
    
    """
    Opens the first pack in the Drafter's pack list
    
    """
    if len(self.current_pack) > 0:
    
      print("Drafter {} opened a pack before they finished their old pack!".format(self.name))
    
    opened_pack = self.packs.pop()
    self.current_pack = opened_pack.cards
    print(self.current_pack)
    
    
  def pass_pack(self):
  
    passed_pack = self.opened_pack
    self.opened_pack = []
    return passed_pack
    
  def get_pack(self, pack):
  
    self.current_pack = pack
    
    
  def make_pick(self):
  
    return;