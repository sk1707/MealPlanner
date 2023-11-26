import datetime
import random

class Food:
    def __init__(self, name, group=None, health=None, price=None, preptime=None):
        self.name = str(name)
        self.group = group
        self.health = health
        self.price = price
        self.preptime = preptime

class Meal:
    def __init__(self, foods=[], date=None):
        self.foods = foods
        self.date = date
        self.get_health()
        self.get_price()
        self.get_preptime()

    def add_date(self, date):
        self.date = date

    def get_health(self):
        self.health = sum([i.health for i in self.foods if i])

    def get_price(self):
        self.price = sum([i.price for i in self.foods if i])

    def get_preptime(self):
        if len(self.foods) != 0:
            self.preptime = max([i.preptime for i in self.foods if i])

    def add_food(self, food):
        self.foods.append(food)
        self.get_health()
        self.get_price()
        self.get_preptime()

    def print_meal(self):
        print('Foods:', ', '.join([food.name for food in self.foods]))
        print('This meal scores a', self.health, 'out of 30 for health, and costs $', self.price)
        print('This meal takes', self.preptime, 'minutes to prepare.')

class Pantry:
    def __init__(self, foods=[]):
        self.contents = [i for i in foods]
        self.price = sum([i.price for i in foods if i])
        self.get_health()
        self.meals = []

    def get_health(self):
        groups = [f.group for f in self.contents]
        self.versatility = len(set(groups))

    def __call__(self, *newfoods):
        self.contents += newfoods
        self.price += sum([i.price for i in newfoods])
        self.get_health()

    def get_meal(self):
        protein = self.get_food('protein')
        vegetable = self.get_food('vegetable')
        carbohydrate = self.get_food('carbohydrate')
        meal = Meal([protein, vegetable, carbohydrate])
        return meal

    def get_food(self, group):
        food = random.choice([f for f in self.contents if f.group == group])
        return food

class FoodPlanner:
    def __init__(self, history=[], pantry=None, user=None, currentmeal=None):
        self.history = history
        self.pantry = pantry
        self.user = user
        self.currentmeal = currentmeal
        self.days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    def add_pantry(self, pantry):
        self.pantry = pantry

    def add_user(self, user):
        self.user = user

    def add_meal_to_history(self, meal):
        self.history.append(meal)

    def propose_meals_for_week(self):
        for day in self.days_of_week:
            print(f"\n----- {day} -----")
            self.propose_meal()

    def propose_meal(self):
        meal = self.pantry.get_meal()
        meal.add_food(self.get_protein())
        meal.print_meal()
        answer = input(f'Do you want this meal tonight, {self.user}? Say Yes or No: ')
        if answer.lower() == 'yes':
            print('I have added this meal to your food history. Enjoy!')
            meal.add_date(datetime.date.today())
            self.add_meal_to_history(meal)
        elif answer.lower() == 'no':
            print('OK! Picking a new meal for you now.')

    def get_protein(self):
        protein = random.choice([f for f in self.pantry.contents if f.group == 'protein'])
        return protein

    def view_history(self):
        for meal in self.history:
            print('On', str(meal.date), 'you ate:')
            meal.print_meal()

# Testing
myFoodPlanner = FoodPlanner()
testFoods = [Food('chicken', 'protein', 8, 5.00, 15), Food('kale', 'vegetable', 10, 5.00, 3),
             Food('rice', 'carbohydrate', 5, 3.00, 20), Food('salmon', 'protein', 9, 7.00, 25),
             Food('spinach', 'vegetable', 10, 4.00, 10), Food('pasta', 'carbohydrate', 3, 2.00, 15),
             Food('steak', 'protein', 5, 8.00, 25), Food('carrots', 'vegetable', 9, 4.00, 2),
             Food('potatoes', 'carbohydrate', 4, 3.00, 15), Food('pork', 'protein', 6, 6.00, 20),
             Food('peppers', 'vegetable', 8, 2.00, 10), Food('tofu', 'protein', 9, 4.00, 10),
             Food('broccoli', 'vegetable', 10, 3.00, 5), Food('quinoa', 'carbohydrate', 7, 6.00, 15),
             Food('beans', 'protein', 8, 2.50, 10), Food('sweet potatoes', 'carbohydrate', 9, 3.50, 20)]

myPantry = Pantry(testFoods)
myFoodPlanner.add_pantry(myPantry)
myFoodPlanner.add_user('Sonia')

# Generate and display a meal plan for a week
myFoodPlanner.propose_meals_for_week()

# View the meal history
myFoodPlanner.view_history()