from bot import bot

# Иницилизируем хендлеры, основной код
from Handler import call, command, text

print("----- БОТ ЗАПУЩЕН -----")
bot.infinity_polling()
