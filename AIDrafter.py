from Drafter import Drafter;
import random;


class AIDrafter(Drafter):

  def __init__(self, name, packs):
  
    super().__init__(name, packs)
    
  def make_pick(self):
  
    # TODO Make Machines Learn
    pick_indexes = list(range(0,min(len(self.current_pack), 8))) + [0,0,0,1,1,1]
    pick_index = random.choice(pick_indexes)
    pick = self.current_pack[pick_index]
    del self.current_pack[pick_index]
    
    self.picks += [pick]
    