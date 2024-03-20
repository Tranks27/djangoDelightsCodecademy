from typing import Any
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Ingredient, MenuItem, Purchase, RecipeRequirement
from .forms import IngredientForm, MenuItemForm, RecipeRequirementForm, PurchaseForm
# for aggregation
from django.db.models import Sum
# Auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout

class HomeView(LoginRequiredMixin, TemplateView):
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

class NewIngredientView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_ingredient.html"
    model = Ingredient
    form_class = IngredientForm

class UpdateIngredientView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/update_ingredient.html"
    model = Ingredient
    form_class = IngredientForm

## Menu Items
class MenuView(LoginRequiredMixin, ListView):
    template_name = "inventory/menu_list.html"
    model = MenuItem

class NewMenuItemView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm

class UpdateMenuItemView(LoginRequiredMixin, UpdateView):
    template_name = "inventory/update_menu_item.html"
    model = MenuItem
    form_class = MenuItemForm

class NewRecipeRequirementView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_recipe_requirement.html"
    model = RecipeRequirement
    form_class = RecipeRequirementForm

class PurchaseView(LoginRequiredMixin, ListView):
    template_name = "inventory/purchase_list.html"
    model = Purchase

class NewPurchaseView(LoginRequiredMixin, CreateView):
    template_name = "inventory/add_purchase.html"
    model = Purchase
    form_class = PurchaseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["menu_items"] = [X for X in MenuItem.objects.all() if X.available()]
        return context
    
    # post method needed if manually handling the form
    def post(self, request):
        menu_item_id = request.POST["menuItem"]
        menu_item = MenuItem.objects.get(pk=menu_item_id)
        requirements = menu_item.reciperequirement_set
        purchase = Purchase(menuItem=menu_item)

        for requirement in requirements.all():
            required_ingredient = requirement.ingredient
            required_ingredient.stock -= requirement.quantity
            required_ingredient.save()
        purchase.save()
        return redirect("/purchases")
    
class ReportView(LoginRequiredMixin, TemplateView):
    template_name = "inventory/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['purchases'] = Purchase.objects.all()
        revenue = Purchase.objects.aggregate(
            revenue=Sum("menuItem__price"))["revenue"]
        total_cost = 0
        for purchase in Purchase.objects.all():
            for recipe_requirement in purchase.menuItem.reciperequirement_set.all():
                total_cost += recipe_requirement.ingredient.unitPrice * recipe_requirement.quantity

        context['revenue'] = revenue
        context['total_cost'] = total_cost
        context['profit'] = revenue - total_cost

        return context

def log_out(request):
    logout(request)
    return redirect('/')