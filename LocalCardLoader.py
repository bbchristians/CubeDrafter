import sys;
import mtgsdk as mtg;
import csv;
from CardLoader import CardLoader;
import CardLoader as cl_mod;

CARD_NO_MULT = 5

class LocalCardLoader(CardLoader):

  def __init__(self, filename):
  
    super().__init__(filename)
    
  def get_cards(self, save_file):
  
    """
    Return:
      A list of Cards
    """
    cards = []
    
    with open(cl_mod.SAVE_DATA_DIR + save_file + cl_mod.SAVE_DATA_EXT) as save_file:
    
      reader = csv.reader(save_file, quotechar='$')
      
      for line in reader:
      
        name = line[0]
        count = int(line[1])
        rarity = line[2]
        image_url = line[3]
        
        card_response_dict = {'name': name, 'rarity': rarity, 'imageUrl': image_url}
        cards += [mtg.Card(card_response_dict)] * count * CARD_NO_MULT
  
    return cards
        