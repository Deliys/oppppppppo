import json

class OfficeFurniture:
    def __init__(self, price, manufacturer):
        self.price = price
        self.manufacturer = manufacturer
    def print_info(self):
        pass
class Table(OfficeFurniture):
    def __init__(self, price, manufacturer, material, shape):
        super().__init__(price, manufacturer)
        self.material = material
        self.shape = shape

    def print_info(self):
        print(f"Стол: Материал: {self.material}, Форма: {self.shape}, Цена: {self.price}, Производитель: {self.manufacturer}")
class Chair(OfficeFurniture):
    def __init__(self, price, manufacturer, material, adjustable_height):
        super().__init__(price, manufacturer)
        self.material = material
        self.adjustable_height = adjustable_height
    def print_info(self):
        print(f"Стул: Материал: {self.material}, Регулируемая высота: {self.adjustable_height}, Цена: {self.price}, Производитель: {self.manufacturer}")
class Cabinet(OfficeFurniture):
    def __init__(self, price, manufacturer, num_shelves, material):
        super().__init__(price, manufacturer)
        self.num_shelves = num_shelves
        self.material = material
    def print_info(self):
        print(f"Шкаф: Количество полок: {self.num_shelves}, Материал: {self.material}, Цена: {self.price}, Производитель: {self.manufacturer}")
def print_furniture(library):
    for index, furniture in enumerate(library):
        print(f"{index}. ", end="")
        furniture.print_info()
    print(f"Всего предметов: {len(library)}")


def add_furniture(library, new_furniture):
    if new_furniture["type"] == "table":
        furniture = Table(new_furniture["price"], new_furniture["manufacturer"], new_furniture["material"], new_furniture["shape"])
    elif new_furniture["type"] == "chair":
        furniture = Chair(new_furniture["price"], new_furniture["manufacturer"], new_furniture["material"], new_furniture["adjustable_height"])
    elif new_furniture["type"] == "cabinet":
        furniture = Cabinet(new_furniture["price"], new_furniture["manufacturer"], new_furniture["num_shelves"], new_furniture["material"])
    else:
        print("Неизвестный тип мебели.")
        return
    library.append(furniture)

def load_furniture_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def main():
    library = []

    # Загрузка начальных данных из JSON файла
    data = load_furniture_from_json("furniture.json")
    for item in data:
        add_furniture(library, item)

    while True:
        mode = int(input("Выберите команду:\n1) ДОБАВИТЬ\n2) УДАЛИТЬ\n3) ПЕЧАТЬ\n4) ВЫХОД\n"))
        if mode == 1:
            furniture_type = input("Введите тип мебели для добавления (стол/стул/шкаф): ").lower()
            manufacturer = input("Введите производителя: ")
            price = int(input("Введите цену: "))
            
            if furniture_type == "стол":
                material = input("Введите материал: ")
                shape = input("Введите форму: ")
                library.append(Table(price, manufacturer, material, shape))
            elif furniture_type == "стул":
                material = input("Введите материал: ")
                adjustable_height = input("Регулируется ли высота? (да/нет): ").lower() == 'да'
                library.append(Chair(price, manufacturer, material, adjustable_height))
            elif furniture_type == "шкаф":
                material = input("Введите материал: ")
                num_shelves = int(input("Введите количество полок: "))
                library.append(Cabinet(price, manufacturer, num_shelves, material))
            else:
                print("Неизвестный тип мебели.")
        elif mode == 2:
            index = int(input("Введите индекс мебели для удаления: "))
            if 0 <= index < len(library):
                del library[index]
                print("Мебель удалена.")
            else:
                print("Неверный индекс.")
        elif mode == 3:
            print_furniture(library)
        elif mode == 4:
            break
        else:
            print("Неверная команда.")
if __name__ == "__main__":
    main()
