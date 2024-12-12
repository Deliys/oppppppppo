class OfficeFurniture:
    """основа фигуры"""
    def __init__(self, price, manufacturer):
        self.price = price
        self.manufacturer = manufacturer
    def print_info(self):
        pass

class Table(OfficeFurniture):
    "столик"
    def __init__(self, price, manufacturer, material, shape):
        super().__init__(price, manufacturer)
        self.material = material
        self.shape = shape

    def print_info(self):
        print(f"Стол: Материал: {self.material},\
                Форма: {self.shape}, Цена: {self.price},\
                Производитель: {self.manufacturer}")

class Chair(OfficeFurniture):
    """стул"""
    def __init__(self, price, manufacturer, material, adjustable_height):
        super().__init__(price, manufacturer)
        self.material = material
        self.adjustable_height = adjustable_height

    def print_info(self):
        print(f"Стул: Материал: {self.material},\
                Регулируемая высота: {self.adjustable_height},\
                Цена: {self.price}, Производитель: {self.manufacturer}")

class Cabinet(OfficeFurniture):
    """шкаф"""
    def __init__(self, price, manufacturer, num_shelves, material):
        super().__init__(price, manufacturer)
        self.num_shelves = num_shelves
        self.material = material

    def print_info(self):
        print(f"Шкаф: Количество полок: {self.num_shelves},\
                Материал: {self.material},\
                Цена: {self.price},\
                Производитель: {self.manufacturer}")

def parse_command(library, command):
    """парсер команд из файлика"""
    parts = command.split()
    if parts[0] == "ADD":
        if parts[1] == "TABLE":
            library.append(Table(int(parts[2]), parts[3], parts[4], parts[5]))
        elif parts[1] == "CHAIR":
            library.append(Chair(int(parts[2]), parts[3], parts[4], parts[5] == "TRUE"))
        elif parts[1] == "CABINET":
            library.append(Cabinet(int(parts[2]), parts[3], int(parts[4]), parts[5]))
        else:
            print("Неизвестный тип мебели.")
    elif parts[0] == "REM":
        if parts[1] == "TABLE":
            library = [furniture for furniture in library if not (isinstance(furniture, Table) and furniture.price == int(parts[2]))]
        elif parts[1] == "CHAIR":
            library = [furniture for furniture in library if not (isinstance(furniture, Chair) and furniture.price == int(parts[2]))]
        elif parts[1] == "CABINET":
            library = [furniture for furniture in library if not (isinstance(furniture, Cabinet) and furniture.price == int(parts[2]))]
        else:
            print("Неизвестный тип мебели.")
    elif parts[0] == "PRINT":
        for index, furniture in enumerate(library):
            print(f"{index}. ", end="")
            furniture.print_info()
        print(f"Всего предметов: {len(library)}")
    return library

def read_commands(file_path):
    """читалка команд из файла"""
    library = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            library = parse_command(library, line.strip())
    return library

def main():
    library = read_commands("commands.txt")
    print("Результат:")
    for index, furniture in enumerate(library):
        print(f"{index}. ", end="")
        furniture.print_info()
    print(f"Всего предметов: {len(library)}")

if __name__ == "__main__":
    main()    