'''
Run this script and continue with the interactive shell.
---
Movie list and users' ratings.
not rated = 0
max rating = 5
'''

#Modify into dictionaries
movies = ['Frozen', 'Parasite', 'Beautiful Mind', 'Creed', 'Zorro']

users = {
    "Alice" : [3, 2, 0, 5, 0], #Modify the values into dictionaries
    "Bob" : [2, 0, 4, 4, 5],
    "Charlie" : [0, 4, 5, 2, 3],
    "Dave" : [2, 5, 3, 0, 4],
    "Eve" : [4, 5, 0, 4, 5],
    "Frank" : [5, 0, 3, 4, 2],
    "Geoffrey" : [0, 3, 3, 5, 0],
    "Ivan" : [5, 5, 5, 0, 2]
}

def get_distance(user1, user2):
    '''Return the distance between two users based on their movie ratings'''

    common_ratings = 0
    distance = 0
    for i in range(len(user1)):
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
    #index of the movie in movies list
    idx = movies.index(movie)
    #save ratings of the user before being deleted
    user_all = user_ratings[user]
    #save rating of the movie before being deleted
    user_rating = user_ratings[user][idx]

    del user_ratings[user]

    #Find distances from the specific movie
    li_movie_distance=[]
    for key in user_ratings:
        if user_ratings[key][idx]:
            distance = 0
            distance += abs(user_ratings[key][idx] - user_rating)
            li_movie_distance.append(distance)
        else:
            li_movie_distance.append(0)
    

    #Find indicees of min distance in li_movie_distance
    #Get an index without 0 rating
    li_index_min_distance = [i for i, x in enumerate(li_movie_distance)
                            if x == min(i for i in li_movie_distance 
                            if i > 0)]

    #calculate common_ratings and distance from other users
    li_common_ratings_distance = []
    for key in user_ratings:
        common_ratings = 0
        distance = 0
        for i in range(len(user_ratings[key])):
            if user_all[i] and user_ratings[key][i]:
                distance += abs(user_all[i] - users[key][i])
                common_ratings += 1
        li_common_ratings_distance.append((common_ratings, distance))

    #Find nearest user by index
    li_cr_d_min = []
    for y in li_index_min_distance:
        li_cr_d_min.append((y,li_common_ratings_distance[y]))
    if li_cr_d_min.count(min(li_cr_d_min,key=lambda x: x[1][1])) == 1:
        '''if there is one and only least distance'''
        nearest_user_index = min(li_cr_d_min,key=lambda x: x[1][1])[0]
        nearest_user = list(user_ratings)[nearest_user_index]
    else:
        '''if there is a tie of min distance'''
        li_cr_d_min2=[]
        for i in li_cr_d_min:
            if i[1][1] == min(li_cr_d_min,key=lambda x: x[1][1]):
                li_cr_d_min2.append(i)
        nearest_user_index = max(li_cr_d_min,key=lambda x: x[1][0])[0]
        nearest_user = list(user_ratings)[nearest_user_index]
    return nearest_user
# print(get_nearest_user('Beautiful Mind',"Eve",users))



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
    idx = movies.index(movie)
    nearest_user = get_nearest_user(movie,user,user_ratings)
    rating = user_ratings[nearest_user][idx]
    if rating >= 3:
        recommend = True
    else:
        recommend = False
    return recommend
print(get_recommendation("Beautiful Mind","Eve",users))

'''
For homework, you have to modify the data structures
of movies and users into dictionaries.

In the real world, users rarely rate movies they have watched,
hence the movie-user matrix will be sparse (many empty entries)
'''