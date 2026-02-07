{\rtf1\ansi\ansicpg1251\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import asyncio\
from datetime import datetime\
\
from aiogram import Bot, Dispatcher, F\
from aiogram.types import (\
    Message,\
    InlineKeyboardButton,\
    InlineKeyboardMarkup,\
    FSInputFile\
)\
from aiogram.filters import CommandStart\
from aiogram.fsm.state import StatesGroup, State\
from aiogram.fsm.context import FSMContext\
\
# ======================\
# \uc0\u1053 \u1040 \u1057 \u1058 \u1056 \u1054 \u1049 \u1050 \u1048 \
# ======================\
\
BOT_TOKEN = "\uc0\u1042 \u1057 \u1058 \u1040 \u1042 \u1068 _\u1057 \u1070 \u1044 \u1040 _\u1058 \u1054 \u1050 \u1045 \u1053 "\
\
# username \uc0\u1080 \u1083 \u1080  chat_id \u1082 \u1072 \u1085 \u1072 \u1083 \u1072 /\u1075 \u1088 \u1091 \u1087 \u1087 \u1099 \
REPORT_CHAT_ID = "@the_coffee_barista"\
\
# \uc0\u55357 \u56393  \u1055 \u1045 \u1056 \u1045 \u1048 \u1052 \u1045 \u1053 \u1054 \u1042 \u1040 \u1053 \u1048 \u1045  \u1041 \u1040 \u1056 \u1048 \u1057 \u1058 \u1040 :\
BARISTAS = \{\
    "barista_1": "\uc0\u1041 \u1072 \u1088 \u1080 \u1089 \u1090 \u1072  1",\
    "barista_2": "\uc0\u1041 \u1072 \u1088 \u1080 \u1089 \u1090 \u1072  2",\
    "barista_3": "\uc0\u1041 \u1072 \u1088 \u1080 \u1089 \u1090 \u1072  3",\
\}\
# \uc0\u1087 \u1088 \u1086 \u1089 \u1090 \u1086  \u1087 \u1086 \u1084 \u1077 \u1085 \u1103 \u1081  \u1079 \u1085 \u1072 \u1095 \u1077 \u1085 \u1080 \u1103 , \u1085 \u1072 \u1087 \u1088 \u1080 \u1084 \u1077 \u1088 :\
# "barista_1": "\uc0\u1040 \u1085 \u1085 \u1072 "\
\
# ======================\
# \uc0\u1057 \u1054 \u1057 \u1058 \u1054 \u1071 \u1053 \u1048 \u1071 \
# ======================\
\
class Checklist(StatesGroup):\
    barista = State()\
    dose = State()\
    yield_espresso = State()\
    time = State()\
    acidity = State()\
    bitterness = State()\
    sweetness = State()\
    balance = State()\
    comment = State()\
    espresso_photo = State()\
    showcase_photo = State()\
\
# ======================\
# \uc0\u1050 \u1051 \u1040 \u1042 \u1048 \u1040 \u1058 \u1059 \u1056 \u1067 \
# ======================\
\
def barista_keyboard():\
    buttons = [\
        [InlineKeyboardButton(text=name, callback_data=key)]\
        for key, name in BARISTAS.items()\
    ]\
    return InlineKeyboardMarkup(inline_keyboard=buttons)\
\
\
def score_keyboard():\
    return InlineKeyboardMarkup(\
        inline_keyboard=[\
            [\
                InlineKeyboardButton(text=str(i), callback_data=str(i))\
                for i in range(1, 6)\
            ]\
        ]\
    )\
\
# ======================\
# \uc0\u1041 \u1054 \u1058 \
# ======================\
\
bot = Bot(token=BOT_TOKEN)\
dp = Dispatcher()\
\
# ======================\
# \uc0\u1061 \u1045 \u1053 \u1044 \u1051 \u1045 \u1056 \u1067 \
# ======================\
\
@dp.message(CommandStart())\
async def start(message: Message, state: FSMContext):\
    await state.clear()\
    await message.answer(\
        "\uc0\u9728 \u65039  \u1054 \u1090 \u1082 \u1088 \u1099 \u1090 \u1080 \u1077  \u1089 \u1084 \u1077 \u1085 \u1099 \\n\\n\u1042 \u1099 \u1073 \u1077 \u1088 \u1080  \u1073 \u1072 \u1088 \u1080 \u1089 \u1090 \u1072 :",\
        reply_markup=barista_keyboard()\
    )\
    await state.set_state(Checklist.barista)\
\
\
@dp.callback_query(Checklist.barista)\
async def choose_barista(callback, state: FSMContext):\
    barista_name = BARISTAS[callback.data]\
    await state.update_data(barista=barista_name)\
\
    await callback.message.answer("\uc0\u9749  \u1044 \u1086 \u1079 \u1080 \u1088 \u1086 \u1074 \u1082 \u1072  \u1087 \u1086 \u1084 \u1086 \u1083 \u1072  (\u1075 ):")\
    await state.set_state(Checklist.dose)\
    await callback.answer()\
\
\
@dp.message(Checklist.dose)\
async def dose(message: Message, state: FSMContext):\
    await state.update_data(dose=message.text)\
    await message.answer("\uc0\u9749  \u1042 \u1099 \u1093 \u1086 \u1076  \u1101 \u1089 \u1087 \u1088 \u1077 \u1089 \u1089 \u1086  (\u1075 ):")\
    await state.set_state(Checklist.yield_espresso)\
\
\
@dp.message(Checklist.yield_espresso)\
async def yield_espresso(message: Message, state: FSMContext):\
    await state.update_data(yield_espresso=message.text)\
    await message.answer("\uc0\u9201  \u1042 \u1088 \u1077 \u1084 \u1103  \u1087 \u1088 \u1086 \u1083 \u1080 \u1074 \u1072  (\u1089 \u1077 \u1082 ):")\
    await state.set_state(Checklist.time)\
\
\
@dp.message(Checklist.time)\
async def time(message: Message, state: FSMContext):\
    await state.update_data(time=message.text)\
    await message.answer("\uc0\u55356 \u57163  \u1050 \u1080 \u1089 \u1083 \u1086 \u1090 \u1085 \u1086 \u1089 \u1090 \u1100  (1\'965):", reply_markup=score_keyboard())\
    await state.set_state(Checklist.acidity)\
\
\
@dp.callback_query(Checklist.acidity)\
async def acidity(callback, state: FSMContext):\
    await state.update_data(acidity=callback.data)\
    await callback.message.answer("\uc0\u55357 \u56613  \u1043 \u1086 \u1088 \u1077 \u1095 \u1100  (1\'965):", reply_markup=score_keyboard())\
    await state.set_state(Checklist.bitterness)\
    await callback.answer()\
\
\
@dp.callback_query(Checklist.bitterness)\
async def bitterness(callback, state: FSMContext):\
    await state.update_data(bitterness=callback.data)\
    await callback.message.answer("\uc0\u55356 \u57199  \u1057 \u1083 \u1072 \u1076 \u1086 \u1089 \u1090 \u1100  (1\'965):", reply_markup=score_keyboard())\
    await state.set_state(Checklist.sweetness)\
    await callback.answer()\
\
\
@dp.callback_query(Checklist.sweetness)\
async def sweetness(callback, state: FSMContext):\
    await state.update_data(sweetness=callback.data)\
    await callback.message.answer("\uc0\u9878 \u65039  \u1041 \u1072 \u1083 \u1072 \u1085 \u1089  (1\'965):", reply_markup=score_keyboard())\
    await state.set_state(Checklist.balance)\
    await callback.answer()\
\
\
@dp.callback_query(Checklist.balance)\
async def balance(callback, state: FSMContext):\
    await state.update_data(balance=callback.data)\
    await callback.message.answer("\uc0\u55357 \u56541  \u1050 \u1086 \u1084 \u1084 \u1077 \u1085 \u1090 \u1072 \u1088 \u1080 \u1081 :")\
    await state.set_state(Checklist.comment)\
    await callback.answer()\
\
\
@dp.message(Checklist.comment)\
async def comment(message: Message, state: FSMContext):\
    await state.update_data(comment=message.text)\
    await message.answer("\uc0\u55357 \u56568  \u1055 \u1088 \u1080 \u1082 \u1088 \u1077 \u1087 \u1080  \u1092 \u1086 \u1090 \u1086  \u1101 \u1089 \u1087 \u1088 \u1077 \u1089 \u1089 \u1086 :")\
    await state.set_state(Checklist.espresso_photo)\
\
\
@dp.message(Checklist.espresso_photo, F.photo)\
async def espresso_photo(message: Message, state: FSMContext):\
    await state.update_data(espresso_photo=message.photo[-1].file_id)\
    await message.answer("\uc0\u55358 \u56769  \u1055 \u1088 \u1080 \u1082 \u1088 \u1077 \u1087 \u1080  \u1092 \u1086 \u1090 \u1086  \u1074 \u1080 \u1090 \u1088 \u1080 \u1085 \u1099 :")\
    await state.set_state(Checklist.showcase_photo)\
\
\
@dp.message(Checklist.showcase_photo, F.photo)\
async def showcase_photo(message: Message, state: FSMContext):\
    data = await state.get_data()\
    showcase_photo_id = message.photo[-1].file_id\
\
    now = datetime.now()\
\
    text = (\
        "\uc0\u9728 \u65039  <b>\u1054 \u1090 \u1082 \u1088 \u1099 \u1090 \u1080 \u1077  \u1089 \u1084 \u1077 \u1085 \u1099 </b>\\n\\n"\
        f"\uc0\u55357 \u56420  \u1041 \u1072 \u1088 \u1080 \u1089 \u1090 \u1072 : \{data['barista']\}\\n"\
        f"\uc0\u55357 \u56517  \{now.strftime('%d.%m.%Y')\}\\n"\
        f"\uc0\u9200  \{now.strftime('%H:%M')\}\\n\\n"\
        "\uc0\u9749  <b>\u1069 \u1089 \u1087 \u1088 \u1077 \u1089 \u1089 \u1086 :</b>\\n"\
        f"\uc0\u1044 \u1086 \u1079 \u1072 : \{data['dose']\} \u1075 \\n"\
        f"\uc0\u1042 \u1099 \u1093 \u1086 \u1076 : \{data['yield_espresso']\} \u1075 \\n"\
        f"\uc0\u1042 \u1088 \u1077 \u1084 \u1103 : \{data['time']\} \u1089 \u1077 \u1082 \\n\\n"\
        "\uc0\u11088  <b>\u1042 \u1082 \u1091 \u1089 :</b>\\n"\
        f"\uc0\u1050 \u1080 \u1089 \u1083 \u1086 \u1090 \u1085 \u1086 \u1089 \u1090 \u1100 : \{data['acidity']\}/5\\n"\
        f"\uc0\u1043 \u1086 \u1088 \u1077 \u1095 \u1100 : \{data['bitterness']\}/5\\n"\
        f"\uc0\u1057 \u1083 \u1072 \u1076 \u1086 \u1089 \u1090 \u1100 : \{data['sweetness']\}/5\\n"\
        f"\uc0\u1041 \u1072 \u1083 \u1072 \u1085 \u1089 : \{data['balance']\}/5\\n\\n"\
        "\uc0\u55357 \u56541  <b>\u1050 \u1086 \u1084 \u1084 \u1077 \u1085 \u1090 \u1072 \u1088 \u1080 \u1081 :</b>\\n"\
        f"\{data['comment']\}"\
    )\
\
    # \uc0\u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1103 \u1077 \u1084  \u1090 \u1077 \u1082 \u1089 \u1090  + 2 \u1092 \u1086 \u1090 \u1086  \u1086 \u1076 \u1085 \u1080 \u1084  \u1072 \u1083 \u1100 \u1073 \u1086 \u1084 \u1086 \u1084 \
    await bot.send_media_group(\
        chat_id=REPORT_CHAT_ID,\
        media=[\
            \{\
                "type": "photo",\
                "media": data["espresso_photo"],\
                "caption": text,\
                "parse_mode": "HTML"\
            \},\
            \{\
                "type": "photo",\
                "media": showcase_photo_id\
            \}\
        ]\
    )\
\
    await message.answer("\uc0\u9989  \u1054 \u1090 \u1095 \u1105 \u1090  \u1086 \u1090 \u1087 \u1088 \u1072 \u1074 \u1083 \u1077 \u1085 . \u1061 \u1086 \u1088 \u1086 \u1096 \u1077 \u1081  \u1089 \u1084 \u1077 \u1085 \u1099  \u9749 \u65039 ")\
    await state.clear()\
\
# ======================\
# \uc0\u1047 \u1040 \u1055 \u1059 \u1057 \u1050 \
# ======================\
\
async def main():\
    await dp.start_polling(bot)\
\
if __name__ == "__main__":\
    asyncio.run(main())}