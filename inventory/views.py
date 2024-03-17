from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm


class HomeView(TemplateView):
    template_name = "inventory/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredients"] = Ingredient.objects.all()
        context["menuItems"] = MenuItem.objects.all()
        context["purchases"] = Purchase.objects.all()
        return context

## Ingredients
class IngredientsView(ListView):
    template_name = "inventory/ingredients_list.html"
    model = Ingredient

class NewIngredientView(CreateView):
    template_name = "inventory/add_ingredient.html"
    model = Ingredient
    form_class = IngredientForm

class UpdateIngredientView(UpdateView):
    template_name = "inventory/update_ingredient.html"
    model = Ingredient
    form_class = IngredientForm

## Menu Items
class MenuView(ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem

class NewMenuItemView(CreateView):
    template_name = "inventory/add_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm

class UpdateMenuItemView(UpdateView):
    template_name = "inventory/update_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm

class NewRecipeRequirementView(CreateView):
    template_name = "inventory/add_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm

class PurchaseView(ListView):
    template_name = "inventory/purchase_list.html"
    model = Purchase
