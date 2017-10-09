from cursesmenu import *
from cursesmenu.items import *
import time
import ccxt

yobit = ccxt.yobit()
yobit.apiKey = '5CB21016D65C1AA4D0B8AA5749A0C0EB'
yobit.secret = '6e51261d69538557dc3b145e94785d80'


def pump():
    print("Pump")
    balance_dispo = yobit.fetch_balance()["BTC"]["total"]
    print("Voici la balance BTC disponible: " + str(balance_dispo))
    montant_achat = float(input("Merci de renseigner le montant d'achat desirée en btc: "))  # BTC/ASK
    pourcent_ask = float(input("Merci de renseigner le pourcentage en plus du ask desirée(1.xx): "))
    pourcent_vente = float(input("Merci de renseigner le pourcentage de vente desirée(1.xx): "))
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = market + "_BTC"
    ticker_rate = yobit.fetch_ticker(marketbtc.lower())['ask']
    rate_raw = '{0:.10f}'.format(ticker_rate)
    rate_buy = float(rate_raw) * pourcent_ask
    rate_buy_form = '{0:.10f}'.format(rate_buy)
    rate_sell = float(rate_raw) * pourcent_vente
    rate_sell_form = '{0:.10f}'.format(rate_sell)
    quantity = montant_achat / float(rate_raw)
    yobit.create_order(marketbtc, "limit", "buy", quantity, rate_buy_form)
    print("Ordre d'Achat ouvert !")
    time.sleep(3)
    yobit.create_order(marketbtc, "limit", "sell", quantity, rate_sell_form)
    print("Ordre de Vente ouvert !")
    input("Appuyer sur une touche pour continuer")


def sell():
    print("Sell order")
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = market + "_BTC"
    balance_dispo = yobit.fetch_balance()[market.upper()]["total"]
    print("Voici la balance disponible: " + str(balance_dispo))
    quantity = float(input("Veuillez entrez la quantité a vendre: "))
    if quantity <= balance_dispo:
        ticker_rate = yobit.fetch_ticker(marketbtc.lower())['ask']
        print("Taux ask: "'{0:.10f}'.format(ticker_rate))
        ask_test = input("Voulez vous vendre au taux 'Ask'? O/N: ")
        if ask_test == "O" or ask_test == "o":
            rate = '{0:.10f}'.format(ticker_rate)
        else:
            rate = float(input("Entrez le taux en BTC svp: "))
        print("Pair d'echange: " + marketbtc + " , Quantité: " + str(quantity) + " , Taux: " + str(rate))
        verif = input("Les données sont elle bonne?: ")
        if verif == "O" or verif == "o":
            yobit.create_order(marketbtc, "limit", "sell", quantity, rate)
            print("Ordre de vente ouvert !")
            input("Press Enter to continue...")
    else:
        print("Merci d'entrer une quantité valide!")
    input("Appuyer sur une touche pour continuer")


def buy():
    print("Buy order")
    market = input("Selectionner la crypto monnaie: ")
    marketbtc = market + "_BTC"
    balance_dispo = yobit.fetch_balance()["BTC"]["total"]
    print("Voici la balance BTC disponible: " + str(balance_dispo))
    quantity = float(input("Veuillez entrez la quantité a acheter: "))
    if quantity <= balance_dispo:
        ask_test = input("Voulez vous acheter au taux 'Ask'? O/N: ")
        if ask_test == "O" or ask_test == "o":
            ticker_rate = yobit.fetch_ticker(marketbtc.lower())['ask']
            rate = '{0:.10f}'.format(ticker_rate)
            quantity = quantity / float(rate)
        else:
            rate = float(input("Entrez le taux en BTC svp: "))
            rate = '{0:.10f}'.format(rate)
            quantity = quantity / float(rate)
        print("Pair d'echange: " + marketbtc + " , Quantité: " + str(quantity) + " , Taux: " + str(rate))
        verif = input("Les données sont elle bonne?: ")
        if verif == "O" or verif == "o":
            yobit.create_order(marketbtc, "limit", "buy", quantity, rate)
            print("Ordre d'achat ouvert !")
            input("Press Enter to continue...")
    else:
        print("Merci d'entrer une quantité valide!")
    input("Appuyer sur une touche pour continuer")


def main():
    menu = CursesMenu("Yobit_bot")
    pump_bot = FunctionItem("Pump_Bot", pump)
    sell_bot = FunctionItem("Sell_bot", sell)
    buy_bot = FunctionItem("Buy_bot", buy)
    menu.append_item(pump_bot)
    menu.append_item(sell_bot)
    menu.append_item(buy_bot)
    menu.start()
    menu.join()


if __name__ == "__main__":
    main()
