import pandas as pd
import functools as ft

vowels = pd.read_csv("vowels.csv", index_col="SOUND")
consonants = pd.read_csv("consonants.csv", index_col="SOUND")

def all_equal(tps):
    vals = list(tps)[1:]
    return ft.reduce(lambda a,b: a and (b == vals[0]),vals)

def get_intersection_and_nat_class(traits,*elems):
    cols = list(traits.columns)
    sounds = [list(traits.loc[val]) for val in elems]
    proper_int = [(val[1],val[0]) for val in zip(cols,*sounds) if all_equal(val)]
    df = traits
    for tup in proper_int:
        df = df[df[tup[1]] == tup[0]]
    proper_int = [f"{val[0]}{val[1]}" for val in proper_int]
    return (proper_int,list(df.index))

sounds = ["s","z","ʃ","ʒ"]
val = get_intersection_and_nat_class(consonants,*sounds)
print(f"Sounds: {sounds}\nNatrual Class Intentionally: {val[0]}\nNatrual Class Extentionally: {val[1]}")

