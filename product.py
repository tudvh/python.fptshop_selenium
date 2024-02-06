from slugify import slugify


class Product:
    def __init__(self, url=None, brand_name=None, name=None, price=None, quantity=None, specs=None, description=None, images=None):
        self.url = url
        self.brand_name = brand_name
        self.name = name
        self.slug = None
        self.price = price
        self.quantity = quantity
        self.specs = specs
        self.description = description
        self.images = images

        if self.name:
            self.set_slug()

    def set_url(self, url):
        self.url = url

    def set_brand_name(self, brand_name):
        self.brand_name = brand_name

    def set_name(self, name):
        self.name = name
        self.set_slug()

    def set_slug(self):
        self.slug = slugify(self.name)

    def set_price(self, price):
        self.price = price

    def set_quantity(self, quantity):
        self.quantity = quantity

    def set_specs(self, specs):
        self.specs = specs

    def set_description(self, description):
        self.description = description

    def set_images(self, images):
        self.images = images

    def get_all(self):
        return {
            'url': self.url,
            'brand_name': self.brand_name,
            'name': self.name,
            'slug': self.slug,
            'price': self.price,
            'quantity': self.quantity,
            'specs': self.specs,
            'description': self.description,
            'images': self.images
        }
