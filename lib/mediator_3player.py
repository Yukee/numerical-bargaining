import numpy as np
import itertools
import gambit as gb

gb_type = gb.Decimal

def reformat(s):
    # remove heading 'b\ and trailing \'
    s = s[2:-1]
    s = s.replace("\\n", "\n")
    return s

def save(game, filename):
    extension = "efg"
    gametxt = game.write(extension)
    filename = filename + "." + extension
    with open(filename, "w") as f:
        f.write(reformat(gametxt))

class mediator_3players:
    def __init__(self, m, c, x, x3_mediator):
        self._m = m
        self._c = c
        self._x = x
        self._x3 = x3_mediator
        
        self._n = 3
        self._iplayers = tuple(i for i in range(self._n))
        
        self._g = gb.Game.new_tree()
        self._g.title = f"Mediator_bargaining_n={self._n}"
        self._players = [self._g.players.add(f"P{i}") for i in range(self._n)]
        
        self.compute_outcomes()
        self.create_gametree()
        self.setup_infosets()
        self.affect_payoffs()
        
    def save(self):
        save(self._g, self._g.title)
    
    def prob(self, m):
        """
        Winning probabilities as a function of players' capacities m
        """
        return m/np.sum(m)
    
    def x2_mediator(self, i, j):
        """
        Outcome proposed by the mediator in case the two players
        the only active players
        """
        ma = self._m[[i,j]]
        xa = self._x[[i,j]]
        return self.prob(ma) @ xa
    
    def compute_outcomes(self):
        """
        Compute payoffs for all action profiles
        """
        self._war = dict()

        # general war
        self._war[self._iplayers] = self._g.outcomes.add(f"war{self._iplayers}")
        for i in self._iplayers:
            self._war[self._iplayers][i] = gb_type( 1. - self.prob(self._m) @ np.abs(self._x - self._x[i]) - self._c[i] )

        # dyadic wars
        for fighters in itertools.combinations(self._iplayers, r=2):
            self._war[fighters] = self._g.outcomes.add(f"war{fighters}")
            
            mf = self._m[list(fighters)]
            pf = self.prob(mf)
            outplayer = list(set(self._iplayers) - set(fighters))[0]
            x2 = np.array([self.x2_mediator(outplayer, j) for j in fighters])
            for i in fighters:
                self._war[fighters][i] = gb_type( 1. - pf @ np.abs(x2 - self._x[i]) - self._c[i] )
            self._war[fighters][outplayer] = gb_type( 1. - pf @ np.abs(x2 - self._x[outplayer]) )

        # peace
        self._peace = self._g.outcomes.add("peace")
        for i in self._iplayers:
            self._peace[i] = gb_type( 1. - np.abs(self._x3 - self._x[i]) )
            
    def create_gametree(self):
        """
        Create the tree structure of the tree
        Rk: No payoffs yet, and default (incorrect) information sets
        Rk2: the labelling convention matters: it will be used to attach payoffs to nodes
        """
        def add_moves(node, i):
            moves = node.append_move(self._players[i], self._n)
            moves.label = f'P{i}move'
            moves.actions[0].label = 'accept'
            idx = 0
            for j in self._iplayers: 
                if j != i:
                    moves.actions[idx + 1].label = f'{i},{j}'
                    idx += 1
            return moves

        add_moves(self._g.root, 0)
        for node1 in self._g.root.children:
            add_moves(node1, 1)
            for node2 in node1.children:
                add_moves(node2, 2)

    def setup_infosets(self):
        """
        Setup the correct information sets: players move simultaneously
        """
        common_infoset_1 = self._g.root.children[0].infoset
        common_infoset_2 = self._g.root.children[0].children[0].infoset
        for node1 in self._g.root.children:
            node1.infoset = common_infoset_1
            for node2 in node1.children:
                node2.infoset = common_infoset_2


    def affect_payoffs(self):
        """
        Attach payoffs to terminal nodes
        """
        def get_fighters(*action_strs):
            fighters = set()
            for action_str in action_strs:
                c_fighters = set()
                if action_str != 'accept':
                    action_str = action_str.split(',')
                    c_fighters = set(int(i) for i in action_str)
                fighters |= set(c_fighters)
            return tuple(fighters)

        for node0, action0 in zip(self._g.root.children, self._g.root.infoset.actions):
            for node1, action1 in zip(node0.children, node0.infoset.actions):
                for node2, action2 in zip(node1.children, node1.infoset.actions):
                    fighters = get_fighters(action0.label, action1.label, action2.label)
                    if len(fighters):
                        node2.outcome = self._war[fighters]
                    else:
                        node2.outcome = self._peace
