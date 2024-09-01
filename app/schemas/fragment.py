from pydantic import BaseModel, Field

class FragmentBase(BaseModel):
    title: str = Field(..., description="Fragment's Title")
    content: str = Field(..., description="Fragment's Full Content")
    summary: str = Field(..., description="Fragment's Generated Summary")
    url: str = Field(..., description="Fragment's Url")
    tags: list[str] | None = Field(None, description="Fragment's Labels")
    related_fragments: list[int] | None = Field(None, description="Related Fragment's ID")

class FragmentCreate(FragmentBase):
    pass

class FragmentUpdate(FragmentBase):
    pass

class FragmentResponse(FragmentBase):
    id: int = Field(..., description="ID")
    title: str = Field(..., description="Fragment's Title")
    content: str = Field(..., description="Fragment's Full Content")
    summary: str = Field(..., description="Fragment's Generated Summary")
    url: str = Field(..., description="Fragment's Url")
    tags: list[str] = Field([], description="Fragment's Labels")
    related_fragments: list[int] | None = Field(None, description="Related Fragment's ID")
