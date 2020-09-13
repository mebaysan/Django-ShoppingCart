from decimal import Decimal
from django.conf import settings
from cart.models import Product


class Cart:
    def __init__(self, request):
        """
        Cart objesi oluşturulurken.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)  # settings.py içerisinde oluşturduğumuz cart id'e erişiyoruz
        if not cart:  # eğer session'da ilgili id'de bir cart objesi yok ise
            # session'a boş bir alışveriş sepeti oluşturuyoruz
            cart = self.session[
                settings.CART_SESSION_ID] = {}  # session'da boş bir cart nesnesi tanımlıyoruz. Key'i 'cart' olacak çünkü settings.py içerisinde ID olarak 'cart' stringini set ettik
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
       Sepete ürün ekliyoruz, eğer ürün zaten ekli ise miktarını artırıyoruz
        """

        product_id = str(product.id)  # eğer slug vb üzerinden gidecekseniz burayı değiştirebilirsiniz
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # işlem yaptığımızı belirtmek için session'u değiştirldi olarak set ediyoruz. Bu Django'ya session'un değiştiğini ve kaydedilmesi gerektiğini söyler.
        self.session.modified = True

    def remove(self, product):
        """
        Sepetten ürün siliyoruz
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def __iter__(self):
        """
        Sepetteki ürünlerin bilgilerini veritabanından getirebiliriz.
        Bunu şu şekilde düşünelim bu fonksiyon
                    for item in cart
        yapılınca çalışacak fonksiyon
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Sepetteki ürün adedini alalım
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Sepet toplam tutarını verir
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_total_items(self):
        """
        Sepet toplam ürün adedini verir
        """
        return sum(item['quantity'] for item in self.cart.values())

    def clear(self):
        # sepeti session'dan silelim
        del self.session[settings.CART_SESSION_ID]
        self.save()
