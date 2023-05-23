from dusekt_Dungeon import Dungeon
import pickle
dungeon = Dungeon = Dungeon(size=(40, 10),
                                       tunnel_number=40,
                                       hero_name="add",
                                       file_load=False)

with open(f"./Dungeon_saves/test1.dng", "wb") as f:

        pickle.dump(dungeon, f)
        f.close()

