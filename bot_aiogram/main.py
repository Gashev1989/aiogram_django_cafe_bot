import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, or_f
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from emoji import emojize

from filters.back_to_start import GoToStart
from filters.is_adress import IsAnotherCafe, IsTrueAdress
from filters.is_contact import IsTrueContact
from filters.is_correct_date import IsCorrectDate
from filters.is_correct_order import IsCorrectOrder
from filters.is_correct_person_amount import IsPersonAmount, TooManyPersons
from handlers.appsched import (one_day_before_iftar, no_reminder,
                               three_hours_before_iftar)
from handlers.basic import (back_to_cafe_menu, back_to_date, back_to_name,
                            back_to_no_table, back_to_persons, back_to_phone,
                            back_to_set, back_to_start, cafe_menu,
                            check_order_go_to_pay, choose_another_cafe,
                            choose_date, choose_pay_method, choose_set,
                            confirm_order,
                            get_contacts, get_fake_contact, get_my_name,
                            get_phone, get_start, get_true_contact,
                            main_cafe_menu, name_for_reserving,
                            no_free_table, person_per_table, route_to_cafe,
                            pay_again_other_cafe, wrong_input)
from handlers.pay import order, pre_checkout_query, succesfull_payment
from middlewares.appshed_middelware import SchedulerMiddleware
from settings import settings
from utils.states import StepsForm


async def start():
    """Функция, запускающая работу бота."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    bot = Bot(token=settings.bots.bot_token)

    dp = Dispatcher(storage=MemoryStorage())
    scheduler = AsyncIOScheduler(timezone='Asia/Yekaterinburg')
    scheduler.start()
    dp.update.middleware.register(SchedulerMiddleware(scheduler))

    dp.message.register(
        get_start,
        Command(commands=['start', 'run'])
    )
    dp.message.register(
        order,
        F.text == 'Оплатить через ЮКасса',
        StepsForm.PAY_STATE
    )
    dp.pre_checkout_query.register(
        pre_checkout_query,
        StepsForm.PAY_STATE
    )
    dp.message.register(
        pay_again_other_cafe,
        IsTrueAdress(),
        StepsForm.PAY_STATE
    )
    dp.message.register(
        succesfull_payment,
        F.successful_payment,
        StepsForm.PAY_STATE
    )
    dp.message.register(
        get_true_contact,
        F.contact,
        IsTrueContact(),
        StepsForm.PHONE_STATE
    )
    dp.message.register(
        get_fake_contact,
        F.contact
    )
    dp.message.register(
        back_to_cafe_menu,
        F.text == 'Назад',
        or_f(
            StepsForm.CHOOSE_DATE, StepsForm.CAFE_ADDRESS, StepsForm.MENU_WATCH
        )
    )
    dp.message.register(
        back_to_date,
        F.text == 'Назад ' + emojize(':calendar:'),
        or_f(StepsForm.PERSON_AMOUNT, StepsForm.NO_FREE_TABLE)
    )
    dp.message.register(
        back_to_persons,
        F.text == 'Назад ' + emojize(':family:'),
        StepsForm.NAME_STATE
    )
    dp.message.register(
        back_to_name,
        F.text == 'Назад ' + emojize(':left_arrow:'),
        StepsForm.PHONE_STATE
    )
    dp.message.register(
        back_to_no_table,
        F.text == 'Назад ' + emojize(':reverse_button:'),
        StepsForm.CHOOSE_ANOTHER_CAFE
    )
    dp.message.register(
        back_to_phone,
        F.text == 'Назад ' + emojize(':mobile_phone:'),
        StepsForm.ORDER_STATE
    )
    dp.message.register(
        back_to_set,
        F.text == 'Назад ' + emojize(':pot_of_food:'),
        StepsForm.ORDER_CHECK_PAY
    )
    dp.message.register(
        main_cafe_menu,
        IsTrueAdress(),
        StepsForm.CHOOSE_CAFE
    )
    dp.message.register(
        back_to_start,
        GoToStart()
    )
    dp.message.register(
        get_contacts,
        F.text == 'Контакты и режим работы',
        StepsForm.CAFE_INFO
    )
    dp.message.register(
        cafe_menu,
        F.text == 'Посмотреть меню',
        StepsForm.CAFE_INFO
    )
    dp.message.register(
        route_to_cafe,
        F.text == 'Как добраться',
        StepsForm.CAFE_INFO
    )
    dp.message.register(
        choose_date,
        F.text == 'Забронировать стол',
        or_f(
            StepsForm.CAFE_INFO, StepsForm.CAFE_ADDRESS, StepsForm.MENU_WATCH
        )
    )
    dp.message.register(
        choose_another_cafe,
        F.text == 'Выбрать другое кафе',
        StepsForm.NO_FREE_TABLE
    )
    dp.message.register(
        name_for_reserving,
        F.text == 'Сдвигать столы',
        StepsForm.NO_FREE_TABLE
    )
    dp.message.register(
        name_for_reserving,
        IsAnotherCafe(),
        StepsForm.CHOOSE_ANOTHER_CAFE
    )
    dp.message.register(
        get_my_name,
        F.text == 'На моё имя',
        StepsForm.NAME_STATE
    )
    dp.message.register(
        one_day_before_iftar,
        F.text == 'За сутки',
        StepsForm.REMINDER_STATE
    )
    dp.message.register(
        three_hours_before_iftar,
        F.text == 'За 3 часа',
        StepsForm.REMINDER_STATE
    )
    dp.message.register(
        no_reminder,
        F.text == 'Не отправлять напоминание',
        StepsForm.REMINDER_STATE
    )
    dp.message.register(
        get_phone,
        F.text.regexp(r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$'),
        StepsForm.NAME_STATE
    )
    dp.message.register(
        choose_set,
        F.text.regexp(r'^((7|8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{10}$'),
        StepsForm.PHONE_STATE
    )
    dp.message.register(
        check_order_go_to_pay,
        F.text == 'Оплатить',
        StepsForm.ORDER_STATE
    )
    dp.message.register(
        choose_pay_method,
        F.text == 'Перейти к оплате',
        StepsForm.ORDER_CHECK_PAY
    )
    dp.message.register(
        confirm_order,
        IsCorrectOrder(),
        StepsForm.ORDER_STATE
    )
    dp.message.register(
        person_per_table,
        IsCorrectDate(),
        StepsForm.CHOOSE_DATE
    )
    dp.message.register(
        no_free_table,
        TooManyPersons(),
        StepsForm.PERSON_AMOUNT
    )
    dp.message.register(
        name_for_reserving,
        IsPersonAmount(),
        or_f(StepsForm.PERSON_AMOUNT, StepsForm.CHOOSE_ANOTHER_CAFE)
    )
    dp.message.register(
        wrong_input
    )

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
