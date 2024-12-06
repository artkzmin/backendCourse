from pydantic import BaseModel


class StatusOK(BaseModel):
    status: str = 'OK'
