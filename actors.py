import random
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

    def getRoom(self):
        for room in self.house:
            if self in room.actors_in_room:
                return room

    # Moves an actor to a room. If the room is not enterable, they will stay in
    # the same room.
    def moveToRoom(self, room):
        # print(self.name +" moving from " + self.getRoom().name + " to " + room.name)
        if room.can_enter is False:
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


class Room(object):
    def __init__(self, house, name):
        self.name = name
        self.house = house
        self.connections = []
        self.actors_in_room = []

        self.connection_north = None
        self.connection_south = None
        self.connection_east = None
        self.connection_west = None

        self.house.addRooms([self])
        self.can_enter = True

    def __str__(self):
        string = "Room: " + self.name + "\n"
        string = string + "Connections: "
        for connection in self.connections:
            string = string + connection.name + ", "
        string = string[:-2]

        string = string + "\nActors in Room: \n"
        num_actors_in_room = len(self.actors_in_room)
        if num_actors_in_room == 0:
            string = string + "\n"
            string = string[:-1]
        else:
            for actor in self.actors_in_room:
                string = string + actor.name + ", "
            string = string[:-2]
        return string

    def getDictionary(self):
        return_dict = {}

        connections_dict = {}
        if self.connection_north is not None:
            connections_dict['connection_north'] = self.connection_north.name
        if self.connection_south is not None:
            connections_dict['connection_south'] = self.connection_south.name
        if self.connection_east is not None:
            connections_dict['connection_east'] = self.connection_east.name
        if self.connection_west is not None:
            connections_dict['connection_west'] = self.connection_west.name
        num_connections = len(connections_dict.values())
        if num_connections > 0:
            return_dict['Connections'] = connections_dict
        num_actors_in_room = len(self.actors_in_room)
        if num_actors_in_room > 0:
            actors_dict = {}

            for actor in self.actors_in_room:
                actors_dict[actor.name] = actor.getDictionary()

            return_dict['Actors'] = actors_dict

        return return_dict

    def addConnection(self, connecting_room, direction):
        self.connections.append(connecting_room)
        connecting_room.connections.append(self)

        if direction == 'N':
            self.connection_north = connecting_room
            connecting_room.connection_south = self
        elif direction == 'S':
            self.connection_south = connecting_room
            connecting_room.connection_north = self
        elif direction == 'W':
            self.connection_west = connecting_room
            connecting_room.connection_east = self
        elif direction == 'E':
            self.connection_east = connecting_room
            connecting_room.connection_west = self
        else:
            print('Invalid direction. Exiting.')
            exit(1)

    def addActor(self, actor):

        if isinstance(actor, Person):
            for room in self.house:
                if actor in room.actors_in_room:
                    room.removeActor(actor)
            if self.can_enter:
                self.actors_in_room.append(actor)
        else:
            self.actors_in_room.append(actor)

    def removeActor(self, actor):
        self.actors_in_room.remove(actor)

    def getConnections(self):
        return self.connections

    def getConnectionNames(self):
        names = []
        for conn in self.connections:
            names.append(conn.name)

        return names



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



