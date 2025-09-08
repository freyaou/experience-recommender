from typing import Optional, List, Dict, Literal
from pydantic import BaseModel

class Place(BaseModel):
    id: str
    name: str
    city: str
    categories: List[str] = []
    price: Optional[int] = None       # 1–4 (≈ $ to $$$$)
    rating: Optional[float] = None
    outdoor: Optional[bool] = None
    url: Optional[str] = None