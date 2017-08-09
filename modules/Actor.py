class Actor(object):
    def __init__(self, house, name):
        self.name = name
        self.house = house
        self.house.actors.append(self)
        self.status = "nothing"

        self.prev_room = self.getRoom()

    def __str__(self):
        return self.name

    def tick(self):
        pass

    def putInRoom(self, room):
        from Room import Room
        for room in self.house:
            if self in room.actors_in_room:
                room.removeActor(self)
        room.addActor(self)

    def getRoom(self):
        for room in self.house:
            if self in room.actors_in_room:
                return room

    # Moves an actor to a room. If the room is not enterable, they will stay in
    # the same room.
    def moveToRoom(self, room):
        # print(self.name +" moving from " + self.getRoom().name + " to " + room.name)
        from Room import Room
        if room.canEnter is False:
            room = self.getRoom()
        if self.prev_room != self.getRoom():
            self.prev_room = self.getRoom()
        self.getRoom().removeActor(self)
        room.addActor(self)

    def getDictionary(self):
        return_dict = {
            'name' : self.name
        }
        return return_dict