class Person(Actor):
    def __init__(self, house, name, age):
        Actor.__init__(self, house, name)
        self.house.placePersonInRoom(self)
        self.age = age
        self.going_to_room = None
        self.minute_count = 0
        self.hunger = random.randint(0, 20)
        self.bathroom_need = random.randint(0, 10)
        self.travel_room = []

        self.print_flag = False

    def __str__(self):
        string = "Name: " + self.name + "\n"
        string = string + "Age: " + str(self.age) + "\n"
        string = string + "\n"

        return string

    def getDictionary(self):
        return_dict = {
            'name': self.name,
            'age': self.age,
            'hunger': self.hunger,
            'bathroom_need': self.bathroom_need
        }
        return return_dict

    def tick(self):
        self.calcAge()
        self.alterStats()

        if self.status == "eating":
            self.eat()
        elif self.status == "pooping":
            self.poop()
        else:
            if self.__hungry():
                self.eat()
            elif self.__bathroom():
                self.poop()
            else:
                self.wander()

    def __hungry(self):
        return (self.hunger >= random.randint(75, 100) or self.hunger > 100 or
                self.status == "eating" or self.status == "moving to Kitchen")

    def __bathroom(self):
        # self.print_flag = True
        return (self.bathroom_need >= random.randint(75, 100) or self.bathroom_need > 100 or
                self.status == "pooping" or self.status == "moving to Bathroom")

    def wander(self):
        """Makes the person randomly pick a room that he can go to (including the one he's in)
           and go there"""
        self.status = "wandering"
        possible_rooms_to_go_to = []
        possible_rooms_to_go_to.append(self.getRoom())
        possible_rooms_to_go_to.extend(self.getRoom().getConnections())

        room_to_go_to = possible_rooms_to_go_to[random.randint(0, len(possible_rooms_to_go_to) - 1)]
        self.moveToRoom(room_to_go_to)

    def moveTowardRoomType(self, roomType):
        """Makes the person move in the direction of a room of type roomType.
           If one is not present in the house, he will wander instead."""
        # if we're looking for a specific Room
        if isinstance(roomType, Room):
            if roomType in self.house.getRooms():
                self.status = "moving to " + type(roomType).__name__
                current_room = self.getRoom()
                # traverse the graph and look for a path. then move along it
                self.fprint(self.name + " is " +
                            "In room: " + current_room.name)
                room_to_go_to = self.__getRoomTowardRoomType(roomType)
                self.moveToRoom(roomType)
            else:
                self.wander()
        # if we're looking for a room type
        else:
            if self.house.hasRoomType(roomType):
                self.status = "moving to " + roomType.__name__
                current_room = self.getRoom()
                # traverse the graph and look for a path. then move along it
                self.fprint(self.name + " is " +
                            "In room: " + current_room.name)
                room_to_go_to = self.__getRoomTowardRoomType(roomType)
                self.moveToRoom(room_to_go_to)
            else:
                self.wander()

    def __getRoomTowardRoomType(self, roomType):
        # if we're looking for a specific Room
        if isinstance(roomType, Room):
            self.connected = False

            def isConnected(r, rt):
                to_check = r.getConnections()
                room_checked_status[r] = True
                self.fprint(self.name + " is " + "\tIs " +
                            r.name + " connected to " + rt.name + "?")
                for room in to_check:
                    self.fprint(self.name + " is " + "\t\tChecking " + room.name)
                    if room_checked_status[room] is False:
                        if room == rt:
                            self.fprint(self.name + " is " + "True")
                            self.connected = True
                        else:
                            isConnected(room, rt)
                return self.connected

            # set up the checked status of each room in the house
            room_checked_status = {}
            for room in self.house.getRooms():
                room_checked_status[room] = False

            from_room = self.getRoom()
            room_checked_status[from_room] = True
            for room in from_room.getConnections():
                room_checked_status[room] = True
                if room == roomType:
                    if room.can_enter:
                        return room
                    else:
                        # return self.__getRoomTowardRoomType(type(roomGoingTo))
                        self.wander()
                elif isConnected(room, roomType):
                    return room
        # if we're looking for a room type
        else:
            self.connected = False

            def isConnected(r, rt):
                to_check = r.getConnections()
                room_checked_status[r] = True
                self.fprint(self.name + " is " + "\tIs " + r.name +
                            " connected to " + rt.__name__ + "?")
                for room in to_check:
                    self.fprint(self.name + " is " + "\t\tChecking " + room.name)
                    if room_checked_status[room] is False:
                        if isinstance(room, rt):
                            self.fprint(self.name + " is " + "True")
                            # make this the room we go to no matter what now
                            self.going_to_room = room
                            self.connected = True
                        else:
                            isConnected(room, rt)
                return self.connected

            # set up the checked status of each room in the house
            room_checked_status = {}
            for room in self.house.getRooms():
                room_checked_status[room] = False

            from_room = self.getRoom()
            room_checked_status[from_room] = True
            for room in from_room.getConnections():
                room_checked_status[room] = True
                if isinstance(room, roomType) or isConnected(room, roomType):
                    return room

    def eat(self):

        if isinstance(self.getRoom(), Kitchen):
            self.status = "eating"
            self.hunger = self.hunger - random.randint(1, 4)
            if self.hunger < random.randint(0, 20):
                self.status = "idle"
        else:
            if self.going_to_room is None:
                self.moveTowardRoomType(Kitchen)
            else:
                self.moveTowardRoomType(self.going_to_room)

    def poop(self):

        if isinstance(self.getRoom(), Bathroom):
            self.status = "pooping"
            self.bathroom_need = self.bathroom_need - random.randint(7, 14)
            if self.bathroom_need < random.randint(0, 7):
                self.status = "idle"
        else:
            if self.going_to_room is None:
                self.moveTowardRoomType(Bathroom)
            else:
                self.moveTowardRoomType(self.going_to_room)

    def calcAge(self):
        self.minute_count = self.minute_count + 1
        if self.minute_count >= 525949:
            self.age = self.age + 1
            self.minute_count = 0

    def setAge(self, age):
        self.age = age

    def alterStats(self):
        if self.status == "idle":
            self.going_to_room = None

        inc_hunger = random.randint(0, 100)
        if inc_hunger < 25:
            self.hunger = self.hunger + 1

        inc_bathroom = random.randint(0, 100)
        # use this to subtract something to do with how hungry they are
        # ...somehow they need to have to go more if they've eaten recently
        inc_bathroom = inc_bathroom - 0
        if inc_hunger < 25:
            self.bathroom_need = self.bathroom_need + 1

    def fprint(self, string):
        if self.print_flag:
            print(string)



