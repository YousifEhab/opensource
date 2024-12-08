import random
from faker import Faker

fake = Faker('en_US')


# Number of entries
entries = 999

# Generate users
users = []
for i in range(999):
    user_id = f"U{str(i+1).zfill(3)}"
    user_name = fake.name()
    user_phone = fake.random_number(digits=9, fix_len=True)
    users.append((user_id, user_name, user_phone))

# Generate delivery agents
agents = []
for i in range(999):
    agent_id = f"A{str(i+1).zfill(3)}"
    agent_name = fake.name()
    agent_phone = fake.random_number(digits=9, fix_len=True)
    agent_rating = round(random.uniform(3.0, 5.0), 1)
    agents.append((agent_id, agent_name, agent_phone, agent_rating))

# Generate restaurants
restaurants = []
categories = ['Italian', 'Chinese', 'Indian', 'Mexican', 'American', 'Thai']
locations = ['Downtown', 'Uptown', 'Suburb', 'City Center', 'Old Town', 'Beachside']
for i in range(999):
    restaurant_id = f"R{str(i+1).zfill(3)}"
    restaurant_name = fake.company()
    restaurant_rating = round(random.uniform(1.0, 5.0), 1)
    restaurant_category = random.choice(categories)
    restaurant_location = random.choice(locations)
    restaurants.append((restaurant_id, restaurant_name, restaurant_rating, restaurant_category, restaurant_location))


# Curated food names for each category
category_food_names = {
    'Starter': [
        'Bruschetta', 'Spring Rolls', 'Caesar Salad', 'Tom Yum Soup',
        'Garlic Bread', 'Caprese Salad', 'French Onion Soup', 'Chicken Wings',
        'Stuffed Mushrooms', 'Shrimp Cocktail', 'Vegetable Samosa', 'Mini Quiche',
        'Deviled Eggs', 'Hummus Platter', 'Spinach Dip'
    ],
    'Main Course': [
        'Grilled Salmon', 'Margherita Pizza', 'Chicken Alfredo Pasta', 'Beef Tacos',
        'Pad Thai', 'Cheeseburger', 'Steak Frites', 'Veggie Wrap',
        'Sushi Platter', 'Lamb Chops', 'Eggplant Parmesan', 'Stuffed Bell Peppers',
        'Shrimp Scampi', 'BBQ Ribs', 'Butter Chicken'
    ],
    'Dessert': [
        'Tiramisu', 'Chocolate Lava Cake', 'Banana Split', 'Cheesecake',
        'Crème Brûlée', 'Ice Cream Sundae', 'Fruit Tart', 'Brownie Sundae',
        'Panna Cotta', 'Macarons', 'Lemon Meringue Pie', 'Coconut Pudding',
        'Strawberry Shortcake', 'Mango Sorbet', 'Apple Crumble'
    ],
    'Beverage': [
        'Iced Latte', 'Mango Smoothie', 'Lemonade', 'Mojito',
        'Espresso', 'Chai Tea Latte', 'Hot Chocolate', 'Green Tea',
        'Orange Juice', 'Pina Colada', 'Cappuccino', 'Berry Smoothie',
        'Sparkling Water', 'Herbal Tea', 'Vanilla Milkshake'
    ]
}

# Define reasonable price ranges for each category
price_ranges = {
    'Starter': (5, 15),      # Prices in the range of $5 to $15
    'Main Course': (10, 30), # Prices in the range of $10 to $30
    'Dessert': (5, 12),      # Prices in the range of $5 to $12
    'Beverage': (3, 10)      # Prices in the range of $3 to $10
}

menu_items = []
item_id = 1  # Initialize item ID

