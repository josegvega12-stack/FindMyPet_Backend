from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


# 🐾 Modelo para crear un usuario
class UserCreate(BaseModel):
    name: str
    email: str
    password: str


# 🐾 Modelo para iniciar sesión
class UserLogin(BaseModel):
    email: str
    password: str


# 🐾 Modelo del usuario completo en la base de datos
class User(BaseModel):
    id: Optional[str]
    name: str
    email: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# 🐕 Modelo para registrar una mascota (guardada en la base de datos)
class Pet(BaseModel):
    id: Optional[str]
    name: str
    breed: Optional[str]
    color: Optional[str]
    image_url: Optional[str]
    owner_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


# 🐾 Modelo para CREAR una mascota (datos que vienen del formulario)
class PetCreate(BaseModel):
    name: str
    breed: Optional[str]
    color: Optional[str]
    image_base64: Optional[str] = None
    image_url: Optional[str] = None



# 🕵️‍♂️ Modelo para un avistamiento guardado en la base de datos
class Sighting(BaseModel):
    id: Optional[str]
    pet_id: str
    location: str
    date_reported: datetime = Field(default_factory=datetime.utcnow)
    image_url: Optional[str]


# 🧭 Modelo para CREAR un avistamiento (lo que envía el frontend)
class SightingCreate(BaseModel):
    pet_id: str
    location: str
    image_url: Optional[str]


# 📬 Modelo para notificaciones automáticas (guardadas en la base)
class Notification(BaseModel):
    id: Optional[str]
    user_id: str
    message: str
    read: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ✏️ Modelo para ACTUALIZAR una notificación existente
class NotificationUpdate(BaseModel):
    read: Optional[bool] = None


# 📊 Dashboard: muestra totales o estadísticas
class DashboardStats(BaseModel):
    total_pets: int
    total_sightings: int
    total_matches: int


# 📍 Ubicación GPS (latitud / longitud)
class Location(BaseModel):
    latitude: float
    longitude: float
