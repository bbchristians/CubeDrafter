from CardPack import CardPack;
from CardLoader import CardLoader;
from WebCardLoader import WebCardLoader;
from LocalCardLoader import LocalCardLoader;
from CardPack import CardPack;
from Draft import Draft;
from HumanDrafter import HumanDrafter;
from AIDrafter import AIDrafter;

  
def do_draft(pool):

  # Make Packs
  packs = CardPack.create_packs(pool, no_packs=24, no_rare=2, no_uncommon=4, no_common=9)

  draft = Draft()

  player = HumanDrafter("me", [packs.pop()]*3, draft)
  
  draft.add_human_drafter(player)
  
  for i in range(7):
  
    ai = AIDrafter("AI{}".format(i), [packs.pop()]*3)
    draft.add_ai_drafter(ai)
    
  draft.start_draft()
    

def main():

  
  c_import = LocalCardLoader("SampleCube.csv")
  pool = c_import.get_cards("cube1")
  
  #c_import = WebCardLoader("SampleCube.csv") 
  #c_import = WebCardLoader("sample.csv")
  #pool = c_import.get_cards()
  
  
  #c_import.save_cards("cube1", pool)
  #c_import.save_cards("test", pool)
  
  print("Loaded {} card(s)".format(len(pool)))
  
  do_draft(pool)
    
  """
  packs = CardPack.create_packs(pool, no_rare=2, no_uncommon=4, no_common=9)
  
  n = 1
  
  for pack in packs:
  
    print("\nPack {}:".format(n))
    n += 1
  
    for card in pack.cards:
    
      print("{} : {}".format(card.name, card.rarity))
  """
 
 
  
if __name__ == "__main__":

  main()