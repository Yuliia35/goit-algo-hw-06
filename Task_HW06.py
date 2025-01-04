from collections import UserDict
import re

class Field: #Базовий клас для полів запису
    pass 

class Name(Field): #Клас для зберігання імені контакту. Обов'язкове поле
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty.")
        self.value = value

class Phone(Field): #Клас для зберігання номера телефону з перевіркою формату
    def __init__(self, value):
        if not self.validate(value):
            raise ValueError("Phone number must be 10 digits long.")
        self.value = value

    @staticmethod
    def validate(value): #Перевірка формату номера телефону
        return bool(re.fullmatch(r'^\d{10}$', value))

class Record: #Клас для зберігання контактної інформації
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone_number): #Додавання телефону до запису
        phone = Phone(phone_number)
        self.phones.append(phone)

    def remove_phone(self, phone_number): #Видалення телефону із запису
        self.phones = [phone for phone in self.phones if phone.value != phone_number]

    def edit_phone(self, old_number, new_number): #Редагувати існуючий номер телефону
        for phone in self.phones:
            if phone.value == old_number:
                if not Phone.validate(new_number):
                    raise ValueError("New phone number must be 10 digits long.")
                phone.value = new_number
                return
        raise ValueError("Old phone number not found.")

    def find_phone(self, phone_number): #Пошук контакту за номером телефону
        """#Пошук об'єкта Телефон за номером."""
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

class AddressBook(UserDict): #Клас для зберігання та керування записами
    def add_record(self, record): #Додати запис до адресної книги
        self.data[record.name.value] = record

    def find(self, name): #Знайдіть запис за назвою
        return self.data.get(name)

    def delete(self, name): #Видалити запис за назвою
        if name in self.data:
            del self.data[name]

    def __str__(self): #Гарне рядкове представлення адресної книги)
        result = "Address Book:\n"
        for name, record in self.data.items():
            phone_numbers = ', '.join(phone.value for phone in record.phones)
            result += f"Name: {name}, Phones: [{phone_numbers}]\n"
        return result.strip()

# Example usage:
if __name__ == "__main__":
    book = AddressBook()

    # Створення запису для John
    record1 = Record("John")
    record1.add_phone("1234567890")
    record1.add_phone("5555555555")
    
    # Створення та додавання нового запису для Jane
    record2 = Record("Jane")
    record2.add_phone("9876543210")

    # Додавання записів до адресної книги
    book.add_record(record1)
    book.add_record(record2)

    # Виведення всіх записів у книзі
    print(book)

    # Пошук запису для John
    found_record = book.find("John")
    if found_record:
        print("+ Found John's record.")
    else:
        print("- John's record not found.")

    # Редагування номера телефону
    try:
        found_record.edit_phone("1234567890", "1111111111")
        print("Updated John's phone number.")
    except ValueError as e:
        print(f"Error: {e}")

    # Видалення запису Jane
    book.delete("Jane")
    print("Deleted Jane's record.")

    # Виведення всіх записів у книзі
    print(book)
