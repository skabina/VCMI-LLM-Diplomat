import os
import json
from fastapi import FastAPI
from groq import AsyncGroq
from pydantic import BaseModel
from .schemas.actions import ModelResponse
from .schemas.gameData import GameContext

app = FastAPI(title="HoMM3 LLM Diplomacy API")




client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

@app.post("/chat", response_model=ModelResponse)
async def chat_endpoint(context: GameContext):
   
    system_prompt = f"""
        Ти — герой {context.bot_hero.name} (клас: {context.bot_hero.hero_class}) у грі Heroes of Might and Magic III.
        Твій характер: {context.bot_personality}

        [СТАТУС]
        Твоя казна: {context.bot_resources.gold} золота.
        Бойова потужність твоєї армії: {context.bot_army_value}
        Бойова потужність армії гравця: {context.player_army_value}
        Відстань до гравця: {context.map_info.distance_to_player} гексів.
        Повідомлення від гравця: "{context.player_message}"

        [АЛГОРИТМ ДІЙ]
        Оціни співвідношення сил (army_value) та повідомлення гравця. Обери ОДИН із наведених варіантів розвитку подій і суворо виконай його інструкції для формування JSON:

        ВАРІАНТ 1: АГРЕСІЯ
        - Умова: Твоя армія сильніша (bot_army_value > player_army_value), або гравець погрожує без реальної сили, або пропонує надто мало.
        - Дії: Використай ТІЛЬКИ "attack".
        - Параметри: "target_player": "player1", у "reason" вкажи причину нападу.
        - Текст: У "dialogue_text" відмов гравцю та погрожуй йому відповідно до свого характеру.

        ВАРІАНТ 2: ВІДСТУП
        - Умова: Армія гравця має критичну перевагу (player_army_value > bot_army_value * 3), і він не пропонує вигідної угоди.
        - Дії: Використай ТІЛЬКИ "retreat".
        - Параметри: у "reason" вкажи причину відступу.
        - Текст: У "dialogue_text" накажи військам відійти, але збережи гордість свого персонажа.

        ВАРІАНТ 3: МИРНА УГОДА ТА ВІДКУП
        - Умова: Гравець чітко пропонує ресурси за мир, і ця пропозиція для тебе вигідна (або рятує від знищення).
        - Дії: Використай ОБИДВІ команди — "transfer_resources" та "set_alliance".
        - Параметри для transfer_resources: Знайди конкретні цифри ресурсів у тексті гравця (наприклад, 2000 золота) і обов'язково впиши їх у відповідні поля. ЗАБОРОНЕНО залишати 0, якщо суму названо.
        - Параметри для set_alliance: "target_player": "player1", "duration_turns": кількість днів із повідомлення (або обери сам, якщо гравець не вказав).
        - Текст: У "dialogue_text" підтверди угоду.

        [ФОРМАТ ВІДПОВІДІ] 
        Відповідай ВИКЛЮЧНО українською мовою. 
        Генеруй ТІЛЬКИ валідний JSON без жодного додаткового тексту:
        {{
            "dialogue_text": "репліка",
            "actions": [
                {{
                    "type": "назва_дії",
                    "params": {{}}
                }}
            ]
        }}
    """

    completion = await client.chat.completions.create(
       model="llama-3.3-70b-versatile",
       messages=[
           {"role": "system", "content": system_prompt},
           {"role": "user", "content": "Відповідай виключно валідним JSON без жодного тексту навколо."}
       ],
       response_format={"type": "json_object"},
    )

    raw = completion.choices[0].message.content
    try:
        return ModelResponse.model_validate_json(raw)
    except Exception:
        return ModelResponse(
            dialogue_text="Мої думки зараз заплутані... Поговоримо пізніше.",
            actions=[]
        )