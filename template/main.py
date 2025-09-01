from alethiometer.instrument import Alethiometer, InstrumentError


def main():
    print("----------------- R1 -----------------")
    al = Alethiometer()

    al.add_symbol("Ant")
    print(len(al))                          # 1
    print(al.get_next_symbol("Ant", 3))     # Ant

    al.add_symbol("Crocodile", "Ant")
    al.add_symbol("Bird", "Ant")
    print(len(al))                              # 3
    print(al.get_next_symbol("Bird", 2))        # Ant  
    print(al.get_next_symbol("Ant", 4))         # Bird
    print(al.get_next_symbol("Crocodile", 3))   # Crocodile      

    try:
        al.add_symbol("Owl", "Horse")
        print("[Error] Missing previous symbol not detected")
    except InstrumentError:
        print("Missing previous symbol correctly identified")  # Missing previous symbol correctly identified

    print("----------------- R2 -----------------")
    print(al.add_concepts("in direzione", "in pericolo", "partire per", "stella polare"))   # 4
    print(al.add_concepts("stella polare", "un viaggio", "amici"))                          # 2    

    al.chain_concepts("partire per", "un viaggio", "in direzione")
    al.chain_concepts("partire per", "un viaggio", "amici")
    
    al.chain_concepts("un viaggio", "in direzione")
    al.chain_concepts("in direzione", "stella polare")
    al.chain_concepts("amici", "in pericolo")  

    print(al.get_next_concepts("partire per"))      # {'amici', 'un viaggio', 'in direzione'}
    print(al.get_next_concepts("un viaggio"))       # {'in direzione'}
    print(al.get_next_concepts("in direzione"))     # {'stella polare'}
    print(al.get_next_concepts("amici"))            # {'in pericolo'}

    print(al.get_previous_concepts("un viaggio"))       # {'partire per'}
    print(al.get_previous_concepts("in direzione"))     # {'partire per', 'un viaggio'}
    print(al.get_previous_concepts("amici"))            # {'partire per'}
    print(al.get_previous_concepts("stella polare"))    # {'in direzione'}
    print(al.get_previous_concepts("in pericolo"))      # {'amici'}

    print("----------------- R3 -----------------")
    al.link_symbol_to_concept("Ant", "in direzione")
    al.link_symbol_to_concept("Ant", "in pericolo")
    al.link_symbol_to_concept("Ant", "stella polare")

    al.link_symbol_to_concept("Bird", "partire per")
    al.link_symbol_to_concept("Bird", "stella polare")

    al.link_symbol_to_concept("Crocodile", "un viaggio")
    al.link_symbol_to_concept("Crocodile", "amici")
    al.link_symbol_to_concept("Crocodile", "un viaggio")

    print(al.get_concepts_of_symbol("Ant"))     # {'in pericolo', 'stella polare', 'in direzione'}
    print(al.get_concepts_of_symbol("Bird", lambda x: "o" in x))                 # {'stella polare'}
    print(al.get_concepts_of_symbol("Crocodile", lambda x: len(x.split()) > 1))  # {'un viaggio'}

    print(al.get_symbols_of_concept("stella polare"))  # [('Ant', 3), ('Bird', 2)]

    print("----------------- R4 -----------------")
    print(al.translation(["Bird", "Crocodile", "Ant", "Bird"]))   # partire per un viaggio in direzione stella polare
    print(al.translation(["Crocodile"]))                          # un viaggio (o amici)
    print(al.translation(["Ant", "Bird", "Crocodile"]))           # None


if __name__ == "__main__":
    main()
