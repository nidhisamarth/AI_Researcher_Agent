def detect_industry_simple(text):
    text_lower = text.lower()
    
    # EXPANDED restaurant keywords
    restaurant_keywords = ['food', 'meal', 'restaurant', 'service', 'waiter', 'dining', 'menu', 
                          'order', 'staff', 'table', 'eat', 'ate', 'dinner', 'lunch', 'server',
                          'dish', 'plate', 'delicious', 'taste', 'flavor', 'chef', 'kitchen',
                          'appetizer', 'entree', 'dessert', 'reservation', '座位', 'waitress']
    
    restaurant_count = sum(1 for word in restaurant_keywords if word in text_lower)
    
    if restaurant_count >= 3:  # If 3+ restaurant words found
        return 'restaurant'
    elif any(word in text_lower for word in ['hotel', 'room', 'stay']):
        return 'hotel'
    elif any(word in text_lower for word in ['flight', 'airline']):
        return 'airline'
    else:
        return 'general'
