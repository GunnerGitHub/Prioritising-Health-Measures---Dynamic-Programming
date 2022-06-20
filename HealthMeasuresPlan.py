from itertools import combinations

Z = range(9)

# The state is a 9-tuple where each element is
# -1 = outbreak, 0 = normal, 1 = protected
# NextStates returns a list of tuples with a probability
# in position 0 and a state as a tuple in position 1
def NextStates(State, OutbreakProb):
    ans = []
    # Z0 are the normal zones
    Z0 = [j for j in Z if State[j]==0]
    n = len(Z0)
    for i in range(n+1):
        for tlist in combinations(Z0, i):
            p = 1.0
            slist = list(State)
            for j in range(n):
                if Z0[j] in tlist:
                    p *= OutbreakProb[Z0[j]]
                    slist[Z0[j]] = -1
                else:
                    p *= 1-OutbreakProb[Z0[j]]
            ans.append((p, tuple(slist)))
    return ans

# example
# zones 0, 6, 7 have been protected
# zones 3, 4, 8 have outbreaks
# zones 1, 2, 5 are normal (so there will be 2**3 = 8 possible next states)
#states = NextStates((1,0,0,-1,-1,0,1,1,-1), [0.2 for j in Z])

Facilities = [
    'Government Office',
    'Convenience Store',
    'Ambulance',
    'Hospital',
    'Library',
    'Post Office',
    'Town Hall',
    'Medical Centre',
    'Police Station',
    'Supermarket',
    'Fire Station',
    'Hotel',
    'School',
    'Bus Depot',
    'Wedding Chapel',
    'Bank'
]

Zones = [
    [1,2,6],
    [9,11,15],
    [0,11],
    [7,8,13,14],
    [4,5],
    [12],
    [0,8,10,11,15],
    [4],
    [3,5,8]
]

plans =[6, 3, 8, 1, 0, 4, 2, 7, 5]

prioritised = [2,3,6,9]
#Maximizing Probability of prioritised zones being accessable (Communication 15)
""" The following is the value fuction to determine the maximum proability that 
the 4 priorities facilties are accessable at the end. It takes input (the current state)
 and returns the maximum probability the prioritised facilties are acessbable, as well
 as the action to take (which zone to target health measures) in tuple (prob,action).
 Please run V((0,0,0,0,0,0,0,0,0)) in console for Communcation 15"""
_V = {}
def V(s):
    if 0 not in s:
        return (essential(s),"Done")
    else:
        if s not in _V:
            max_exp = (0,'None')
            for a in plans:
                if s[a]==0:
                    t = s
                    lst = list(t)
                    lst[a] = 1
                    st = tuple(lst)
                    Possible = NextStates(st,probst(st))
                    y = (sum(prob*V(state)[0] for prob,state in Possible),a)
                    if y[0]>max_exp[0]:
                        max_exp = y
            _V[s] = max_exp
        return _V[s]


#Maximizing expected distinct facilties (COMMUNICATION 14 and 13)
""" The following is the value fuction to determine the maximum expected distinct faciltiy 
at the end of the operation. It takes input (the current state) and returns the 
maximum expected distinct faciltiy, as well as the action to take 
(which zone to target health measures next) in tuple (max expected,action).
Please run V1((0,0,0,0,0,0,0,0,0)) in console for Communcation 14"""
_V1 = {}
def V1(s):
    if 0 not in s:
        return (distinct(s),"Done")
    else:
        if s not in _V1:
            max_exp = (0,'None')
            for a in plans:
                if s[a]==0:
                    t = s
                    lst = list(t)
                    lst[a] = 1
                    st = tuple(lst)
                    Possible = NextStates(st,probst(st))
                    y = (sum(prob*V1(state)[0] for prob,state in Possible),a)
                    if y>max_exp:
                        max_exp = y
            _V1[s] = max_exp
        return _V1[s]

""" The following is the value fuction to determine the maximum expected distinct faciltiy 
at the end of the operation (Com13). It takes input (the current state) and returns the 
maximum expected distinct faciltiy, as well as the action to take 
(which zone to target health measures next) in tuple (max expected,action).
Please run V2((0,0,0,0,0,0,0,0,0)) in console for Communcation 13"""
_V2 = {}
def V2(s):
    if 0 not in s:
        return (distinct(s),"Done")
    else:
        if s not in _V2:
            max_exp = (0,'None')
            for a in plans:
                if s[a]==0:
                    t = s
                    lst = list(t)
                    lst[a] = 1
                    st = tuple(lst)
                    Possible = NextStates(st,[0.2 for i in Z])
                    y = (sum(prob*V2(state)[0] for prob,state in Possible),a)
                    if y>max_exp:
                        max_exp = y
            _V2[s] = max_exp
        return _V2[s]


#Finds the distinct number of facilities for a given state (Comm14)
""" This function is used in Communication 14 to get the number of dinsitct facilities
by inputting a state (tuple). It returns the number of dinsitct facilities"""
def distinct(ending_state):
    maybe={0:0,1:0,2:0,3:0,4:0,5:0,6:0,7:0,8:0,
           9:0,10:0,11:0,12:0,13:0,14:0,15:0}
    for a in Z:
        rn=Zones[a]
        if ending_state[a]==1: #or ending_state[a]==0:
            for n in rn:
                maybe[n]+=1
    distinct_facility=0
    for a in range(len(maybe)):
        if maybe[a]>0.1:
            distinct_facility+=1
    return distinct_facility

