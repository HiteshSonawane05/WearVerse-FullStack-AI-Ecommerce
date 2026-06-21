from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware   # CORS

from backend.routers.product_routes import router as product_router
from backend.routers.customer_routes import router as customer_router
from backend.routers.order_routes import router as order_router
from backend.routers.transaction_routes import router as transaction_router
from backend.routers.auth_routes import router as auth_router
from backend.routers.cart_routes import router as cart_router
from backend.routers.chat_routes import router as chat_router


app = FastAPI()

# CORS   
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, PUT, DELETE
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(customer_router)
app.include_router(order_router)
app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(cart_router)
app.include_router(chat_router)
