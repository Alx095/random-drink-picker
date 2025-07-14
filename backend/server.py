from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import json
import base64
import random
from datetime import datetime
import uuid
from emergentintegrations.llm.chat import LlmChat, UserMessage, ImageContent
import asyncio

load_dotenv()

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

# API keys
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
menu_collection = db.menu_analyses

@app.get("/")
async def root():
    return {"message": "Menu Drink Selector API"}

@app.get("/api")
async def api_root():
    return {"message": "Menu Drink Selector API"}

@app.post("/api/analyze-menu")
async def analyze_menu(image_data: str = Form(...)):
    """
    Analyze menu image to extract drink options using Google Gemini
    """
    try:
        print(f"📸 Received image data of length: {len(image_data)}")
        
        # Create a new chat instance for menu analysis using Google Gemini
        chat = LlmChat(
            api_key=GEMINI_API_KEY,
            session_id=f"menu-analysis-{uuid.uuid4()}",
            system_message="""You are a menu analysis expert. Your task is to analyze menu images and extract ONLY drink items. 
            
            Rules:
            1. Only identify beverages, drinks, cocktails, juices, sodas, coffee, tea, wine, beer, etc.
            2. Ignore all food items completely
            3. Return a JSON response with this exact structure:
            {
                "drinks": [
                    {
                        "name": "drink name",
                        "description": "brief description if available",
                        "price": "price if visible"
                    }
                ]
            }
            4. If no drinks are found, return {"drinks": []}
            5. Be thorough - look for all drink sections including alcoholic and non-alcoholic beverages
            """
        ).with_model("gemini", "gemini-2.0-flash")

        print("🤖 Created LlmChat instance with Gemini successfully")

        # Create image content from base64
        image_base64 = image_data.split(',')[1] if ',' in image_data else image_data
        image_content = ImageContent(image_base64=image_base64)

        print("🖼️ Created image content successfully")

        # Analyze the menu image
        user_message = UserMessage(
            text="Analyze this menu image and extract all drink items. Return the response as valid JSON only.",
            file_contents=[image_content]
        )

        print("💬 Sending message to Google Gemini...")
        
        # Get analysis from Gemini
        response = await chat.send_message(user_message)
        
        print(f"✅ Received response from Gemini: {response[:200]}...")
        
        # Parse the JSON response
        try:
            analysis_result = json.loads(response)
            print("✅ Successfully parsed JSON response")
        except json.JSONDecodeError as json_err:
            print(f"⚠️ JSON decode error: {json_err}")
            # If response is not valid JSON, try to extract JSON from the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                analysis_result = json.loads(json_match.group())
                print("✅ Extracted JSON from response")
            else:
                print("❌ Could not find valid JSON in response")
                analysis_result = {"drinks": []}

        # Generate analysis ID
        analysis_id = str(uuid.uuid4())
        
        # Store analysis in database
        analysis_record = {
            "analysis_id": analysis_id,
            "drinks": analysis_result.get("drinks", []),
            "timestamp": datetime.utcnow(),
            "image_data": image_data[:100] + "..." if len(image_data) > 100 else image_data  # Store truncated image data
        }
        
        await menu_collection.insert_one(analysis_record)
        print(f"💾 Stored analysis in database with ID: {analysis_id}")
        
        return {
            "analysis_id": analysis_id,
            "drinks": analysis_result.get("drinks", []),
            "total_drinks": len(analysis_result.get("drinks", []))
        }

    except Exception as e:
        print(f"❌ Error analyzing menu: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error analyzing menu: {str(e)}")

@app.post("/api/random-drink")
async def get_random_drink(analysis_id: str = Form(...)):
    """
    Get a random drink from the analyzed menu
    """
    try:
        # Retrieve analysis from database
        analysis = await menu_collection.find_one({"analysis_id": analysis_id})
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        drinks = analysis.get("drinks", [])
        
        if not drinks:
            raise HTTPException(status_code=404, detail="No drinks found in this menu")
        
        # Select random drink
        random_drink = random.choice(drinks)
        
        return {
            "selected_drink": random_drink,
            "message": f"🍹 Your random drink choice: {random_drink['name']}!"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error selecting random drink: {str(e)}")

@app.get("/api/analysis/{analysis_id}")
async def get_analysis(analysis_id: str):
    """
    Get analysis details by ID
    """
    try:
        analysis = await menu_collection.find_one({"analysis_id": analysis_id})
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")
        
        return {
            "analysis_id": analysis["analysis_id"],
            "drinks": analysis["drinks"],
            "total_drinks": len(analysis["drinks"]),
            "timestamp": analysis["timestamp"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving analysis: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)