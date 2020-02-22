from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import override


class Human(models.Model):
    class Gender:
        MALE = 'MALE'
        FEMALE = 'FEMALE'

    first_name = models.CharField(max_length=40, null=False, blank=False)
    last_name = models.CharField(max_length=40, null=False, blank=False)
    father_name = models.CharField(max_length=100, null=False, blank=False)
    national_id = models.CharField(max_length=10, blank=False, null=False)
    gender = models.CharField(blank=False, null=False, max_length=10)
    birth_date = models.IntegerField(blank=False, null=False, default=1)
    birth_month = models.IntegerField(blank=False, null=False, default=1)
    birth_year = models.IntegerField(blank=False, null=False, default=1370)
    parent = models.ForeignKey('Human', on_delete=models.CASCADE, default=None, null=True)
    spouse = models.ForeignKey('Human', on_delete=models.SET_DEFAULT, null=True, default=None,
                               related_name='spouse_related')

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Account(models.Model):
    class GradeType:
        PHD = 'PHD'  # دکترا
        BACHELOR = 'BACHELOR'  # کارشناسی
        MASTER = 'MASTER'  # ارشد

    class EducationalStatus:
        STUDENT = 'STUDENT'
        GRADUATED = 'GRADUATED'
        ETC = 'ETC'

    class CaravanType:
        MARRIED = 'MARRIED'
        MEN = 'MEN'
        WOMEN = 'WOMEN'

    class StateNames:
        TEHRAN = 'TEHRAN'
        ESFAHAN = 'ESFEHAN'
        SHIRAZ = 'SHIRAZ'
        ARAK = 'ARAK'
        QOM = 'QOM'
        KORDESTAN = 'KORDESTAN'
        YAZD = 'YAZD'

    user = models.OneToOneField(User, default=None, null=True, on_delete=models.CASCADE, related_name='account')
    participated_count = models.IntegerField(default=0)
    entry_year = models.IntegerField(default=98)
    grade = models.CharField(max_length=20, blank=False)
    educational_status = models.CharField(max_length=20, blank=False)
    phone_number = models.CharField(max_length=12, null=False, blank=False)
    human = models.ForeignKey(Human, default=None, null=True, on_delete=models.CASCADE, related_name='account')
    college = models.CharField(blank=False, null=False, max_length=20)
    caravan = models.CharField(max_length=20, default=None)
    return_destination = models.CharField(max_length=30, null=True, blank=True, default=StateNames.TEHRAN)
