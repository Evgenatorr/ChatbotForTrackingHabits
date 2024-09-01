from src.loader import bot


async def reminder_task(chat_id, title_habit):
    await bot.send_message(chat_id, text=f'<i>Напоминание о привычке "{title_habit}"\n'
                                         f'Не забывайте выполнять привычки</i>')
