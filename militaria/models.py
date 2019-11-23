from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=20)
    how_many = models.IntegerField()
    priority = models.IntegerField(default=2, choices=[(1, "1"), (2, "2"), (3, "3")])
    min = models.IntegerField(default=70)
    max = models.IntegerField(default=90)
    user = models.ManyToManyField('auth.User')
    weight = models.IntegerField(default=3, choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")])

    def __str__(self):
        return "{} {}".format(self.name, self.how_many)

    def substraction_from_percent_value(self, value: int):
        self.how_many = self.how_many - value

    def get_warehouse_fill_code(self):
        if self.how_many >= self.min:
            if self.how_many < self.max:
                return '#fffab7'    # orange
            else:
                return '#99dcbb'    # green
        else:
            return '#ff153c'       # red

