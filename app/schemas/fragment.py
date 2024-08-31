from pydantic import BaseModel, Field
from typing import List, Optional

class FragmentBase(BaseModel):
    title: str = Field(..., description="Fragment's Title")
    content: str = Field(..., description="Fragment's Full Content")
    summary: str = Field(..., description="Fragment's Generated Summary")
    tags: Optional[str] = Field(None, description="Fragment's Labels")
    related_fragments: Optional[List[int]] = Field(None, description="Related Fragment's ID")

class FragmentCreate(FragmentBase):
    pass

class FragmentUpdate(FragmentBase):
    pass

class FragmentResponse(FragmentBase):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Fragment's Title")
    content: str = Field(..., description="Fragment's Full Content")
    summary: str = Field(..., description="Fragment's Generated Summary")
    tags: List[str] = Field([], description="Fragment's Labels")
    related_fragments: Optional[List[int]] = Field(None, description="Related Fragment's ID")
