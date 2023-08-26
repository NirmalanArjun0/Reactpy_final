from fastapi import FastAPI
from reactpy import component, html, use_state, event
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = FastAPI()

# MongoDB setup
uri = "mongodb+srv://Reactpy_Task01:arjun123@cluster0.y8gowmd.mongodb.net/"
client = MongoClient(uri, server_api=ServerApi("1"))
db = client["Reactpy_Task01"]
collection = db["Task01"]

# ReactPy component definition
@component
def MyCrud():
    alltodo = use_state([])
    name, set_name = use_state("")
    password, set_password = use_state("")

    async def mysubmit(event):
        newtodo = {"name": name, "password": password}
        await save_user(newtodo)  # Use await for asynchronous operations
        alltodo.set_value(alltodo.value + [newtodo])

    async def save_user(user_data):
        await collection.insert_one(user_data)

    # Rest of your component logic...

# Mount the ReactPy component directly to the root of the app


    list = [
        html.li(
            {},
            f"{b} => {i['name']} ; {i['password']} ",
        )
        for b, i in enumerate(alltodo.value)
    ]

    def handle_event(event):
        print(event)

    return html.div(
        {"style": {"padding": "20px"}},
        html.form(
            {"on_submit": mysubmit},
            html.h1("Login Form - ReactPy & MongoDB"),
            html.input(
                {
                    "type": "text",
                    "placeholder": "Name",
                    "on_change": lambda event: set_name(event["target"]["value"]),
                }
            ),
            html.input(
                {
                    "type": "password",
                    "placeholder": "Password",
                    "on_change": lambda event: set_password(event["target"]["value"]),
                }
            ),
            html.button(
                {
                    "type": "submit",
                    "on_click": event(lambda event: mysubmit(event), prevent_default=True),
                },
                "Submit",
            ),
        ),
        html.ul(list),
    )

# Mount the Reactpy component directly to the root of the app
app.mount("/", MyCrud)
