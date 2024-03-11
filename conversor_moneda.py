import string
import tkinter
import requests
from tkinter import *
from tkinter import ttk

API_KEY = "386a1d0b1c69cc95384c40e9"
URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"



def get_currency_data():
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        currency_rates = data.get("conversion_rates", {})
        # Obtener el código de la moneda
        currency_codes = list(currency_rates.keys())
        # Combinar los códigos de moneda con los nombres de los países
        currency_data = {
            code: {
                "rate": rate,
                "name": code
            }
            for code, rate in currency_rates.items()
        }

        return currency_data

    else:
        print("Error al obtener los datos de las monedas")
        return {}


def convert_currency(amount, from_currency, to_currency, rates):
    if from_currency == to_currency:
        return amount
    if from_currency == "USD":
        return amount * rates[to_currency]["rate"]
    elif to_currency == "USD":
        return amount / rates[from_currency]["rate"]
    else:
        return amount / rates[from_currency]["rate"] * rates[to_currency][
            "rate"]


def on_convert():
    amount = float(entry_amount.get())
    from_currency = combobox_from.get()
    to_currency = combobox_to.get()

    rates = get_currency_data()
    if from_currency not in rates or to_currency not in rates:
        result_label.config(text="Moneda no válida")
        return

    result = convert_currency(amount, from_currency, to_currency, rates)
    result_label.config(
        text=f"{amount} {from_currency} es igual a {result:.2f} {to_currency}")

def exchange_values():
    from_value = entry_amount.get()
    to_value = combobox_from.get()
    combobox_from.set(combobox_to.get())
    combobox_to.set(to_value)
    entry_amount.delete(0, END)
    entry_amount.insert(0, from_value)


currency_data = get_currency_data()

def validate_input(text):
    return text.isdigit()

def validate_mayus(text):
    return text.isupper() or text == ""



ventana = Tk()
ventana.geometry("400x280")
ventana.title("Conversor de divisas")
ventana.configure(bg="white")

lbl = Label(ventana, text="Conversor de Divisas")
lbl.pack()
lbl.configure(bg="white")

lbl_amount = Label(ventana, text="Cantidad:")
lbl_amount.place(x=10, y=20, width=100, height=30)
lbl_amount.configure(bg="white")

validate_func = ventana.register(validate_input)
entry_amount = tkinter.Entry(ventana, bg="white", validate="key", validatecommand=(validate_func, "%P"))
entry_amount.place(x=110, y=20, width=100, height=30)
entry_amount.configure(bg="white")

lbl_from = Label(ventana, text="Moneda origen:")
lbl_from.place(x=10, y=60, width=100, height=30)
lbl_from.configure(bg="white")

validate_may = ventana.register(validate_mayus)
combobox_from = ttk.Combobox(ventana, width=17, height=30, validate="key", validatecommand=(validate_may, "%P"))
combobox_from["values"] = list(currency_data.keys())
combobox_from.place(x=120, y=60)

img_exchange = PhotoImage(file="imagenes/img_exchange.png")
btn_exchange = Button(ventana, text="-><-", command= exchange_values, image=img_exchange)
btn_exchange.place(x=290, y=80, width=20, height=20)

lbl_to = Label(ventana, text="Moneda destino:")
lbl_to.place(x=10, y=100, width=100, height=30)
lbl_to.configure(bg="white")

combobox_to = ttk.Combobox(ventana, width=17, height=30, validate="key", validatecommand=(validate_may, "%P"))
combobox_to["values"] = list(currency_data.keys())
combobox_to.place(x=120, y=100)

btn_convert = Button(ventana, text="Convertir", command=on_convert)
#img_convert = PhotoImage(file="imagenes/img_convert.png")
#btn_convert.config(image=img_convert)
btn_convert.place(x=10, y=140, width=100, height=30)

result_label = Label(ventana, text="Resultado")
result_label.place(relx=0, rely=0.6, width=400, height=90)
result_label.configure(bg="white")

ventana.mainloop()

