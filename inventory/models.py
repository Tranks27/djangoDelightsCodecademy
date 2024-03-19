from django.db import models

# Create your models here.
class Ingredient(models.Model):
    name = models.CharField(max_length=20)
    unitPrice = models.FloatField(default=0.00)
    stock = models.FloatField(default=0.00)
    unit = models.CharField(max_length=200)

    def __str__(self):
        return f"""
        name={self.name};
        stock={self.stock};
        unit={self.unit};
        unitPrice={self.unitPrice}
        """
    
    def get_absolute_url(self):
        return "/menu"
    
class MenuItem(models.Model):
    name = models.CharField(max_length=20, unique=True)
    price = models.FloatField(default=0.00)

    def __str__(self):
        return f"MenuItem = {self.name}; price={self.price}"

    def available(self):
        return all(X.enough() for X in self.reciperequirement_set.all())
    
    def get_absolute_url(self):
        return "/menu"
    
class RecipeRequirement(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.00)

    def __str__(self):
        return f"""
        menuItem=[{self.menuItem.__str__()}];
        ingredient={self.ingredient.name};
        qty={self.quantity}
        """
    def enough(self):
        return self.quantity <= self.ingredient.stock
    
    def get_absolute_url(self):
        return "/menu"

class Purchase(models.Model):
    menuItem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"""
        menuItem=[{self.menuItem.__str__()}]; 
        time={self.timestamp}
        """
    def get_absolute_url(self):
        return "/purchases"