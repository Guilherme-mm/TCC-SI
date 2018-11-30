from math import sqrt

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    
    if len(si)==0: return 0

    sum_of_squares=sum([pow(float(prefs[person1][item])-float(prefs[person2][item]),2)
                          for item in prefs[person1] if item in prefs[person2]])

    return 1/(1+sum_of_squares)

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(prefs,person,n=5,similarity=sim_distance):
    scores=[(similarity(prefs,person,other),other)
                       for other in prefs if other!=person]
    # Sort the list so the highest scores appear at the top scores.sort( )
    scores.reverse( )
    return scores[0:n]

# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_distance):
    totals={}
    simSums={}
    
    for other in prefs:
        # don't compare me to myself
        if other == person: continue
        
        sim = similarity(prefs,person,other)
        # ignore scores of zero or lower
        if sim<=0: continue
        
        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or float(prefs[person][item]) == 0:
                # Similarity * Score 
                totals.setdefault(item,0)
                totals[item] += float(prefs[other][item])*sim 
                # Sum of similarities 
                simSums.setdefault(item,0)
                simSums[item]+=sim

    # Create the normalized list
    rankings=[(total/simSums[item],item) for item,total in totals.items()]
    
    # Return the sorted list
    rankings.sort( )
    rankings.reverse( )
    return rankings