#import library
from agents import *

#start
def program(percepts):
    '''Returns an action based on it's percepts'''
    print(percepts)
    return input()


class Gold(Thing):
    location = ()
    def to_string(self):
        return "G"
    pass


class Bump(Thing):
    def to_string(self):
        return "Bu"
    pass


class Glitter(Thing):
    location = ()
    pass


class Pit(Thing):
    location = ()
    def to_string(self):
        return "P"
    pass


class Breeze(Thing):
    location = ()
    def to_string(self):
        return "B"
    pass


class Arrow(Thing):
    pass


class Scream(Thing):
    def to_string(self):
        return "Rooaar"
    pass


class Wumpus(Agent):
    location = ()
    screamed = False
    def __init__(self):
        self.alive = True

    def to_string(self):
        if (self.alive):
            return "W"
        else:return "X"
    pass


class Stench(Thing):
    location = ()
    def to_string(self):
        return "S"
    pass


class Explorer(Agent):
    holding = []
    has_arrow = True
    killed_by = ""
    direction = Direction('down')
    location = ()
    visited = []
    safe = []
    threat_list = []
    smellList = []
    breezeList = []
    performance = 100
    win = False

    def can_grab(self, thing):
        """Explorer can only grab gold"""
        return thing.__class__ == Gold




