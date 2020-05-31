'''
Run this script and continue with the interactive shell.
---
Movie list and users' ratings.
not rated = 0
max rating = 5
'''
#change the data types of movies and users into dictionaries
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

"""answer"""
# movies = {
#     '101': 'Frozen', 
#     '202': 'Parasite', 
#     '333': 'Beautiful Mind', 
#     '444': 'Creed', 
#     '555': 'Zorro'
# }

# users = {
#     "Alice" : {'101': 3, '202': 2, '444': 5, }, # [3, 2, 0, 5, 0], #Modify the values into dictionaries
#     "Bob" : {'101': 2, '333': 4, '444': 4, '555': 5}, # [2, 0, 4, 4, 5],
#     "Charlie" : {'202': 4, '333': 5, '444': 2, '555': 4}, # [0, 4, 5, 2, 3],
#     "Dave" : {'101': 2, '202': 5, '333': 3 , '555': 5}, # [2, 5, 3, 0, 4],
#     "Eve" : {'101': 4, '202': 5, '444': 4, '555': 5}, # [4, 5, 0, 4, 5],
#     "Frank":  {'101': 5, '333': 3, '444': 4, '555': 2}, # [5, 0, 3, 4, 2],
#     "Geoffrey" : {'202': 3, '333': 3, '444': 5,}, # [0, 3, 3, 5, 0],
#     "Ivan" : {'101': 5, '202': 5, '333': 5, '555': 2}, # [5, 5, 5, 0, 2]
# }


def get_distance(user1, user2):
    '''Return the distance between two users based on their movie ratings'''

    common_ratings = 0
    distance = 0

    for i in user1.keys():
        if user1[i] and user2[i]:
            distance += abs(user1[i] - user2[i])
            common_ratings += 1

    return (common_ratings, distance)

def get_nearest_user(movie, user, user_ratings):
    '''
    Get the user with smallest distance to user for movie.

    -- Explanation
    Note: @ prefix means function arguments.

    @user_ratings is the dictionary like the one declared on line 12.
    Iterate over all users in the dictionary who have watched @movie
    to get the distance from the target @user,
    then return the nearest user.
    '''
    #index of the movie in the dictionaries
    idx = list(user_ratings[user].keys()).index(movie)
    #save ratings of the user before being deleted
    user_all = list(user_ratings[user].values())
    #save rating of the movie of the user before being deleted
    user_rating = user_all[idx]

    del user_ratings[user]


    #Find distances from the specific movie
    li_movie_distances=[]
    for key in user_ratings:
        if list(user_ratings[key].values())[idx]:
            distance = 0
            distance += abs(list(user_ratings[key].values())[idx] - user_rating)
            li_movie_distances.append(distance)
        else:
            li_movie_distances.append(0)
    

    #Find indices of min distance in li_movie_distances
    #Get indices without 0 rating
    li_index_min_distance = [i for i, x in enumerate(li_movie_distances)
                            if x == min(i for i in li_movie_distances 
                            if i > 0)]

    #Calculate common_ratings and distance from the other users
    li_common_ratings_distance = []
    for key in user_ratings:
        common_ratings = 0
        distance = 0
        for i in range(len(list(user_ratings[key].values()))):
            if user_all[i] and list(user_ratings[key].values())[i]:
                distance += abs(user_all[i] - list(user_ratings[key].values())[i])
                common_ratings += 1
        li_common_ratings_distance.append((common_ratings, distance))

    #Find nearest user by index
    li_min_d = []
    for y in li_index_min_distance:
        li_min_d.append((y,li_common_ratings_distance[y]))
    if li_min_d.count(min(li_min_d,key=lambda x: x[1][1])) == 1:
        '''if there is one and only least distance'''
        nearest_user_index = min(li_min_d,key=lambda x: x[1][1])[0]
        nearest_user = list(user_ratings)[nearest_user_index]
    else:
        '''if there is a tie of min distance, then take the max common ratings '''
        li_min_d_cr=[]
        for i in li_min_d:
            if i[1][1] == min(li_min_d,key=lambda x: x[1][1]):
                li_min_d_cr.append(i)
        nearest_user_index = max(li_min_d,key=lambda x: x[1][0])[0]
        nearest_user = list(user_ratings)[nearest_user_index]
    return nearest_user



def get_recommendation(movie, user, user_ratings):
    '''
    Get the recommendation for a movie.
    The return value is a boolean.

    -- Explanation
    Note: @ prefix means function arguments.

    Determine whether to recommend @movie or not 
    to @user based on the rating
    given by the nearest user returned by get_nearest_user()
    '''
    idx = list(user_ratings[user].keys()).index(movie)
    nearest_user = get_nearest_user(movie,user,user_ratings)
    rating = list(user_ratings[nearest_user].values())[idx]
    if rating >= 3:
        recommend = True
    else:
        recommend = False
    return recommend

'''
For homework, you have to modify the data structures
of movies and users into dictionaries.

In the real world, users rarely rate movies they have watched,
hence the movie-user matrix will be sparse (many empty entries)
'''

"""answer"""
# def get_distance(user1, user2):
#     '''Return the distance between two users based on their movie ratings'''

#     common_ratings = 0
#     distance = 0
#     for movie,rating in user1.items(): #range(len(user1)):
#         if user2.get(movie):
#             distance += abs(rating - user2[movie])
#             common_ratings += 1

#     return (common_ratings, distance)

# def get_nearest_user(movie, user, user_ratings):
#     '''
#     Get the user with smallest distance to user for movie.

#     -- Explanation
#     Note: @ prefix means function arguments.

#     @user_ratings is the dictionary like the one declared on line 12.
#     Iterate over all users in the dictionary who have watched @movie
#     to get the distance from the target @user,
#     then return the nearest user.
#     '''
#     nearest_user = None
#     nearest_distance = None

#     for o_user,o_ratings in user_ratings.items():
#         if o_user == user:
#             continue
#         if o_ratings.get(movie):
#             o_distance = get_distance(user_ratings[user], user_ratings[o_user])
#             if not o_distance[0]: # similar to o_distance[0] != 0
#                 continue
#             if not nearest_user:
#                 nearest_distance = o_distance
#                 nearest_user = o_user
#             else:
#                 if nearest_distance[1]/nearest_distance[0] > o_distance[1]/o_distance[0]:
#                     nearest_distance = o_distance
#                     nearest_user = o_user
#     return nearest_user

# def get_recommendation(movie, user, user_ratings):
#     '''
#     Get the recommendation for a movie.
#     The return value is a boolean.

#     -- Explanation
#     Note: @ prefix means function arguments.

#     Determine whether to recommend @movie or not 
#     to @user based on the rating
#     given by the nearest user returned by get_nearest_user()
#     '''
#     recommend = False
#     nearest_user = get_nearest_user(movie, user, user_ratings)
#     if nearest_user:
#         nearest_rating = user_ratings[nearest_user][movie]
#         if nearest_rating >= 4:
#             recommend = True
    
#     # T2 Complete the code in this function
#     return recommend