#determine if the 4 prioritised facilties are accessable (Communcation 15)
""" This function is used in Communication 15. It inputs a state (tuple) and
returns 1 if he 4 prioritised facilties are accessable (So ZONES 0,1,3 are accessable)
in the given state, and 0 if not"""
def essential(ending_state):
    if ending_state[0]==1 and ending_state[1]==1 and ending_state[8]==1:
        return 1
    else:
        return 0
#the next one generalises the above function
"""This is a substitute for the above function, just more generalised."""
def essential2(ending_state):
    access = {3:0, 6:0, 2:0, 9:0}
    n=0
    for a in ending_state:
        if a == 1:
            for fac in Zones[n]:
                if fac in access:
                    access[fac]=1 
        n+=1    
    if sum(access.values())==4:
        return 1
    else:
        return 0
    
# Changes probability depending on neighbours outbreaks
""" This function inputs the current state (tuple) and updates the probbiility
of each zone having an outbreak the next week depending on its neighbours. The 
data for this was examined through the image provided. It returns a list of the
new probabilties"""
def probst(state):
    zone_prob = [0.2 for j in Z]
    if state[0]==-1:
        zone_prob[1]+=0.05
        zone_prob[4]+=0.05
    if state[1]==-1:
        zone_prob[0]+=0.05
        zone_prob[2]+=0.05
        zone_prob[5]+=0.05
    if state[2]==-1:
        zone_prob[1]+=0.05
        zone_prob[3]+=0.05
        zone_prob[6]+=0.05
    if state[3]==-1:
        zone_prob[2]+=0.05
        zone_prob[7]+=0.05
    if state[4]==-1:
        zone_prob[0]+=0.05
        zone_prob[5]+=0.05
    if state[5]==-1:
        zone_prob[1]+=0.05
        zone_prob[4]+=0.05
        zone_prob[6]+=0.05
    if state[6]==-1:
        zone_prob[2]+=0.05
        zone_prob[5]+=0.05
        zone_prob[7]+=0.05
        zone_prob[8]+=0.05
    if state[7]==-1:
        zone_prob[3]+=0.05
        zone_prob[6]+=0.05
    if state[8]==-1:
        zone_prob[6]+=0.05
    
    return zone_prob


#The next two functions gives reuslt for COMMUNICATION 14
""" This function inputs a state then returns the most frequent action (ZONE for helath 
measures from the value function across all possible next states."""
def nextoption1(state):
    s=state
    actions = []
    Possible = NextStates(s,[0.2 for j in Z])
    for pro,sta in Possible:
        act = V1(sta)[1]
        if act in (0,1,2,3,4,5,6,7,8):
            actions.append(act) 
    List=actions
    return max(set(List), key = List.count)

strat1 =[] #the startegy proposed for communication 14
""" This function inputs a state. It first updates strat1 for the first action if not done 
already, then looks at nextoption1 and adds the action recommended by that, 
then running for the state with the action now being 1 until 9 actions found"""
def strategy1(state):
    if 1 not in state:
        first = V1((0,0,0,0,0,0,0,0,0))
        print("Maximum expected distinct facilties are",first[0], "facilities.")
        print("The first zone to target health measures is ZONE", first[1], "for maximum expected distinct facilties.")
        strat1.append(first[1])
        t = state
        lst = list(t)
        lst[first[1]] = 1
        state = tuple(lst)     
    a=nextoption1(state)
    strat1.append(a)
    t = state
    lst = list(t)
    lst[a] = 1
    st = tuple(lst)
    if 0 not in st:
        print("The proposed strategy is", strat1)
    else:
        strategy1(st)


#The next two function give result for COMMUNICATION15 using value function
""" This function inputs a state then returns the most frequent action (ZONE for helath 
measures from the value function across all possible next states. Note, it only looks
at possibel next states where the critical zones are still open"""
def nextoption(state):
    s=state
    actions = []
    Possible = NextStates(s,[0.2 for j in Z])
    for pro,sta in Possible:
        act = V(sta)[1]
        if act in (0,1,8):
            actions.append(act) 
    List=actions
    return max(set(List), key = List.count)

strat=[] #the strategy for communication 15
""" This function inputs a state. It first updates strat1 for the first action if not done 
already, then looks at nextoption1 and adds the action recommended by that, 
then running for the state with the action now being 1 until the first 3 actions are found
corresponding to the 3 zones needing to be accesable for the 4 prioritised facilties"""
def strategy(state):
    if 1 not in state:
        first = V((0,0,0,0,0,0,0,0,0))
        print("Maximum probability of the prioritised facilities being accesable at the end:",first[0])
        print("The first zone to target health measures is ZONE", first[1], 'for maximum probability of the prioritised facilities being accesable at the end.')
        strat.append(first[1])
        t = state
        lst = list(t)
        lst[first[1]] = 1
        state = tuple(lst)     
    a=nextoption(state)
    strat.append(a)
    t = state
    lst = list(t)
    lst[a] = 1
    st = tuple(lst)
    if 0 not in (st[0],st[1],st[8]):
        print("The proposed strategy (for prioritised facilties) is", strat)
        print("The order of the rest of zones is not needed as they do not contain prioritied facilties.")
    else:
        strategy(st)

print("COMMUNICATION 14 ANSWER")
strategy1((0,0,0,0,0,0,0,0,0))
print("COMMUNICATION 15 ANSWER")
strategy((0,0,0,0,0,0,0,0,0))

strat=[]
strat1=[]

print("Three value functions are provided V (Comm15),V1 (Comm14),V2 (Comm13) which take the initial input of (0,0,0,0,0,0,0,0,0), and give the optimal value and actions in tuple (optimal value, action).")



