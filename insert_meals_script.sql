SELECT 
    ingredients.name, meals_ingredients.quantity, ingredients.unit
FROM 
    meals_ingredients
JOIN 
    ingredients ON meals_ingredients.ingredient_id = ingredients.id
WHERE 
    meals_ingredients.meal_id = ?;

def add_meal(name, description, instructions):
    conn = sqlite3.connect('meals.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals (name, description, instructions) VALUES (?, ?, ?)", (name, description, instructions))
    meal_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return meal_id

def add_ingredient(name, unit, calories):
    conn = sqlite3.connect('meals.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO ingredients (name, unit, calories) VALUES (?, ?, ?)", (name, unit, calories))
    ingredient_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ingredient_id

def link_meal_ingredient(meal_id, ingredient_id, quantity):
    conn = sqlite3.connect('meals.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO meals_ingredients (meal_id, ingredient_id, quantity) VALUES (?, ?, ?)", (meal_id, ingredient_id, quantity))
    conn.commit()
    conn.close()

    -- Insert sample meals
INSERT INTO meals (name, description, instructions) VALUES
('Spaghetti Bolognese', 'A classic Italian pasta dish with rich meat sauce.', 'Cook spaghetti according to package instructions. In a pan, sauté onions and garlic, add ground beef, and cook until browned. Add tomato sauce and simmer for 20 minutes. Serve over cooked spaghetti.'),
('Chicken Curry', 'A flavorful chicken dish simmered in a spiced curry sauce.', 'Marinate chicken with spices for 1 hour. Sauté onions, garlic, and ginger in a pot. Add chicken and cook for 10 minutes. Pour in coconut milk and simmer for 30 minutes. Serve with rice.'),
('Nasi Lemak', 'Fragrant rice cooked in coconut milk and pandan leaves, served with a side of sambal (a spicy paste), eggs and anchovies.', 'To make nasi lemak, cook rice with coconut milk, water, pandan leaves, and salt until fluffy. Blend and sauté chilies, shallots, and garlic to make sambal, then add tamarind, sugar, and salt, simmering until thick. Fry anchovies until crispy. Serve the rice with sambal, boiled eggs, fried anchovies, roasted peanuts, and cucumber slices.'),
('Satay', 'Grilled marinated chicken skewers served with peanut sauce.', 'To make chicken satay, marinate bite-sized chicken pieces in a mix of soy sauce, oyster sauce, turmeric, curry powder, cumin, coriander, honey, garlic, shallots, oil, salt, and pepper. After at least an hour of marinating, skewer the chicken and grill until cooked and slightly charred. For the peanut sauce, sauté chili paste, then add ground peanuts, tamarind, sugar, coconut milk, and salt, simmering until thick. Serve the satay with the sauce and fresh cucumber slices.');

-- Insert sample ingredients
INSERT INTO ingredients (name, unit, calories) VALUES
('Spaghetti', 'grams', 158),
('Tomato Sauce', 'cups', 80),
('Chicken Breast', 'grams', 165),
('Garlic', 'cloves', 5),
('Coconut Milk', 'cups', 552);

-- Link meals to ingredients
-- Spaghetti Bolognese (assuming its ID is 1)
INSERT INTO meals_ingredients (meal_id, ingredient_id, quantity) VALUES
(1, 1, 200),  -- 200 grams of Spaghetti
(1, 2, 1),    -- 1 cup of Tomato Sauce
(1, 4, 2);    -- 2 cloves of Garlic

-- Chicken Curry (assuming its ID is 2)
INSERT INTO meals_ingredients (meal_id, ingredient_id, quantity) VALUES
(2, 3, 250),  -- 250 grams of Chicken Breast
(2, 4, 3),    -- 3 cloves of Garlic
(2, 5, 1);    -- 1 cup of Coconut Milk

