import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton




def getKeyboard():
    keyboard = ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="Crea filtro x Competenze")
                                    # , KeyboardButton(text="Crea filtro x Cliente")
                                    ,KeyboardButton(text="I mie filtri"), KeyboardButton(text="Cancella filtro")]
                                    ,
                                        [
                                 KeyboardButton(text="Ticket oggi")
                                    ,KeyboardButton(text="Ticket ultimi 20")]
                                ]
                            )
    return keyboard  


def getFilterKeyboard():
    keyboard = ReplyKeyboardMarkup(
                                keyboard=[
                                    [KeyboardButton(text="+ Filtro x competenze")
                                    , KeyboardButton(text="+ Filtro x Cliente")
                                    ]
                                
                                ]
                            )
    return keyboard  



     


     
        