import mtgsdk as mtg;
from CardPack import CardPack;
from Drafter import Drafter;


class Draft:

  drafters = []
  human_drafter = None
  gui = None

  def __init__(self):
  
    pass
    
  def add_ai_drafter(self, drafter):
  
    self.drafters += [drafter]
    
  def add_human_drafter(self, drafter):
  
    self.drafters += [drafter]
    self.human_drafter = drafter
    
  
  def start_draft(self):
  
    self.crack_packs()
    
    
  def ready_picks(self):
  
    self.ai_draft_packs()
    
    if self.gui is None:
    
      self.human_drafter.make_pick()
      
      
  def crack_packs(self):
  
    if len(self.human_drafter.packs) <= 0 :
    
      print("Draft Concluded")
      return
  
    print("Drafters opened packs!")
    for drafter in self.drafters:
      
      drafter.open_pack()
      
    self.alert_gui()
    self.ready_picks()
      
        
  def human_makes_pick(self):
  
    if len(self.human_drafter.current_pack) == 0:
    
      self.crack_packs()
      
    else:
    
      self.pass_all_packs()
      self.ready_picks()
      
      
      
  def ai_draft_packs(self):
  
    for drafter in self.drafters:
    
      if len(drafter.current_pack) <= 0:
      
        print("Drafter {} was told to draft an empty pack!".format(drafter.name))
    
      if drafter == self.human_drafter:
      
        continue
        
      drafter.make_pick()
      
        
        
  def pass_all_packs(self):

    new_pack_order = []
    
    new_pack_order += [self.drafters[len(self.drafters)-1].current_pack]
    
    for drafter in self.drafters:
      
      new_pack_order += [drafter.current_pack]
      
      
    for i in range(len(self.drafters)):
    
      try:
      
        self.drafters[i].get_pack(new_pack_order[i])
        
      except IndexError:
      
        print("Pack/Drafter number mismatch. No Drafters: {}, No Packs:{}".format(len(self.drafters), len(new_pack_order)))
     
    self.alert_gui()
        
  def get_players_pack(self):
  
    return self.human_drafter.current_pack
    
    
  def make_player_pick(self, index):
  
    self.human_drafter.confirm_pick(index)
    
  def add_gui(self, gui):
  
    self.gui = gui
    
    
  def alert_gui(self):
  
    if self.gui is not None:
  
      self.gui.render_humans_pack()
       
       
       
       
       