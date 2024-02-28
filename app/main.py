from datetime import datetime
import requests

class address:
    def __init__ (self, street: str, city: str, state: str, zip: str):
        self.street: str = street
        self.city: str = city
        self.state: str = state
        self.zip: str = zip

    def __str__ (self):
        return self.street + '\n' + self.city + ' ' + self.state + ' ' + self.zip

class Product:
    def __init__ (self, sku: int):
        self.sku: str = int
        self.department: str = None
        self.category: str = None
        self.brand: str = None
        self.name: str = None
        self.retail_price: float = None
        self.sale_price: float = None

        api_url = f'http://localhost:8000/api/products/{sku}'

        try:
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            self.department = data['DEPARTMENT']
            self.category = data['CATEGORY']
            self.brand = data['BRAND']
            self.name = data['NAME']
            self.retail_price = float(data['RETAIL_PRICE'])
            self.sale_price = float(data['SALE_PRICE'])

        except requests.exceptions.RequestException as e:
            print(f'Error fetching product data: {e}')

    def __str__(self):
        return f"UPC: {self.sku} | Name: {self.name} | Description: {self.description} | Price: ${self.retail_price:.2f}"

class order_item:
    def __init__ (self, item: Product):
        self.item: Product = item
        self.quantity: int = 1
        self.total: float = self.__calc_total()

    def increment (self):
        self.quantity = self.quantity + 1
        self.total = self.__calc_total()

    def decrement (self):
        if self.quantity != 0:
            self.quantity = self.quantity - 1
        self.total = self.__calc_total()

    def set_quantity (self, qty):
        if qty >= 0:
            self.quantity = qty
        self.total = self.__calc_total()

    def __calc_total (self) -> float:
        return self.item.sale_price * self.quantity

    def __str__ (self):
        return self.item.name + '\t' + str(self.quantity) + ' @ ' + str(self.item.sale_price) + '     ' + str(self.total)

class Order:
    def __init__ (self, id:int, online:bool, items: list[order_item] = None):
        self.id: int = id
        self.member_id: int
        self.online: bool = online
        self.order_status: str = 'Pending'
        self.order_date: datetime = datetime.now()
        self.order_items: list[order_item] = items
        self.payment_method: str
        self.order_subtotal: float = self.__calc_subtotal()
        self.order_total: float = self.__calc_total()

    def add_item (self, item: Product):
        new_item = order_item(item)
        if self.order_items is None:
            self.order_items = [new_item]
        if new_item.item.sku in [x.item.sku for x in self.order_items]:
            for y in self.order_items:
                if new_item.item.sku == y.item.sku:
                    y.increment()
        else:
            self.order_items.append(order_item(item))

    def __cleanup_items (self):
        for i, item in enumerate(self.order_items):
            if item.quantity <= 0:
                self.order_items.pop(i)
        self.order_subtotal = self.__calc_subtotal()
        self.order_total = self.__calc_total()

    def __calc_subtotal (self) -> float:
        order_total = 0.0
        for item in self.order_items:
            order_total = order_total + item.total
        return order_total

    def __calc_total (self) -> float:
        return self.order_subtotal * 1.0975

    def __str__ (self):
        self.__cleanup_items()
        return 'Order#' + str(self.id) + '\n' + self.order_date.strftime('%m/%d/%y %I:%M %p') + '\n' + '\n' + '\n'.join(f'{item}' for item in self.order_items) + '\n\n' + 'Subtotal\n$' + str(round(self.order_subtotal, 2)) + '\nTotal\n$' + str(round(self.order_total, 2))

class member:
    def __init__ (self, id: int, fname: str, lname: str, address: address, phone: str, email: str):
        self.id: int = id
        self.first_name: str = fname
        self.last_name: str = lname
        self.address: str = address
        self.phone_number: str = phone
        self.email:str = email

    def __str__ (self):
        return 'Member#' + str(self.id) + '\n' + self.first_name + ' ' + self.last_name + '\n' + str(self.address) + '\n' + self.phone_number + '\n' + self.email

def main():
    order = Order(1, False, [])
    scanned_barcode = input('sku: ')
    scanned_barcode = int(scanned_barcode)
    products = {}
    if scanned_barcode not in products:
        products[scanned_barcode] = Product(scanned_barcode)
    order.add_item(products[scanned_barcode])
    print(order)

if __name__=='__main__':
    main()