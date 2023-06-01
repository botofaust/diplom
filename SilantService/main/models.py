import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q


class ReferenceTable(models.Model):
    TYPES = (
        ('MM', 'Machine Model'),
        ('EM', 'Engine Model'),
        ('TM', 'Transmission Model'),
        ('DM', 'Driving Bridge Model'),
        ('CM', 'Controlled Bridge Model'),
        ('MT', 'Maintenance Type'),
        ('FT', 'Failure Type'),
        ('RT', 'Repair Type'),
        ('SC', 'Service Company'),
    )
    type = models.CharField(max_length=2, choices=TYPES)
    title = models.TextField(default='', max_length=100)
    description = models.TextField(default='')

    def __str__(self):
        return f'{self.type}: {self.title}'

    @staticmethod
    def get_component_qfilter():
        return Q(type='EM') | Q(type='TM') | Q(type='DM') | Q(type='CM')


class Machine(models.Model):
    model = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'MM'},
        on_delete=models.CASCADE,
        related_name='machine_model',
    )
    model_serial = models.TextField(default='', max_length=100, unique=True)

    engine = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'EM'},
        on_delete=models.CASCADE,
        related_name='machine_engine',
    )
    engine_serial = models.TextField(default='', max_length=100, unique=True)

    transmission = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'TM'},
        on_delete=models.CASCADE,
        related_name='machine_transmission'
    )
    transmission_serial = models.TextField(default='', max_length=100, unique=True)

    driving_bridge = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'DM'},
        on_delete=models.CASCADE,
        related_name='machine_driving_bridge'
    )
    driving_bridge_serial = models.TextField(default='', max_length=100, unique=True)

    controlled_bridge = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'CM'},
        on_delete=models.CASCADE,
        related_name='machine_controlled_bridge'
    )
    controlled_bridge_serial = models.TextField(default='', max_length=100, unique=True)

    contract = models.TextField(default='', max_length=100, unique=True)
    shipment_date = models.DateField(auto_now_add=True)
    counteragent = models.TextField(default='')
    shipment_address = models.TextField(default='')
    equipment = models.TextField(default='')
    client_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='machine_client_user',
    )
    service_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='machine_service_user',
    )

    def __str__(self):
        return f'{self.model}: {self.model_serial}'


class Maintenance(models.Model):
    type = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'MT'},
        on_delete=models.CASCADE,
        related_name='maintenance_type',
    )
    date = models.DateField(auto_now_add=True)
    operating_time = models.IntegerField(default=0)
    order_number = models.TextField(default='')
    order_date = models.DateField()
    service_company = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'SC'},
        on_delete=models.CASCADE,
        related_name='maintenance_service_company'
    )
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    service = models.ForeignKey(User, on_delete=models.CASCADE)


class Reclamation(models.Model):
    failure_date = models.DateTimeField(auto_now_add=True)
    operating_time = models.IntegerField(default=0)
    failure_component = models.ForeignKey(
        ReferenceTable,
        limit_choices_to=ReferenceTable.get_component_qfilter,
        on_delete=models.CASCADE,
        related_name='reclamation_failure_component',
    )
    failure_description = models.TextField(default='')
    repair_type = models.ForeignKey(
        ReferenceTable,
        limit_choices_to={'type': 'RT'},
        on_delete=models.CASCADE,
        related_name='reclamation_repair_type'
    )
    used_consumables = models.TextField(default='')
    repair_date = models.DateTimeField()
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    service_user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def downtime(self):
        return self.repair_date.date() - self.failure_date.date()

    def __str__(self):
        return f'{self.downtime}'
