from models import Meal, Order, User

meals_list = []
orders_list = []


class MealStore:
    def get_all_meals(self):
        return meals_list

    def get_meal_by_id(self, id):
        result = None
        for meal in meals_list:
            if meal.id == id:
                result = meal
                break
        return result

    def add_order(self,order):
        orders_list.append(order)

    def get_orders(self):
        return orders_list

    def delete_order(self,id):
        order = self.get_meal_by_id(id)
        orders_list.remove(order)
        return orders_list

class Admin:
    def get_all_meals(self):
        return meals_list

    def add_meal(self,meal):
        meals_list.append(meal)

    def get_meal_by_id(self,id):
        result = None
        for meal in meals_list:
            if meal.id == id:
                result = meal
                break
        return result

    def update(self,id,fields):
        meal = self.get_meal_by_id(id)
        meal.name = fields['name']
        meal.photo_url = fields['photo_url']
        meal.details = fields['details']
        meal.price = fields['price']
        return meal

    def get_all_orders(self):
        return orders_list

    def delete(self,id):
        meal = self.get_meal_by_id(id)
        meals_list.remove(meal)
        return meals_list

