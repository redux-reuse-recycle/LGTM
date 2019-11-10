# (row, col) format

UP = (1, 0)
RIGHT = (0, 1)
DOWN = (-1, 0)
LEFT = (0, -1)

# action is one of UP, RIGHT, DOWN, LEFT
# state: (row, col)
# Returns the state (row, col) before action was applied
def unapply_action(action, state):
    return (state[0] - action[0], state[1] - action[1])

# Returns the state (row, col) after action is applied
def apply_action(action, state):
    return (state[0] + action[0], state[1] + action[1])

# Observations: 1 for 1 wall, 2 for 2 walls, 3 for end, 0 for no observation
# Returns the probability of observing obs in state
def observation_prob(state, obs):
    if obs == 3:
        if state == (3, 4) or state == (2, 4):
            return 1
        else:
            return 0
    if obs == 0:
        return 1

    if state[1] == 3:
        # In 3rd column
        if obs == 1:
            return 0.9
        else:
            return 0.1
    else:
        if obs == 2:
            return 0.9
        else:
            return 0.1

# Returns true if state is not (2, 2) and in the grid, false otherwise
def is_valid_state(state):
    return state != (2, 2) and 1 <= state[0] <= 3 and 1 <= state[1] <= 4

# Normalizes a belief object
def normalize(belief):
    belief_sum = 0
    for state in belief:
        belief_sum += belief[state]

    for state in belief:
        belief[state] = belief[state] / belief_sum

    return belief

# Returns a list of (direction, probability) tuples given an action
def possible_outcomes(action):
    if action == UP:
        return [(UP, 0.8), (LEFT, 0.1), (RIGHT, 0.1)]
    elif action == LEFT:
        return [(LEFT, 0.8), (DOWN, 0.1), (UP, 0.1)]
    elif action == RIGHT:
        return [(RIGHT, 0.8), (UP, 0.1), (DOWN, 0.1)]
    else:
        # action == DOWN
        return [(DOWN, 0.8), (LEFT, 0.1), (RIGHT, 0.1)]

# Given an action and a state, returns a mapping of the state(s) the agent may have been in to their probability
def source_states(action, state):
    ss = {}
    for a, prob in possible_outcomes(action):
        old_state = unapply_action(a, state)
        # Terminal states allow no further actions
        if old_state != (3, 4) and old_state != (2, 4) and is_valid_state(old_state):
            ss[old_state] = prob

        # Check if it could have stayed in this state by bouncing off a wall
        if not is_valid_state(apply_action(a, state)) and state != (3,4) and state != (2,4):
            if state in ss:
                ss[state] += prob
            else:
                ss[state] = prob

    return ss

# Updates old_belief given a list of actions and observations
def belief_update(old_belief, actions, observations):
    for i in range(len(actions)):
        # Map from belief state to belief
        new_belief = {}

        action = actions[i]
        obs = observations[i]
        for state in old_belief:
            prob_sum = 0
            source_state_probs = source_states(action, state)
            for source_state in source_state_probs:
                prob_sum += source_state_probs[source_state] * old_belief[source_state]

            # new_belief[state] = observation_prob(state, obs)
            #                     * (sum of ways to arrive to state given state and action * old_belief[old_state])
            new_belief[state] = observation_prob(state, obs) * prob_sum
        old_belief = normalize(new_belief)

    return old_belief

# The agent has no idea where it is at the start (i.e., uniform belief state on non-terminal states)
# (row, col) notation
INITIAL_STATE_UNKNOWN = {
    (1,1): 1/9,
    (1,2): 1/9,
    (1,3): 1/9,
    (1,4): 1/9,
    (2,1): 1/9,
    (2,3): 1/9,
    (2,4): 0, # Terminal state
    (3,1): 1/9,
    (3,2): 1/9,
    (3,3): 1/9,
    (3,4): 0, # Terminal state
}

# The agent knows that it is starting in (1, 1)
INITIAL_STATE_1_1 = {
    (1,1): 1,
    (1,2): 0,
    (1,3): 0,
    (1,4): 0,
    (2,1): 0,
    (2,3): 0,
    (2,4): 0,
    (3,1): 0,
    (3,2): 0,
    (3,3): 0,
    (3,4): 0,
}

# lecture slide examples:
# print(belief_update(INITIAL_STATE_UNKNOWN, [LEFT, LEFT, LEFT, LEFT, LEFT], [0, 0, 0, 0, 0]))
# print(belief_update(INITIAL_STATE_1_1, [LEFT], [2]))

# Assignment questions (row, col)

belief_update(INITIAL_STATE_UNKNOWN, [UP, UP, UP], [2, 2, 2])
belief_update(INITIAL_STATE_UNKNOWN, [UP, UP, UP], [1, 1, 1])
belief_update({
    (1,1): 0,
    (1,2): 0,
    (1,3): 0,
    (1,4): 0,
    (2,1): 0,
    (2,3): 0,
    (2,4): 0,
    (3,1): 0,
    (3,2): 1,
    (3,3): 0,
    (3,4): 0,
}, [RIGHT, RIGHT, UP], [1, 1, 3])
belief_update(INITIAL_STATE_1_1, [UP, RIGHT, RIGHT, RIGHT], [2, 2, 1, 1])
