import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from openai import AsyncOpenAI

# === Твои ключи ===
TELEGRAM_TOKEN = "8765732336:AAE93UigYFl4C3Y7PQ9nahrdWJAhhsWno00"
GROQ_API_KEY = "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"

# Настройки Groq
client = AsyncOpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# Модель
AI_MODEL = "qwen/qwen3.8-27b"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

SYSTEM_PROMPT = """
Ты — эксперт по написанию продающих офферов для обмена Telegram-подарков на Stars.
Пиши только на русском языке.
Стиль: живой, цепляющий, с эмодзи, без воды и лишних слов.

Структура оффера:
1. Яркий заголовок с эмодзи
2. Краткое описание подарка
3. Что именно предлагаешь (количество Stars)
4. Условия (если указаны пользователем)
5. Чёткий призыв к действию

Не пиши ничего кроме готового текста оффера. Не добавляй пояснений.
"""

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Кидай описание подарка и сколько Stars хочешь получить.\n\n"
        "Пример:\n"
        "<code>Обменяю коллекционный подарок Golden Bear на 450 Stars. Только через гаранта, срочно</code>\n\n"
        "Я сгенерирую красивый готовый оффер.",
        parse_mode=ParseMode.HTML
    )

@dp.message()
async def generate_offer(message: types.Message):
    user_text = message.text.strip()
    if not user_text:
        return

    wait_msg = await message.answer("Генерирую оффер...")

    try:
        response = await client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ],
            temperature=0.85,
            max_tokens=700
        )
        
        offer = response.choices[0].message.content.strip()
        await wait_msg.edit_text(offer)
        
    except Exception as e:
        await wait_msg.edit_text(f"Ошибка:\n<code>{str(e)}</code>", parse_mode=ParseMode.HTML)

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
