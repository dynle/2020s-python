'''
Run this script and continue with the interactive shell.
---
Movie list and users' ratings.
not rated = 0
max rating = 5

            Frozen  Parasite    Pikachu Creed   Zorro
Alice       3       2                   5        
Bob         2                   4       4       5
Charlie             4           5       2       3
Dave        2       5           3       2       3
Eve         4       5                   4       5
Frank       5                   3       4       2
Geoffrey            3           3       5        
Ivan        5       5           5               2

'''

movies = ['Frozen', 'Parasite', 'Pikachu', 'Creed', 'Zorro']

users = {
    "Alice" : [3, 2, 0, 5, 0],
    "Bob" : [2, 0, 4, 4, 5],
    "Charlie" : [0, 4, 5, 2, 3],
    "Dave" : [2, 5, 3, 0, 4],
    "Eve" : [4, 5, 0, 4, 5],
    "Frank" : [5, 0, 3, 4, 2],
    "Geoffrey" : [0, 3, 3, 5, 0],
    "Ivan" : [5, 5, 5, 0, 2]
}

# Print users and ratings
# for user,movie in users.items():
#     print( '%s: %s' % ( user, ' '.join( map( str, movie ) ) ) )


# T1 Print the movie titles and ratings by each user
# Example: Alice: Frozen 3, Parasite 2, Creed 5
for key in users:
    print(key+": ",end="")
    for i in range(len(movies)):
        if i < 3:
            if users[key][i] == 0:
                continue
            print(movies[i],str(users[key][i])+",",end=" ")
        elif i == 3 and users[key][i+1] == 0:
            if users[key][i] == 0:
                continue
            else:
                print(movies[i],str(users[key][i])+"\n")
        elif i == 3 and users[key][i+1] != 0:
            if users[key][i] == 0:
                continue
            else:
                print(movies[i],str(users[key][i])+",",end=" ")
        else:
            if users[key][i] == 0:
                continue
            else:
                print(movies[i],str(users[key][i])+"\n")
            
                
             
        
            
                
                       
            


            



'''
D1 What do you think about the choice of these data types for a recommendation system?
D2 How to make them better? You should state your assumptions, too. 
'''