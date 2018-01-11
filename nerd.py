import sys;
import mtgsdk as mtg;
import csv;
from CardPack import CardPack;
from CardLoader import CardLoader;
from WebCardLoader import WebCardLoader;
from LocalCardLoader import LocalCardLoader;

  
    
    

def main():

  
  c_import = LocalCardLoader("SampleCube.csv")
  pool = c_import.get_cards("cube1")
  
  #c_import = WebCardLoader("SampleCube.csv") 
  #c_import = WebCardLoader("sample.csv")
  #pool = c_import.get_cards()
  
  
  #c_import.save_cards("cube1", pool)
  #c_import.save_cards("test", pool)
  
  for card in pool:
  
    print(card.name)
    
    
  
  
  
  
if __name__ == "__main__":

  main()