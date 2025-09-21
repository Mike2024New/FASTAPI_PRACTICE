from fastapi import APIRouter

router = APIRouter(
    prefix="/notes",
    tags=["notes"]
)


@router.get("/")
def notes_main():
    return {"msg": "Приложение с заметками"}
