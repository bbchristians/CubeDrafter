import sys;
import mtgsdk as mtg;
from CardLoader import CardLoader;

class WebCardLoader(CardLoader):

  cards = {}
  rarity_dict = {}
  image_dict = {}

  def __init__(self, filename):
  
    super().__init__(filename)
    
    
  def make_queries(self):
  
    """
    Return:
      A list of tuples in the form:
        (card_name, [Card,[Card]*], int(count))
                        ^ Variance of cards with the same name
    
    """
    ret = []
    
    cards_read = 0;
    
    for card_name in self.cards:
      
      qb = mtg.querybuilder.QueryBuilder(mtg.Card)
      qb.where(name=card_name, rarity=self.rarity_dict[card_name])
      ret.append((card_name, qb.all(), self.cards[card_name]))
      
      cards_read += 1
      perc_done = cards_read / len(self.cards) * 100
      print("\r|{}{}|{}%".format('█'*int(perc_done/10), ' '*int(10 - (perc_done/10)), int(perc_done)), end='\r')
      
    return ret;
    
    
  def get_cards(self):
  
    """
    Return:
      A list of Cards
    """
    card_pool = []
    
    queries = self.make_queries()
    
    for query in queries:
    
      if len(query[1]) <= 0:
      
        print("Card not found: {} @ {}".format(query[0], self.rarity_dict[query[0]]))
        continue
    
      for card in query[1]:
      
        if card.name == query[0]:
        
          card_pool += [card]*query[2]
          self.image_dict[card.name] = card.image_url
          
          break
      
    return card_pool
    
    
if __name__ == "__main__":

  loader = WebCardLoader("SampleCube.csv")
  cards = loader.get_cards()
  loader.save_cards("cube1", cards)
  
  