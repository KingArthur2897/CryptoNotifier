import json
import asyncio
from functools import partial
from pywebio.output import *
import pywebio.input as inp
from pywebio.session import run_js

class TaskHandler:
    def __init__(self):
        self.__coins = ["BTC", "ETH"]
        self.__type = ["Купить", "Продать"]
    
    @staticmethod
    def read_task_file():
        with open("tasks.json", encoding="utf-8") as file:
            return json.load(file)
    
    @staticmethod
    def add_task_to_file(data: dict):
        last_changes = TaskHandler.read_task_file()
        last_changes[data["name"]] = [
            data["price to alert"][0],
            data["price to alert"][1]
        ]
        with open("tasks.json","w", encoding="utf-8") as file:
            json.dump(last_changes, file, indent=4)
            
    @staticmethod
    def delete_task_in_file(coin_name, update=True):
        last_changes = TaskHandler.read_task_file()
        try:
            del last_changes[coin_name]
            with open("tasks.json","w", encoding="utf-8") as file:
                json.dump(last_changes, file, indent=4)
        except KeyError:
            print("Ключ отсутствует в списке заданий")
        if update:
            run_js("location.reload()")
            
    @staticmethod
    def get_task_list():
        result = []
        tasks = TaskHandler.read_task_file()
        print(tasks)
        
        for name, price in tasks.items():
            result.append([
                name,
                price[0],
                price[1],
                put_button(f"delete {name}", onclick=partial(TaskHandler.delete_task_in_file, name))
            ])
        put_table(
            result,
            header=["name", "price to alert","type", "delete?"]
        )
        
        put_button("Назад", onclick=lambda: run_js("location.reload()"))
    
    
    @staticmethod
    def add_task_validate(data):
        if data is None or data=="":
            return "price", "Необходимо зполнить поле"
        
    async def add_task_in_list(self):
        coin_ticker = await inp.select("Выберите монету", self.__coins, multiple=False)
        price = await inp.input("Введите ожидаемую цену", validate = TaskHandler.add_task_validate)
        type = await inp.select("Купить или продать", self.__type, multiple = False)
        if all([coin_ticker, price]):
            toast("Задание успешно завершено")
            await asyncio.sleep(1)
            run_js("location.reload()")
            TaskHandler.add_task_to_file({
                "name":coin_ticker.lower(),
                "price to alert": [
                    price.replace('.','',).replace(',','').lower(),
                    type.lower()
                ]
            })
        