class WumpusEnvironment(XYEnvironment):
    pit_probability = 0.2  # Probability to spawn a pit in a location. (From Chapter 7.2)
    visited = []
    wumpus = Wumpus()
    gold = Gold()

    def __init__(self, agent, width=6, height=6):
        super().__init__(width, height)
        self.init_world(agent,self.wumpus,self.gold, self.visited)


    def init_world(self, agent,wumpus,gold,visited):
        """Spawn items in the world based on probabilities from the book"""
        "AGENT"
        self.add_thing(agent, self.random_location_inbounds(exclude=None), True)
        visited.append(agent.location)



        "WUMPUS"
        w_x, w_y = self.random_location_inbounds(exclude=agent.location)
        self.add_thing(wumpus, (w_x, w_y), True)
        self.add_thing(Stench(), (w_x - 1, w_y), True)
        self.add_thing(Stench(), (w_x + 1, w_y), True)
        self.add_thing(Stench(), (w_x, w_y - 1), True)
        self.add_thing(Stench(), (w_x, w_y + 1), True)



        "GOLD"
        g_x, g_y = self.random_location_inbounds(exclude= wumpus.location)
        self.add_thing(gold, (g_x, g_y), True)
        self.add_thing(Glitter(), (g_x, g_y), True)

        "PITS"
        for x in range(self.x_start, self.x_end):
            for y in range(self.y_start, self.y_end):
                if ((x, y) != agent.location and (x, y) != (w_x,w_y) and (x, y) != (g_x,g_y)):
                    if random.random() < self.pit_probability:
                        self.add_thing(Pit(), (x, y), True)
                        self.add_thing(Breeze(), (x - 1, y), True)
                        self.add_thing(Breeze(), (x, y - 1), True)
                        self.add_thing(Breeze(), (x + 1, y), True)
                        self.add_thing(Breeze(), (x, y + 1), True)



    def get_world(self):
        """Return the items in the world"""
        result = []
        x_start, y_start = (0, 0)
        x_end, y_end = self.width, self.height

        for x in range(x_start, x_end):
            row = []
            for y in range(y_start, y_end):
                row.append(self.list_things_at((x, y)))
            result.append(row)
        return result

    def percepts_from(self, agent, location, tclass=Thing):
        """Return percepts from a given location,
        and replaces some items with percepts from chapter 7."""
        thing_percepts = {
            Gold: Glitter(),
            Wall: Bump(),
            Wumpus: Stench(),
            Pit: Breeze()}

        """Agents don't need to get their percepts"""
        thing_percepts[agent.__class__] = None

        """Gold only glitters in its cell"""
        if location != agent.location:
            thing_percepts[Gold] = None

        result = [thing_percepts.get(thing.__class__, thing) for thing in self.things
                  if thing.location == location and isinstance(thing, tclass)]
        return result if len(result) else [None]

    def percept(self, agent):
        """Return things in adjacent (not diagonal) cells of the agent.
        Result format: [Left, Right, Up, Down, Center / Current location]"""
        x, y = agent.location
        result = []
        result.append(self.percepts_from(agent, (x - 1, y)))
        result.append(self.percepts_from(agent, (x + 1, y)))
        result.append(self.percepts_from(agent, (x, y - 1)))
        result.append(self.percepts_from(agent, (x, y + 1)))
        result.append(self.percepts_from(agent, (x, y)))

        """The wumpus gives out a loud scream once it's killed."""
        wumpus = [thing for thing in self.things if isinstance(thing, Wumpus)]
        if len(wumpus) and not wumpus[0].alive and not wumpus[0].screamed:
            result[-1].append(Scream())
            wumpus[0].screamed = True

        return result

    def execute_action(self, agent, action):
        """Modify the state of the environment based on the agent's actions.
        Performance score taken directly out of the book."""

        if isinstance(agent, Explorer) and self.in_danger(agent):
            return

        agent.bump = False
        if action == 'TurnRight':
            agent.direction = Direction('down')
            agent.performance -= 1
        elif action == 'TurnLeft':
            agent.direction = Direction('up')
            agent.performance -= 1
        elif action == 'Up':
            agent.direction = Direction('left')
            agent.performance -= 1
        elif action == 'Down':
            agent.direction = Direction('right')
            agent.performance -= 1
        elif action == 'Forward':
            agent.bump = self.move_to(agent, agent.direction.move_forward(agent.location))
            agent.performance -= 1
            if(agent.location not in self.visited):
                self.visited.append(agent.location)

        elif action == 'Grab':
            things = [thing for thing in self.list_things_at(agent.location)
                      if agent.can_grab(thing)]
            if len(things):
                print("Grabbing", things[0].__class__.__name__)
                if len(things):
                    agent.holding.append(things[0])
            agent.performance -= 1
            if (isinstance(agent.holding[0],Gold)):
                agent.performance += 1001
                agent.win = True
        elif action == 'Climb':
            if agent.location == (1, 1):  # Agent can only climb out of (1,1)
                agent.performance += 1000 if Gold() in agent.holding else 0
                self.delete_thing(agent)
        elif action == 'Shoot':
            """The arrow travels straight down the path the agent is facing"""
            if agent.has_arrow:
                arrow_travel = agent.direction.move_forward(agent.location)
                while(self.is_inbounds(arrow_travel)):
                    wumpus = [thing for thing in self.list_things_at(arrow_travel)
                              if isinstance(thing, Wumpus)]
                    if len(wumpus):
                        wumpus[0].alive = False
                        break
                    arrow_travel = agent.direction.move_forward(agent.location)
                agent.has_arrow = False

    def in_danger(self, agent):
        """Check if Explorer is in danger (Pit or Wumpus), if he is, kill him"""
        for thing in self.list_things_at(agent.location):
            if isinstance(thing, Pit) or (isinstance(thing, Wumpus) and thing.alive):
                agent.alive = False
                agent.performance -= 1000
                agent.killed_by = thing.__class__.__name__
                return True
        return False

    def is_done(self):
        """The game is over when the Explorer is killed
        or if he climbs out of the cave only at (1,1)."""
        explorer = [agent for agent in self.agents if isinstance(agent, Explorer)]
        if len(explorer):
            if explorer[0].alive:
                return False
            else:
                print("Death by {} [-1000].".format(explorer[0].killed_by))
        else:
            print("Explorer climbed out {}."
                  .format(
                      "with Gold [+1000]!" if Gold() not in self.things else "without Gold [+0]"))
        return True