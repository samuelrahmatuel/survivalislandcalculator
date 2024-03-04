from collections import defaultdict

class CraftingRecipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients

    def get_ingredients(self):
        return self.ingredients

# Recipes
crafting_recipes = {
    'Iron Ingot': {'Iron Ore': 2, 'Wood': 3},
    'Charcoal': {'Wood': 2},
    'Copper Ingot': {'Copper Ore': 3, 'Wood': 4},
    'Sulfur': {'Sulfur Ore': 3, 'Wood': 4},
    'Alloy': {'Iron Ingot': 1, 'Copper Ingot': 1, 'Charcoal': 1},
    'Steel': {'Iron Ingot': 2, 'Lime': 2, 'Charcoal': 1},  # Steel is used in some recipes
}

# Create recipe objects
recipes = {name: CraftingRecipe(name, ingredients) for name, ingredients in crafting_recipes.items()}

def calculate_ingredients(item, quantity, ingredients=None):
    if ingredients is None:
        ingredients = defaultdict(int)

    recipe = recipes.get(item)
    if not recipe:
        return ingredients  # Base case: If the item is not craftable, return current ingredients

    # Calculate the number of times the recipe needs to be crafted (considering batch size)
    craft_count = max(1, quantity // recipe.ingredients.get('Crafting Item', 1))

    # Add required ingredients for the recipe (scaled by craft count)
    for ingredient, amount in recipe.ingredients.items():
        if ingredient != 'Crafting Item':
            ingredients[ingredient] += amount * craft_count

    # Recursively calculate ingredients for sub-recipes
    for ingredient, amount in recipe.ingredients.items():
        if ingredient != 'Crafting Item':
            calculate_ingredients(ingredient, amount * craft_count, ingredients)

    return ingredients

import streamlit as st

st.set_page_config(page_title="Survival Island Resource Calculator")

st.markdown("<h2 style='text-align: center; color: white;'>Farming Assistant</h2>", unsafe_allow_html=True)

# Add the image from local file path
image_path = "image1.png"  # Replace this with the path to your image file
st.image(image_path, use_column_width=True)

# Simple Overview
st.write("This tool helps you plan your resource gathering for crafting refined materials in Survival Island. Select your smelter level, choose the material you want to craft, and specify the quantity and batch size. The app will calculate the total raw materials needed for your desired output.")

# How to Use
st.subheader("How to Use:")
st.write("1. Select your current Smelter Level.")
st.write("2. Choose the refined material you want to craft from the dropdown menu.")
st.write("3. Enter the desired quantity of the material per batch.")
st.write("4. Specify the number of batches you want to craft.")
st.write("5. Click the 'Calculate' button.")
st.write("6. The app will display the crafting information and a list of required raw materials for the specified quantity.")

# Smelter level selection
smelter_level_options = ["Select Level", 9, 10]
selected_smelter_level = st.selectbox("Smelter Level 🏭", smelter_level_options)

# Limit based on Smelter Level
craft_limit = {
    9: 3000,
    10: 5000
}

if selected_smelter_level != "Select Level":
    # Recipe selection, quantity input with limit validation, and batch size input
    recipe_names = list(recipes.keys())
    selected_recipe = st.selectbox("Select Refined Material 📜", recipe_names)

    max_quantity = craft_limit.get(selected_smelter_level, 0)
    quantity = st.number_input("Quantity (per Batch) 🛠️", min_value=1, max_value=max_quantity, value=1)
    batch_size = st.number_input("Batch Size 📦", min_value=1, value=1)

    if st.button("Calculate 🧮"):
        total_ingredients = calculate_ingredients(selected_recipe, quantity * batch_size)

        # Create two columns for displaying crafting info and ingredients
        col1, col2 = st.columns(2)

        with col1:
            st.header("Crafting Info")
            st.write(f"Smelter Level: {selected_smelter_level}")
            st.write(f"Crafting Recipe: {selected_recipe}")
            st.write(f"Quantity per Batch: {quantity} Pcs")
            st.write(f"Batch Size: {batch_size}")
            st.write(f"Total Quantity: **:green[{quantity * batch_size} {selected_recipe}]**")

        with col2:
            st.header("Resource Needed")
            for ingredient, amount in total_ingredients.items():
                if ingredient in ["Iron Ingot", "Charcoal", "Copper Ingot", "Alloy", "Steel"]:
                    # Use `st.markdown` with raw HTML for green and bold text
                    st.markdown(f"- **:green[{amount} {ingredient}]**")
                else:
                    st.write(f"- **{amount} {ingredient}**")

            # Add notes about raw materials
            st.write("*_White text indicates total non-refined raw materials needed._*")
else:
    st.warning("Please select your Smelter Level")

html_temp = """
<div style="text-align: center; font-size: 12px; color: gray;">
    This simple Application Made By <b><i><a href="https://rahmatuelsamuel.com" style="color: gray;">Rahmatuel Samuel</a></i></b>
</div>
"""

st.markdown(html_temp, unsafe_allow_html=True)
