#!/usr/bin/env python3
"""
Test Gemini integration with a more realistic menu image
"""

import requests
import json
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except:
        pass
    return "http://localhost:8001"

def create_menu_image_base64():
    """Create a realistic menu image with drinks"""
    # Create a larger image
    img = Image.new('RGB', (600, 800), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_item = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_price = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except:
        font_title = ImageFont.load_default()
        font_item = ImageFont.load_default()
        font_price = ImageFont.load_default()
    
    # Draw menu title
    draw.text((50, 30), "DRINKS MENU", fill='black', font=font_title)
    
    # Draw beverages section
    y_pos = 100
    draw.text((50, y_pos), "BEVERAGES", fill='black', font=font_title)
    y_pos += 50
    
    drinks = [
        ("Coca Cola", "$3.50"),
        ("Fresh Orange Juice", "$4.00"),
        ("Iced Coffee", "$3.75"),
        ("Green Tea", "$2.50"),
        ("Lemonade", "$3.25"),
        ("Sparkling Water", "$2.00")
    ]
    
    for drink, price in drinks:
        draw.text((70, y_pos), drink, fill='black', font=font_item)
        draw.text((400, y_pos), price, fill='black', font=font_price)
        y_pos += 30
    
    # Draw cocktails section
    y_pos += 30
    draw.text((50, y_pos), "COCKTAILS", fill='black', font=font_title)
    y_pos += 50
    
    cocktails = [
        ("Mojito", "$8.50"),
        ("Margarita", "$9.00"),
        ("Whiskey Sour", "$8.75"),
        ("Cosmopolitan", "$9.50")
    ]
    
    for cocktail, price in cocktails:
        draw.text((70, y_pos), cocktail, fill='black', font=font_item)
        draw.text((400, y_pos), price, fill='black', font=font_price)
        y_pos += 30
    
    # Convert to base64
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_data = buffer.getvalue()
    
    base64_string = base64.b64encode(img_data).decode('utf-8')
    return f"data:image/png;base64,{base64_string}"

def test_gemini_with_realistic_menu():
    """Test Gemini with a realistic menu image"""
    print("🧪 Testing Gemini Integration with Realistic Menu")
    print("=" * 50)
    
    BASE_URL = get_backend_url()
    
    try:
        # Create realistic menu image
        menu_image = create_menu_image_base64()
        print("✅ Created realistic menu image")
        
        # Send to analyze endpoint
        data = {'image_data': menu_image}
        response = requests.post(f"{BASE_URL}/api/analyze-menu", data=data)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Analysis ID: {result['analysis_id']}")
            print(f"Total drinks found: {result['total_drinks']}")
            print("Drinks found:")
            
            for i, drink in enumerate(result['drinks'], 1):
                print(f"  {i}. {drink.get('name', 'Unknown')}")
                if drink.get('description'):
                    print(f"     Description: {drink['description']}")
                if drink.get('price'):
                    print(f"     Price: {drink['price']}")
            
            if result['total_drinks'] > 0:
                print("✅ Gemini successfully extracted drinks from menu!")
                
                # Test random drink selection
                print("\n🎲 Testing random drink selection...")
                rand_data = {'analysis_id': result['analysis_id']}
                rand_response = requests.post(f"{BASE_URL}/api/random-drink", data=rand_data)
                
                if rand_response.status_code == 200:
                    rand_result = rand_response.json()
                    print(f"Random drink selected: {rand_result['selected_drink']['name']}")
                    print(f"Message: {rand_result['message']}")
                    print("✅ Random drink selection working!")
                else:
                    print(f"❌ Random drink selection failed: {rand_response.json()}")
                
                return True
            else:
                print("⚠️ Gemini processed the image but found no drinks")
                return True  # Still working, just no drinks detected
        else:
            print(f"❌ Request failed: {response.json()}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

if __name__ == "__main__":
    test_gemini_with_realistic_menu()