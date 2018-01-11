from Drafter import Drafter;


class HumanDrafter(Drafter):

  draft = None

  def __init__(self, name, packs, draft):
  
    super().__init__(name, packs)
    self.draft = draft
    
  def make_pick(self):
  
    print("\nPicks:\n--------")
    
    no = 0
    
    for card in self.current_pack:
      
      print("{}: {}({})".format(no, card.name, card.rarity[0]))
      no += 1
      
    selection = input("Draft Pick: ")
    pick = self.current_pack[int(selection)]
    
    del self.current_pack[int(selection)]
    
    self.draft.human_makes_pick()
    
    