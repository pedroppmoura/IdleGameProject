import tkinter as tk
from math import pow

class Gear:
	def __init__(self, name, cost, quantity, per_second, multiplier = None):
		self.name = name
		self.cost = cost
		self.quantity = quantity
		self.per_second = per_second
		self.multiplier = multiplier



class Clicker:
	def __init__(self, parent):
		self.parent = parent
		
		
		
		self.show_upgrade = {}

		self.gear = {}
		self.gear['lumberjack'] = Gear('lumberjack', 10, 1, 0, 1)
		self.gear['small_crops'] = Gear('small_crops', 15, 0, 1, 1)
		self.gear['chickens'] = Gear('chickens', 100, 0, 5, 1)
		self.gear['mine'] = Gear('mine', 500, 0, 40, 1)


	# Buttons

		# Changes the quantity of buildings bought at once.

		self.buy_factor = 1.0
		self.quantity_buy_once = tk.Button(parent, text = 'Buy '+str(self.buy_factor) +'x', command = lambda : self.toogle_buy())
		self.quantity_buy_once.grid(row=2,column=0)


		# Produces coins by manual clicks

		self.current_coins = 0
		self.the_button = tk.Button(parent, text = 'Chop Trees!', command = self.increment)
		self.the_button.grid(row=0, column=0)


		# Auto coin producers

		self.purchase_buttons = {}

		self.purchase_buttons['lumberjack'] = tk.Button(parent, text = 'Lumberjacks ( %.0f ) current : 1 ' % round(self.geometric(self.gear['lumberjack'].cost)), command = lambda : self.purchase('lumberjack'))
		self.purchase_buttons['small_crops'] = tk.Button(parent, text = 'Small crops ( %.0f ) current : 0' %  round(self.geometric(self.gear['small_crops'].cost)), command = lambda : self.purchase('small_crops'))
		self.purchase_buttons['chickens'] = tk.Button(parent, text = 'Chickens ( %.0f ) current : 0' %  round(self.geometric(self.gear['chickens'].cost)), command = lambda : self.purchase('chickens'))
		self.purchase_buttons['mine'] = tk.Button(parent, text = 'Mine (%.0f) current : 0' % round(self.geometric(self.gear['mine'].cost)), command = lambda : self.purchase('mine'))

		
		# Upgrades

		self.upgrade_buttons = {}

		self.upgrade_buttons['iron_axes'] = tk.Button(parent, text = 'Iron axes (2x chopping production)(50)', command = lambda : self.upgrade('iron_axes','lumberjack', 2, 50))
		self.upgrade_buttons['potatoes'] = tk.Button(parent, text = 'Potato seeds (2x small crops production)(200)', command = lambda : self.upgrade('potatoes','small_crops', 2, 200))
		self.upgrade_buttons['hen_house'] = tk.Button(parent, text = 'Hen house (2x chickens production)(500)', command = lambda : self.upgrade('hen_house','chickens', 2, 500))
		self.upgrade_buttons['torches'] = tk.Button(parent, text = 'Torches (2x mine productions)(2000)', command = lambda : self.upgrade('torches', 'mine', 2, 2000))



	# Labels for production info

		self.current_coins_label = tk.Label(parent, text = '0 coins')
		self.current_coins_label.grid(row=1, column=0)

		self.current_manual_profit_label = tk.Label(parent, text = '1 coin(s) per click')
		self.current_manual_profit_label.grid(row=1, column=1)

		self.current_auto_cps_label = tk.Label(parent, text = '0 auto cps')
		self.current_auto_cps_label.grid(row = 3, column = 2)


	# Achievements

		self.achievements_title = tk.Label(parent, text = 'Achievements')
		self.achievements_title.grid(row =  0, column = 4)

		self.achievements_1 = tk.Label(parent, text = 'Reach 100 coins per click')
		self.achievements_1.grid(row =  1, column = 4)



	# Buttons layout

		# Auto coin producers

		manual_row = -1
		auto_row = -1

		for name in self.gear:
			if self.gear[name].per_second:
				manual_row += 1	
				row = manual_row
				column = 2
			else:
				auto_row += 1
				row = auto_row
				column = 1

			self.purchase_buttons[name].grid(row=row, column=column)

		self.update()


		# Upgrades 

		for name in self.upgrade_buttons:
			self.show_upgrade[name] = True

		self.refresh_upgrades_row()
		
			
		

		

	

		#Functions


	def increment(self):
		self.current_coins += self.gear['lumberjack'].quantity * self.gear['lumberjack'].multiplier
		self.refresh_current_coins()



	def purchase (self, name):

		for dummy in range(round(self.buy_factor)):
			if round(self.current_coins) >= round(self.gear[name].cost):
				self.gear[name].quantity += 1
				self.current_coins -= round(self.gear[name].cost)

				if self.gear[name].cost < 10:
					self.gear[name].cost += 1
				else:
					self.gear[name].cost = self.gear[name].cost * 1.15


		self.current_manual_profit_label.config(text = '%.0f coins per click' % (self.gear['lumberjack'].quantity * self.gear['lumberjack'].multiplier))

		self.purchase_buttons[name].config(text = self.purchase_buttons[name]['text'].split('(')[0] + '( %.0f' % round(self.geometric(self.gear[name].cost)) + ' ) current : %.0f' % self.gear[name].quantity)

		total_cps = 0

		for name in self.gear:
			if self.gear[name].per_second:
				total_cps += self.gear[name].quantity * self.gear[name].per_second * self.gear[name].multiplier

		
		self.current_auto_cps_label.config(text = '%.0f auto cps' % total_cps)

		self.refresh_current_coins()
		


	# Buy upgrades

	def upgrade (self, button, name, multiplier_upgrade, cost_upgrade):
		if self.current_coins >= cost_upgrade:
			self.gear[name].multiplier = self.gear[name].multiplier * multiplier_upgrade
			self.current_coins -= cost_upgrade
			self.current_manual_profit_label.config(text = '%.0f coins per click' % (self.gear['lumberjack'].quantity * self.gear['lumberjack'].multiplier))
			self.upgrade_buttons[button].destroy()
			self.show_upgrade[button] = False
			self.refresh_upgrades_row()

			total_cps = 0
			for name in self.gear:
				if self.gear[name].per_second:
					total_cps += self.gear[name].quantity * self.gear[name].per_second * self.gear[name].multiplier

			self.current_auto_cps_label.config(text = '%.0f auto cps' % total_cps)
			self.refresh_current_coins()

	# Changes the amount of producers bought at once

	def toogle_buy (self):
		if self.buy_factor == 1:
			self.buy_factor = 10
		elif self.buy_factor == 10:
			self.buy_factor = 25
		elif self.buy_factor == 25:
			self.buy_factor = 100
		else:
			self.buy_factor = 1

		self.quantity_buy_once.config(text = 'Buy ' + str(self.buy_factor) +'x')

		
		for name in self.gear:
			self.purchase_buttons[name].config(text = self.purchase_buttons[name]['text'].split('(')[0] + '( %.0f' % round(self.geometric(self.gear[name].cost)) + ' ) current : %.0f' % self.gear[name].quantity)


	# Calculates the total cost of large quantities of producers 

	def geometric (self, i):

		return i * (pow(1.15, self.buy_factor) - 1) / 0.15



	def refresh_upgrades_row (self):

		upgrade_row = -1

		for name in self.upgrade_buttons:
			if self.show_upgrade[name] == True:
				upgrade_row += 1
				self.upgrade_buttons[name].grid(row=upgrade_row, column = 3)



	def refresh_current_coins (self):

		self.current_coins_label.config(text = '%.0f coins' % self.current_coins)



	#Timer

	def update (self):
		for gear in self.gear.values():
			self.current_coins += gear.per_second*gear.quantity
		self.current_coins_label.config(text = '%.0f coins' % self.current_coins)
		self.parent.after(1000, self.update)

		if (self.gear['lumberjack'].quantity * self.gear['lumberjack'].multiplier) >= 100:
		 	self.achievements_1.destroy()






root = tk.Tk()
clicker = Clicker(root)
root.mainloop()