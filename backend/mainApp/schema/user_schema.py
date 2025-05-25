from pydantic import BaseModel,EmailStr,validator

class SighinUserValidations(BaseModel):
    email: EmailStr
    password :str
    username : str    
    @validator("email","password","username")
    def validate(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value
    


class LoginUserValidations(BaseModel):
    email: EmailStr
    password :str
    @validator("email","password")
    def validate(value):
        value = value.strip()
        if value =="":
            raise Exception(" field must be filled!!")
        return value
    
