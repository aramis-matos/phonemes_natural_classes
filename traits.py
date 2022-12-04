import pandas as pd
import functools as ft
import itertools as it

vowels = pd.read_csv("vowels.csv", index_col="SOUND")
consonants = pd.read_csv("consonants.csv", index_col="SOUND")

# x = consonants[consonants.SONORANT == "-"]

# print(x[x.LABIAL == "+"])


def all_equal(tps):
    vals = list(tps)[1:]
    return ft.reduce(lambda a, b: a and (b == vals[0]), vals)


def get_intersection(traits, sounds):
    return [(val[1], val[0]) for val in zip(traits, *sounds) if all_equal(val)]


def get_nat_class(intersection, traits):
    df = traits
    for tup in intersection:
        df = df[df[tup[1]] == tup[0]]
    return list(df.index)


def get_intersection_and_nat_class(traits, *elems):
    cols = list(traits.columns)
    sounds = [list(traits.loc[val]) for val in elems]
    proper_int = get_intersection(cols, sounds)
    nat_class = get_nat_class(proper_int, traits)
    # proper_int = [f"{val[0]}{val[1]}" for val in proper_int]
    return (proper_int, nat_class)


def get_minimized_intersection(traits, intr_and_nat_class):
    intr, nat_class = intr_and_nat_class[0], intr_and_nat_class[1]
    new_int = intr.copy()
    for val in intr:
        index = new_int.index(val)
        trait = new_int.pop(index)
        new_nat_class = get_nat_class(new_int, traits)
        if new_nat_class != nat_class:
            new_int.insert(index, trait)
    return new_int


def get_all_min_intersection(intr_and_nat_class, traits):
    perms = [list(x) for x in it.permutations(intr_and_nat_class[0])]
    perms = [get_minimized_intersection(
        traits, [x, intr_and_nat_class[1]]) for x in perms]
    for perm in perms:
        perm.sort(key=lambda a: a[1])
    perms = list(set(tuple(x) for x in perms))
    return perms


sounds = ["ʃ", "ʒ"]
intr = get_intersection_and_nat_class(consonants, *sounds)
min_intr = get_all_min_intersection(intr, consonants)
print(
    f"Sounds: {sounds}\nNatural Class Intentionally: {intr[0]}\nMinimized Intentional Natural Class(es):")
for x in min_intr:
    print(x)
print(f"Natural Class Extensionally: {intr[1]}")

# intr = [('-',"CORONAL"),("-","VOICED"),("-","STRIDENT")]
# print(get_nat_class(intr,consonants))
