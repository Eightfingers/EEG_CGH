class Vehicle():
	def __init__(self,name,battery=70):
		self.name = name
		self.battery = battery

	def battery_life(self):
		print("It has "+ str(self.battery) + " horsepower")
		
	def name_1(self):
		print(self.name + " is my favourite car")


my_car = Vehicle ("corvette c7")
my_car.battery_life()
my_car.name_1()

class Bullet(Vehicle):
	def __init__(self,name,battery,color):
		super().__init__(name,battery)
		self.color = 350
	def color1(self):
		print("The color is " + str(self.color))
	
my_bullet = Bullet("Thunderbird", "Matte Black" ,350)
			
my_bullet.name_1()
my_bullet.battery_life()
my_bullet.color1()