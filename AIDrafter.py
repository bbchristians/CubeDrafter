from Drafter import Drafter;
import random;

class AIDrafter(Drafter):

  def __init__(self, name, packs):
  
    super().__init__(name, packs)
    
  def make_pick(self):
  
    # TODO Make Machines Learn
    random.shuffle(self.current_pack)
    self.picks += [self.current_pack.pop()]