class Product:
    def __init__(self, name, quantity, purchase_price, sale_price):
        self.name = name
        self.quantity = quantity
        self.purchase_price = purchase_price
        self.sale_price = sale_price

class Warehouse:
    def __init__(self, balance):
        self.balance = balance
        self.products = {}

    def add_product(self, product, quantity):
        if product.name in self.products:
            self.products[product.name].quantity += quantity
        else:
            self.products[product.name] = product

    def remove_product(self, product, quantity):
        if product.name in self.products and self.products[product.name].quantity >= quantity:
            self.products[product.name].quantity -= quantity
            self.balance += product.sale_price * quantity
        else:
            print("Недостатньо товару на складі")

class Invoice:
    def __init__(self, supplier, products):
        self.supplier = supplier
        self.products = products

    def process_invoice(self):
        total_amount = sum(purchase_price * quantity for product, quantity, purchase_price in self.products)
        if self.supplier.balance >= total_amount:
            self.supplier.balance -= total_amount
            return total_amount
        else:
            print("Недостатньо коштів на рахунку постачальника")
            return 0

class Supplier:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def process_payment(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        else:
            return False

class Client:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance

    def make_purchase(self, warehouse, product_name, quantity):
        if product_name in warehouse.products and warehouse.products[product_name].quantity >= quantity:
            total_price = warehouse.products[product_name].sale_price * quantity
            if self.balance >= total_price:
                self.balance -= total_price
                warehouse.remove_product(warehouse.products[product_name], quantity)
                return True
            else:
                print("Недостатньо коштів на рахунку клієнта")
        else:
            print("Недостатньо товару на складі")
        return False

# Запит у користувача даних
def input_product():
    name = input("Введіть назву продукту: ")
    quantity = int(input(f"Введіть кількість {name}: "))
    purchase_price = float(input(f"Введіть закупівельну ціну {name}: "))
    sale_price = float(input(f"Введіть ціну продажу {name}: "))
    return Product(name, quantity, purchase_price, sale_price)

def input_supplier():
    name = input("Введіть ім'я постачальника: ")
    balance = float(input(f"Введіть баланс рахунку постачальника {name}: "))
    return Supplier(name, balance)

def input_client():
    name = input("Введіть ім'я клієнта: ")
    balance = float(input(f"Введіть баланс рахунку клієнта {name}: "))
    return Client(name, balance)

def input_invoice(supplier, warehouse):
    products = []
    while True:
        product = input_product()
        warehouse.add_product(product, product.quantity)
        quantity = int(input(f"Введіть кількість {product.name} для накладної: "))
        products.append((product, quantity, product.purchase_price))
        more = input("Хочете додати ще товар? (y/n): ").lower()
        if more != 'y':
            break
    invoice = Invoice(supplier, products)
    return invoice

def main():
    # Створення складу
    warehouse = Warehouse(balance=1000)

    # Введення постачальників і клієнтів
    supplier = input_supplier()
    client = input_client()

    # Обробка накладної
    print("\nОбробка накладної постачання:")
    invoice = input_invoice(supplier, warehouse)
    total_cost = invoice.process_invoice()
    if total_cost > 0:
        print(f"\nТовари доставлені на склад. З рахунку постачальника списано {total_cost} грн.")
    else:
        print("Накладну не можна обробити. Недостатньо коштів на рахунку постачальника.")

    # Клієнт робить покупку
    print("\nКлієнт робить покупку:")
    product_name = input("Введіть назву товару для покупки: ")
    quantity = int(input(f"Введіть кількість {product_name} для покупки: "))
    purchase_successful = client.make_purchase(warehouse, product_name, quantity)
    if purchase_successful:
        print(f"Клієнт {client.name} успішно купив {quantity} одиниць {product_name}.")
    else:
        print(f"Клієнт {client.name} не зміг купити товар.")

    # Показати баланс складу та клієнта
    print(f"\nБаланс складу: {warehouse.balance} грн.")
    print(f"Баланс клієнта: {client.balance} грн.")

if __name__ == "__main__":
    main()
