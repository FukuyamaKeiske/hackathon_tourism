from fastapi import APIRouter

router = APIRouter()


@router.get("/get")
async def get_interests():
    interests = {
        "dest": [
            "достопримечательности",
            "рестораны",
            "бары",
            "активный отдых",
            "парки",
            "конференции и офисы",
        ],
        "with": [
            "семья",
            "группа",
            "один"
        ],
        "food": [
            "халяль",
            "алкоголь",
            "мясо",
            "домашняя еда",
            "русская кухня",
            "зарубежная кухня",
        ],
    }
    
    return interests
