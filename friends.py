from Simulation import *
from actors import *

class Friends(Simulation):
	def __init__(self):
		Simulation.__init__(self)
	
	def setup(self):	
		self.home = House()
		
		kitchen = Kitchen(self.home, "Kitchen", 'W')
		livingRoom = Room(self.home, "Living Room", 'W')
		diningRoom = Room(self.home, "Dining Room", 'W')
		joshuaBedroom = Room(self.home, "Joshua's Room", 'W')
		emmaBedroom = Room(self.home, "Emma's Room", 'W')
		jacksonBedroom = Room(self.home, "Jackson's Room", 'W')
		claireBedroom = Room(self.home, "Claire's Room", 'W')
		hallway = Room(self.home, "Hallway", 'W')
		bathroom = Bathroom(self.home, "Bathroom", 'W')
		laundryRoom = Room(self.home, "Laundry Room", 'W')
		
		kitchen.addConnection([livingRoom, diningRoom])
		hallway.addConnection([joshuaBedroom, emmaBedroom, claireBedroom, jacksonBedroom, livingRoom, laundryRoom, bathroom])
		#kitchen.addConnections([bathroom])
		#hallway.addConnections([livingRoom, bathroom])
		
		joshua = Person(self.home, "Joshua", 21)
		joshua.hunger = 69
		emma = Person(self.home, "Emma", 19)
		jackson = Person(self.home, "Jackson", 20)
		claire = Person(self.home, "Claire", 21)
		

sim = Friends()
sim.run()
