from pydantic import BaseModel

class Object_Detection(BaseModel):
    objects: str = None
    url_image: str

class Object_Detection_Tien(BaseModel):
    objects: list[str]
    url_image: str
    object_to_criteria: dict[str, str]