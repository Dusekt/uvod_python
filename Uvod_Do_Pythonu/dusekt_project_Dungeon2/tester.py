from dungeon_items import *
import inspect
from dusekt_Dungeon import Dungeon

item = ["vvv","vvv","vvv"]
item2 = ["ada","awda","awd"]

Dungeon = Dungeon(size=(40, 10),
                                       tunnel_number=40,
                                       hero_name="wad",
                                       file_load=False)

for j,i in enumerate(item):
    print(i, end="")
    print(f"  {item2[j]}")

Dungeon.set_HUD()
#print(list(Dungeon.HUD.items())[1])
#print(list(filter(lambda x: x[1] == Dungeon.hero.position[1],Dungeon.empty_space)))
#print(list(filter(lambda x: x[0] == Dungeon.hero.position[0],Dungeon.empty_space)))
#print(Dungeon.find_shortest_path(Dungeon.hero.position,Dungeon.beholder.position))
#print(Dungeon)
Dungeon.update_map()
#print(Dungeon.beholder.position)
#print(Dungeon.find_level2(Dungeon.beholder.position,Dungeon.hero.position))

list=["a","b","c"]
list.remove("a")
print(list)
print(0//3)