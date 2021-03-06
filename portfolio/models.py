from django.db import models
from django.utils import timezone
from django.db import models
from django.utils import timezone
import requests


# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=200)
    cust_number = models.IntegerField(blank=False, null=False)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    cell_phone = models.CharField(max_length=50)
    created_date = models.DateTimeField(
        default=timezone.now)
    updated_date = models.DateTimeField(auto_now_add=True)

    def created(self):
        self.created_date = timezone.now()
        self.save()

    def updated(self):
        self.updated_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.cust_number)


class Investment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='investments')
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    acquired_value = models.DecimalField(max_digits=10, decimal_places=2)
    acquired_date = models.DateField(default=timezone.now)
    recent_value = models.DecimalField(max_digits=10, decimal_places=2)
    recent_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.acquired_date = timezone.now()
        self.save()

    def updated(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def results_by_investment(self):
        return float(self.recent_value) - float(self.acquired_value)


class Stock(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    shares = models.DecimalField(max_digits=10, decimal_places=1)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateField(default=timezone.now, blank=True, null=True)

    def created(self):
        self.recent_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.customer)

    def initial_stock_value(self):
        return float(self.shares) * float(self.purchase_price)

    def current_stock_price(self):
        symbol_f = str(self.symbol)
        main_api = 'https://www.alphavantage.co/query?function=BATCH_STOCK_QUOTES&symbols='
        api_key = '&apikey= 20GSDX4W5D1GVBGT'
        url = main_api + symbol_f + api_key
        json_data = requests.get(url).json()
        open_price = float(json_data["Stock Quotes"][0]["2. price"])
        share_value = open_price
        return share_value

    def current_stock_value(self):
        return float(self.current_stock_price()) * float(self.shares)

    def results_by_stock(self):
        return self.current_stock_value() - float(self.initial_stock_value())


class Currency(models.Model):
    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)
    from_number = models.DecimalField(decimal_places=2, max_digits=8)
    rate = models.DecimalField()

    def rate(self):
        from_symbol = str(self.from_currency)
        to_symbol = str(self.to_currency)
        main_api = 'https://free.currconv.com/api/v7/convert?q='
        combined_symbol = from_symbol + '_' + to_symbol
        api_key = '&compact=ultra&apiKey=672e844f6f7acb1e8217'
        url = main_api + combined_symbol + api_key
        json_data = requests.get(url).json()
        rate = float(json_data[combined_symbol])
        return rate

    def to_number(self):
        to_number = float(self.from_number) * float(self.rate())
        return to_number



