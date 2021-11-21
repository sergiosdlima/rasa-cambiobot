# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset

import requests

#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ClearSlots(Action):

    def name(self) -> Text:
        return "action_clear_slots"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #limpa slots da cotacao
        return [AllSlotsReset()]

class SubmitCotacao(Action):

    moedas = {
        "Dólar Americano": "USD",
        "Dólar Canadense": "CAD",
        "Euro": "EUR",
        "Libra Esterlina": "GBP",
        "Peso Argentino": "ARS",
        "Bitcoin": "BTC",
        "Litecoin": "LTC",
        "Iene Japonês": "JPY",
        "Franco Suíço": "CHF",
        "Dólar Australiano": "AUD",
        "Yuan Chinês": "CNY",
        "Novo Shekel Israelense": "ILS",
        "Ethereum": "ETH",
        "XRP": "XRP",
        "Dogecoin": "DOGE",
        "Dólar de Cingapura": "SGD",
        "Dirham dos Emirados": "AED",
        "Coroa Dinamarquesa": "DKK",
        "Dólar de Hong Kong": "HKD",
        "Peso Mexicano": "MXN",
        "Coroa Norueguesa": "NOK",
        "Dólar Neozelandês": "NZD",
        "Zlóti Polonês": "PLN",
        "Riyal Saudita": "SAR",
        "Coroa Sueca": "SEK",
        "Baht Tailandês": "THB",
        "Nova Lira Turca": "TRY",
        "Dólar Taiuanês": "TWD",
        "Rand Sul-Africano": "ZAR",
        "Peso Chileno": "CLP",
        "Guarani Paraguaio": "PYG",
        "Peso Uruguaio": "UYU",
        "Peso Colombiano": "COP",
        "Sol do Peru": "PEN",
        "Boliviano": "BOB",
        "Rublo Russo": "RUB",
        "Rúpia Indiana": "INR",
    }

    def real_br_money_mask(self, my_value) -> Text:
        a = "R${:,.2f}".format(float(my_value))
        b = a.replace(",","v")
        c = b.replace(".",",")
        return c.replace("v",".")

    def name(self) -> Text:
        return "action_submit_cotacao"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #recebe dados dos slots
        moeda = tracker.get_slot("moeda")

        # return [
        #     SlotSet("resultado_cotacao", "moeda capturada: " + moeda + " - cod moeda: " + self.moedas.get(moeda)),
        #     SlotSet("moeda", None)
        # ]

        #executa alguma coisa com os dados
        moeda_cod = self.moedas.get(moeda)
    
        if moeda_cod:
            r = requests.get("https://economia.awesomeapi.com.br/json/last/" + moeda_cod)
            if r.status_code == requests.codes.ok:
                cotacao = r.json()[moeda_cod + "BRL"]
                brazilian_money = self.real_br_money_mask(cotacao["ask"])
                return [
                    SlotSet("resultado_cotacao", "1 " + moeda + " equivale a " + brazilian_money + "."),
                    SlotSet("moeda", None)
                ]
            else:
                return [
                    SlotSet("resultado_cotacao", r.text["message"]),
                    SlotSet("moeda", None)
                ]
        else:
            return [
                SlotSet("resultado_cotacao", "Moeda não encontrada."),
                SlotSet("moeda", None)
            ]
