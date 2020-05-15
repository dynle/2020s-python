
users = {
    "Alice" : {'Frozen' : 3, 'Parasite' : 2, 'Beautiful Mind' : 0, 'Creed' : 5, 'Zorro' : 0},
    "Bob" : {'Frozen' : 2, 'Parasite' : 0, 'Beautiful Mind' : 4, 'Creed' : 4, 'Zorro' : 5},
    "Charlie" : {'Frozen' : 0, 'Parasite' : 4, 'Beautiful Mind' : 5, 'Creed' : 2, 'Zorro' : 3},
    "Dave" : {'Frozen' : 2, 'Parasite' : 5, 'Beautiful Mind' : 3, 'Creed' : 0, 'Zorro' : 4},
    "Eve" : {'Frozen' : 4, 'Parasite' : 5, 'Beautiful Mind' : 0, 'Creed' : 4, 'Zorro' : 5},
    "Frank" : {'Frozen' : 5, 'Parasite' : 0, 'Beautiful Mind' : 3, 'Creed' : 4, 'Zorro' : 2},
    "Geoffrey" : {'Frozen' : 0, 'Parasite' : 3, 'Beautiful Mind' : 3, 'Creed' : 5, 'Zorro' : 0},
    "Ivan" : {'Frozen' : 5, 'Parasite' : 5, 'Beautiful Mind' : 5, 'Creed' : 0, 'Zorro' : 2}
}

# print(list(users["Alice"].values()))
a = list(users["{}".format("Alice")].values())
print(a)