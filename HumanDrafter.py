from Drafter import Drafter;


class HumanDrafter(Drafter):

  draft = None
  pool = []
  gui = False

  def __init__(self, name, packs, draft, gui=False):
  
    super().__init__(name, packs)
    self.draft = draft
    self.gui = gui
    
  def make_pick(self):
  
    print("\nPicks:\n--------")
    
    no = 0
    
    for card in self.current_pack:
      
      print("{}: {}({})".format(no, card.name, card.rarity[0]))
      no += 1
      
    if not self.gui:
      
      selection = input("Draft Pick: ")
      self.confirm_pick(int(selection))
    
  def confirm_pick(self, index):
  
    self.pool += [self.current_pack[index]]
    
    print("Human Picked Card: {}".format(self.current_pack[index].name))
    
    del self.current_pack[int(index)]
    
    self.draft.human_makes_pick()