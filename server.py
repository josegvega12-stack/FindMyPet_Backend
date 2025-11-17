from fastapi import FastAPI, APIRouter, HTTPException, Depends, Header, UploadFile, File
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from typing import List, Optional
from datetime import datetime

from models import (
    User, UserCreate, UserLogin, Pet, PetCreate, Sighting, SightingCreate,
    Notification, NotificationUpdate, DashboardStats, Location
)
from auth import hash_password, verify_password, create_access_token, verify_token
from image_processing import simple_embedding, extract_colors_from_base64
from matching import matcher, process_sighting_matches
from utils import load_grid_cell
from dotenv import load_dotenv
from pathlib import Path
import os
import motor.motor_asyncio

# Ruta base del proyecto
ROOT_DIR = Path(__file__).parent

# Solo cargar .env si existe (LOCAL). En Render se usan las Environment Variables.
dotenv_path = ROOT_DIR / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)



from dotenv import load_dotenv
import os
import motor.motor_asyncio

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


# Create the main app
app = FastAPI()
# CORS para permitir acceso desde tu HTML local
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # permite cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")

security = HTTPBearer()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__) 
 # --- RUTAS DE PRUEBA PARA QUE APAREZCAN EN /docs ---
@api_router.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

@api_router.get("/ping", tags=["system"])
def ping():
    return {"pong": True}

# ==== USUARIOS: registro, login y perfil autenticado ====
from bson import ObjectId
from fastapi import status

# Colección de usuarios
users_col = db["users"]

pets_col = db["pets"]


# Utilidades para serializar
def to_user_response(doc) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "email": doc.get("email"),
        "created_at": doc.get("created_at"),
    }

# ==== UTILIDAD PARA SERIALIZAR MASCOTAS ====
def pet_response(doc) -> dict:
    if not doc:
        return None
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "breed": doc.get("breed"),
        "color": doc.get("color"),
        "image_url": doc.get("image_url"),
        "owner_id": str(doc.get("owner_id")),
        "created_at": doc.get("created_at"),
    }


async def get_user_by_email(email: str):
    return await users_col.find_one({"email": email})

# Dependencia para obtener el usuario actual a partir del token Bearer
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

    user_id = payload.get("user_id") or payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

    user = await users_col.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

    return user

# 1) Registro de usuario
@api_router.post("/users/register", tags=["users"])
async def register_user(payload: UserCreate):
    # ¿ya existe el correo?
    exists = await get_user_by_email(payload.email)
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    hashed = hash_password(payload.password)
    doc = {
        "name": payload.name,
        "email": payload.email,
        "password": hashed,
        "created_at": datetime.utcnow(),
    }
    res = await users_col.insert_one(doc)
    created = await users_col.find_one({"_id": res.inserted_id})
    return {"message": "Usuario creado correctamente"}


# 2) Login: devuelve JWT
@api_router.post("/users/login", tags=["users"])
async def login_user(payload: UserLogin):
    user = await get_user_by_email(payload.email)
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({
        "user_id": str(user["_id"]),
        "email": user["email"]
    })
    return {"access_token": token, "token_type": "bearer"}

# 3) Perfil del usuario actual (requiere Bearer Token)
@api_router.get("/users/me", tags=["users"])
async def users_me(current_user: dict = Depends(get_current_user)):
    return to_user_response(current_user)

# ==== MASCOTAS: crear mascota ====
@api_router.post("/pets/register", tags=["pets"])
async def register_pet(payload: PetCreate, current_user: dict = Depends(get_current_user)):
    # current_user viene del token JWT
    user = to_user_response(current_user)
    owner_id = user["id"]

    doc = {
        "name": payload.name,
        "breed": payload.breed,
        "color": payload.color,
        "image_url": payload.image_url,
        "owner_id": owner_id,
        "created_at": datetime.utcnow(),
    }

    res = await pets_col.insert_one(doc)
    created = await pets_col.find_one({"_id": res.inserted_id})
    return pet_response(created)




# IMPORTANTE: incluir el router en la app (solo 1 vez en todo el archivo)
app.include_router(api_router)
