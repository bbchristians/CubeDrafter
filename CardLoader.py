import mtgsdk as mtg;
import csv;


SAVE_DATA_DIR = "Pools/"
SAVE_DATA_EXT = ".dat"

class CardLoader:

  def __init__(self, filename):
  
    self.cards = {}
    self.rarity_dict = {}
  
    with open(filename) as file:
    
      reader = csv.reader(file)
      
      for line in reader:
      
        self.cards[line[0]] = int(line[1])
        self.rarity_dict[line[0]] = line[2]
    

  def get_cards(self):
  
    cards = {}
    rarity_dict = {}
    image_dict = {}

  def save_cards(self, filename, cards):
  
    """
    Saves a pool of cards to the local files
    Saved Data is formatted as CSV in the format:
      "Name","Count","Rarity","Image_Url"
    
    Return: None
    """
    with open(SAVE_DATA_DIR + filename + SAVE_DATA_EXT, "w+", newline="\n") as save_file:
    
      writer = csv.writer(save_file, quotechar="$", quoting=csv.QUOTE_ALL)
      
      card_set = set(cards)
      
      for card in card_set:
      
        csv_line = [card.name, cards.count(card), card.rarity, card.image_url]
        
        writer.writerow(csv_line)
    
    
