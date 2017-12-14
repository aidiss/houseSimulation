from modules.Room import Room
from modules.Person import Person


class Bathroom(Room):
    def __init__(self, house, name):
        Room.__init__(self, house, name)
        self.occupied = False
        self.occupied_by = None

    def addActor(self, actor):
        Room.addActor(self, actor)
        if isinstance(actor, Person):
            self.occupied_by = actor
            self.occupied = True
            self.canEnter = False

    def removeActor(self, actor):
        if isinstance(actor, Person):
            self.occupied_by = None
            self.occupied = False
            self.canEnter = True
            Room.removeActor(self, actor)
        else:
            Room.removeActor(self, actor)
