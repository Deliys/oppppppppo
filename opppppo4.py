import unittest
import io
import sys

class TestParseCommand(unittest.TestCase):

    def setUp(self):#начинаем жить с чистого листа
        self.library = []

    def test_add_table(self):#добавлем нормальный столик
        command = "ADD TABLE 1000 IKEA Дерево Квадрат"
        self.library = parse_command(self.library, command)
        self.assertEqual(len(self.library), 1)
        self.assertIsInstance(self.library[0], Table)
        self.assertEqual(self.library[0].price, 1000)
        self.assertEqual(self.library[0].manufacturer, "IKEA")
        self.assertEqual(self.library[0].material, "Дерево")
        self.assertEqual(self.library[0].shape, "Квадрат")

    def test_add_chair(self):
        command = "ADD CHAIR 500 IKEA Plastic TRUE"#добавлем нормальный стул
        self.library = parse_command(self.library, command)
        self.assertEqual(len(self.library), 1)
        self.assertIsInstance(self.library[0], Chair)
        self.assertEqual(self.library[0].price, 500)
        self.assertEqual(self.library[0].manufacturer, "IKEA")
        self.assertEqual(self.library[0].material, "Plastic")
        self.assertTrue(self.library[0].adjustable_height)

    def test_add_cabinet(self):
        command = "ADD CABINET 1500 IKEA 5 Wood"
        self.library = parse_command(self.library, command)
        self.assertEqual(len(self.library), 1)
        self.assertIsInstance(self.library[0], Cabinet)
        self.assertEqual(self.library[0].price, 1500)
        self.assertEqual(self.library[0].manufacturer, "IKEA")
        self.assertEqual(self.library[0].material, "Wood")
        self.assertEqual(self.library[0].num_shelves, 5)

    def test_remove_table(self):#проверка удаления
        self.library.append(Table(1000, "IKEA", "Wood", "Round"))
        command = "REM TABLE 1000"
        self.library = parse_command(self.library, command)
        self.assertEqual(len(self.library), 0)

    def test_remove_nonexistent_table(self):#проверка удаления обхекта которого нет
        self.library.append(Table(1000, "IKEA", "Wood", "Round"))
        command = "REM TABLE 2000"  
        self.library = parse_command(self.library, command)
        self.assertEqual(len(self.library), 1)


    def test_print_command(self):#тест вывода
        self.library.append(Table(1000, "IKEA", "Wood", "Round"))
        command = "PRINT"
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        self.library = parse_command(self.library, command)
        sys.stdout = sys.__stdout__
        self.assertEqual(len(self.library), 1)
        self.assertIn("Стол", capturedOutput.getvalue())
        self.assertIn("Всего предметов: 1", capturedOutput.getvalue())



    def test_unknown_type(self):#неизвестный тип мебели
        command = "ADD DESK 800 IKEA Wood"
        capturedOutput = io.StringIO()
        sys.stdout = capturedOutput
        result = parse_command(self.library, command)
        sys.stdout = sys.__stdout__
        self.assertEqual(capturedOutput.getvalue(), "Неизвестный тип мебели.\n")
        
    def test_literr_in_price(self):#тест на буквы в цене .их не должно быть 
        command = "ADD CHAIR уац IKEA Plastic TRUE"
        print(parse_command(self.library, command))
        self.assertIn("ne int", parse_command(self.library, command))
        


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
        if parts[2].isnumeric() == False:
            return "ne int"   
        if parts[1] == "TABLE":
            library.append(Table(int(parts[2]), parts[3], parts[4], parts[5]))
        elif parts[1] == "CHAIR":
            library.append(Chair(int(parts[2]), parts[3], parts[4], parts[5] == "TRUE"))
        elif parts[1] == "CABINET":
            library.append(Cabinet(int(parts[2]), parts[3], int(parts[4]), parts[5]))
        else:
            print("Неизвестный тип мебели.")
            return "Неизвестный тип мебели."
    elif parts[0] == "REM":
        if parts[1] == "TABLE":
            library = [furniture for furniture in library if not (isinstance(furniture, Table) and furniture.price == int(parts[2]))]
        elif parts[1] == "CHAIR":
            library = [furniture for furniture in library if not (isinstance(furniture, Chair) and furniture.price == int(parts[2]))]
        elif parts[1] == "CABINET":
            library = [furniture for furniture in library if not (isinstance(furniture, Cabinet) and furniture.price == int(parts[2]))]
        else:
            print("Неизвестный тип мебели.")
            return "Неизвестный тип мебели."
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
    unittest.main()
    main()    
