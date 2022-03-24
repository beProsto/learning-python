# testing out encapsulation (classes and objects)
class Animal:
	health = 100
	damage = 20
	name = "Basic Animal Name"
	isdead = False

	def attack(self, animal):
		if not self.isdead:
			self.attackRoar()
			animal.takeDamage(self.damage)
	
	def takeDamage(self, dmg):
		if not self.isdead:
			self.health -= dmg
			self.damageRoar()
			self.hasDied()

	def hasDied(self):
		if self.health <= 0:
			self.deathRoar()
			print(self.name, "has died!")
			self.isdead = True
	
	def deathRoar(self):
		print("Basic Animal Death Roar") 
	def damageRoar(self):
		print("Basic Animal Damage Roar") 
	def attackRoar(self):
		print("Basic Animal Attack Roar")

class Dog(Animal):
	health = 120
	name = "Dog"
	def deathRoar(self):
		print("woohoo") 
	def damageRoar(self):
		print("woof") 
	def attackRoar(self):
		print("rawr")

class Swine(Animal):
	name = "Swine"
	def deathRoar(self):
		print("whiiiiiiii") 
	def damageRoar(self):
		print("whee") 
	def attackRoar(self):
		print("hrum")

a = Swine()
b = Dog()

print("--- Starting Stats: ---")
print("Swine:", a.health, "hp,", a.damage, "dmg")
print("Doggo:", b.health, "hp,", b.damage, "dmg")
print("---  ---")


for i in range(1, 6):
	print("Round:", i)
	a.attack(b)
	b.attack(a)

print("--- Final Stats: ---")
print("Swine:", a.health, "hp,", a.damage, "dmg")
print("Doggo:", b.health, "hp,", b.damage, "dmg")
print("---  ---")