class Car:
    def __init__(self, brand, name, price, year, damage, last_seen, image, id=None):
        self.image = image
        self.last_seen = last_seen
        self.damage = damage
        self.year = year
        self.price = price
        self.name = name
        self.brand = brand
        self.id = id

    def to_dict(self):
        return {
            'brand': self.brand,
            'name': self.name,
            'price': self.price,
            'year': self.year,
            'damage': self.damage,
            'last_seen': self.last_seen,
            'id': self.id,
            'image': self.image
        }
