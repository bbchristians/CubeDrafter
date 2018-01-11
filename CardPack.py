import mtgsdk as mtg;
import random;

class CardPack():

  cards = []

  def __init__(self, cards):
  
    self.cards = cards
    
  
  def pick_card(self, card):
  
    self.cards.remove(card)
    
    
  # Static method
  def create_packs(card_pool, no_packs=3, no_common=10, no_uncommon=3, no_rare=1):
  
    """
    args:
      card_pool: A list of Cards
      no_opacks: The number of packs to generate
      no_common: The number of common cards to put in the pack
      no_uncommon: The number of uncommon cards to put in the pack
      no_rare: The number of (Mythic) rares to put into the pack
    return:
      A list of CardPack objects
    """
  
    pack_size = no_common + no_uncommon + no_rare
    # Split the pool by rarity
    commons = []
    uncommons = []
    rares = [] #Rares AND mythics
    
    for card in card_pool:
    
      if card.rarity == "Common":
      
        commons += [card]
        
      elif card.rarity == "Uncommon":
      
        uncommons += [card]
        
      else:
      
        rares += [card]
        
        
    # assure there are enough cards for the packs
    if no_common * no_packs > len(commons):
    
      print("Not enough commons for the requested amount. Required: {}, Found: {}".format(no_common * no_packs, len(commons)))
      return
      
    if no_uncommon * no_packs > len(uncommons):
    
      print("Not enough uncommons for the requested amount. Required: {}, Found: {}".format(no_uncommon * no_packs, len(uncommons)))
      return
      
    if no_rare * no_packs > len(rares):
    
      print("Not enough rares for the requested amount. Required: {}, Found: {}".format(no_rare * no_packs, len(rares)))
      return
        
    # Shuffle rarity stacks and distribute cards from them
    ret_packs = [] # return array of packs
    
    random.shuffle(commons)
    random.shuffle(uncommons)
    random.shuffle(rares)
    
    for i in range(0,no_packs):
    
      pack = []
      
      for r in range(0, no_rare):
      
        pack += [rares.pop(0)]
        
      for u in range(0, no_uncommon):
      
        pack += [uncommons.pop(0)]
    
      for c in range(0, no_common):
      
        pack += [commons.pop(0)]
        
        
      ret_packs += [CardPack(pack)]
        
    return ret_packs