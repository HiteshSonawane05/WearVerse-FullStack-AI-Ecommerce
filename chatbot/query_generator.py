from groq import Groq
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)


# function for FastAPI
def get_query_response(user_message):
    
    # fetch products fresh every time
    res = requests.get("http://127.0.0.1:8000/products?page=1&limit=100")
    products = res.json()
    product_list = products["data"]
    simplified = []
    for p in product_list:
        simplified.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "category": p["category"]
        })
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[
            {"role": "system", "content": f"""You are a helpful shopping assistant for a clothes ecommerce store.
Always filter products strictly based on user query.
If user asks for price limit, strictly follow it — never show products above that price.
If user asks for category, strictly filter by that category only.
Here are the available products:
{simplified}
Always return response in this exact JSON format:
[
    {{"id": 1, "name": "product name", "price": 499, "category": "men"}}
]
Return only JSON — no extra text, no explanation.
If no products found return empty list: []
"""},
            {"role": "user", "content": user_message}
        ]
    )
    
    result = response.choices[0].message.content
    
    try:
        parsed = json.loads(result)
        return parsed
    except:
        return []