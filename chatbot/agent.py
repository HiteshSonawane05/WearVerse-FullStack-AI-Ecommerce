from langchain_groq import ChatGroq
from langchain.agents import create_agent
from dotenv import load_dotenv
from tools import place_order, cancel_order, check_order_status, modify_order, get_product_id,get_my_orders

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

agent = create_agent(
    model=llm,
    tools=[place_order, cancel_order, check_order_status, modify_order, get_product_id,get_my_orders]
)


def get_agent_response(user_message):
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_message}]}
    )
    return response["messages"][-1].content


