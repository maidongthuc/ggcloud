from pydantic import BaseModel

class Object_Detection(BaseModel):
    objects: str = None
    url_image: str