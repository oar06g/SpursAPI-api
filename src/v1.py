from fastapi import APIRouter


class API1:
  def __init__(self):
    self.router = APIRouter()
    
    @self.router.get("/")
    def read_root():
      return "Hello World from API1"