for restaurant in restaurants:
    restaurant_id = restaurant[0]  # Get the restaurant ID
    menu = []

    # Generate items per category
    for category, count_range in [('Starter', (1, 3)), 
                                  ('Main Course', (4, 6)), 
                                  ('Dessert', (2, 2)), 
                                  ('Beverage', (3, 5))]:
        item_count = random.randint(*count_range)
        available_items = random.sample(category_food_names[category], item_count)

        for item_name in available_items:
            # Generate a price within the range for this category
            item_price = random.randint(*price_ranges[category]) * 10  # Convert to whole dollars
            menu.append((item_id, item_price, item_name, category, restaurant_id))
            item_id += 1

    menu_items.extend(menu)

# Generate orders
orders = []
for i in range(3000000):
    order_id = i + 1
    order_delivery_location = fake.address().replace("\n", ", ")
    order_paymentmethod = random.choice(['Cash', 'Card'])
    order_date = fake.date_time_this_year()
    user_id = random.choice(users)[0]
    restaurant_id = random.choice(restaurants)[0]
    agent_id = random.choice(agents)[0]
    orders.append((order_id, order_delivery_location, order_paymentmethod, order_date, user_id, restaurant_id, agent_id))

    
# Generate menu_item_has_order
menu_item_orders = []
for order in orders:
    order_id = order[0]
    assigned_items = set()  # Keep track of items already assigned to this order
    num_items = random.randint(1, 5)  # Number of items for this order

    while len(assigned_items) < num_items:
        item_id = random.choice(menu_items)[0]
        if item_id not in assigned_items:  # Add only if it's not already assigned
            menu_item_orders.append((item_id, order_id))
            assigned_items.add(item_id)  # Mark this item as assigned to the order

# Generate SQL insert statements
sql_statements = []

# Users
sql_statements.append("-- Inserting users")
sql_statements.append("INSERT INTO `FoodApp`.`user` (user_id, user_name, user_phone) VALUES")
sql_statements.append(",\n".join([f"('{u[0]}', '{u[1]}', {u[2]})" for u in users]) + ";")

# Delivery agents
sql_statements.append("-- Inserting delivery agents")
sql_statements.append("INSERT INTO `FoodApp`.`delivery_agent` (agent_id, agent_name, agent_phone, agent_rating) VALUES")
sql_statements.append(",\n".join([f"('{a[0]}', '{a[1]}', {a[2]}, {a[3]})" for a in agents]) + ";")

# Restaurants
sql_statements.append("-- Inserting restaurants")
sql_statements.append("INSERT INTO `FoodApp`.`restaurant` (restaurant_id, restaurant_name, restaurant_rating, restaurant_category, restaurant_location) VALUES")
sql_statements.append(",\n".join([f"('{r[0]}', '{r[1]}', {r[2]}, '{r[3]}', '{r[4]}')" for r in restaurants]) + ";")

# Menu items
sql_statements.append("-- Inserting menu items")
sql_statements.append("INSERT INTO `FoodApp`.`menu_item` (item_id, item_price, item_name, item_category, restaurant_id) VALUES")
sql_statements.append(",\n".join([f"({m[0]}, {m[1]}, '{m[2]}', '{m[3]}', '{m[4]}')" for m in menu_items]) + ";")

# Orders
sql_statements.append("-- Inserting orders")
sql_statements.append("INSERT INTO `FoodApp`.`food_order` (order_id, order_delivery_location, order_paymentmethod, order_date, user_id, restaurant_id, agent_id) VALUES")
sql_statements.append(",\n".join([f"({o[0]}, '{o[1]}', '{o[2]}', '{o[3]}', '{o[4]}', '{o[5]}', '{o[6]}')" for o in orders]) + ";")

# Menu item has order
sql_statements.append("-- Inserting menu_item_has_order")
sql_statements.append("INSERT INTO `FoodApp`.`food_order_has_menu_item` (item_id, order_id) VALUES")
sql_statements.append(",\n".join([f"({mo[0]}, {mo[1]})" for mo in menu_item_orders]) + ";")

# Write to a file
with open("insert_dummy_data.sql", "w") as file:
    file.write("\n".join(sql_statements))

print("SQL script generated successfully as 'insert_dummy_data.sql'")
