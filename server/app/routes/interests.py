from fastapi import APIRouter

router = APIRouter()


@router.get("/get")
async def get_interests():
    interests = {
        "dest": [
            "Клубы",
            "Здоровье",
            "Спорт",
            "Активный отдых",
            "Музеи",
            "Агротуризм",
            "Музыка",
            "Рестораны",
            "Театры",
            "Достопримечательности",
            "Сады и парки",
            "Исторические места"
        ],
        "with": [
            "Один",
            "Семья",
            "Бизнес"
        ],
        "food": [
            "Халяль",
            "Мясо птицы",
            "Мясо животных",
            "Зерновые",
            "Молочные продукты",
            "Морепродукты",
            "Глютен",
            "Алкоголь",
            "Чай",
            "Десерты",
            "Вегитарианство"
        ]
    }
    
    return interests