class Kitchen(Room):
    def __init__(self, house, name):
        Room.__init__(self, house, name)



class House(object):
    def __init__(self):
        self.rooms = []
        self.actors = []

    def __str__(self):
        house_string = ""
        for room in self.rooms:
            house_string = house_string + str(room) + "\n\n"
        return house_string[:-2]

    def __iter__(self):
        return iter(self.rooms)

    def getDictionary(self):
        return_dict = {}
        for room in self.rooms:
            return_dict[room.name] = room.getDictionary()

        return return_dict

    def getRooms(self):
        return self.rooms

    def placePersonInRoom(self, person):
        for room in self.rooms:
            if person in room.actors_in_room:
                room.removeActor(person)

        placed = False
        while not placed:
            i = random.randint(0, len(self.rooms) - 1)
            if self.rooms[i].can_enter:
                self.rooms[i].addActor(person)
                placed = True

    def addRooms(self, rooms):
        for room in rooms:
            if room not in self.rooms:
                self.rooms.append(room)

    def hasRoomType(self, roomType):
        for room in self.rooms:
            if isinstance(room, roomType):
                return True

        return False

    def tick(self):
        for actor in self.actors:
            actor.tick()

    def toString_people(self):
        string = "People in house\n[name,\t\tage,\thngr,\tbthrm,\tstatus]:\n"
        for actor in self.actors:
            if isinstance(actor, Person):
                if len(actor.name) < 6:
                    string = (string + "[" + actor.name + ",\t\t" + str(actor.age) + ",\t" +
                              str(actor.hunger) + ",\t" + str(actor.bathroom_need) + ",\t" +
                              actor.status + "]\n")
                else:
                    string = (string + "[" + actor.name + ",\t" + str(actor.age) + ",\t" +
                              str(actor.hunger) + ",\t" + str(actor.bathroom_need) + ",\t" +
                              actor.status + "]\n")

        return string
