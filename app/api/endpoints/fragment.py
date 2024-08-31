from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.schemas.fragment import FragmentCreate, FragmentResponse
from app.services.fragment_service import FragmentService

router = APIRouter()

# Instancia del servicio de fragmentos
fragment_service = FragmentService()