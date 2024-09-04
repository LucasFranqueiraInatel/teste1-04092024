from django.db import models


class DiscountRule(models.Model):
    CONSUMER_TYPE_CHOICES = [
        ('Residencial', 'Residencial'),
        ('Comercial', 'Comercial'),
        ('Industrial', 'Industrial'),
    ]

    CONSUMPTION_RANGE_CHOICES = [
        ('<10000', 'Menor que 10.000 kWh'),
        ('10000-20000', 'Entre 10.000 e 20.000 kWh'),
        ('>20000', 'Maior que 20.000 kWh'),
    ]

    consumer_type = models.CharField("Tipo de Consumidor", max_length=20, choices=CONSUMER_TYPE_CHOICES)
    consumption_range = models.CharField("Faixa de Consumo", max_length=20, choices=CONSUMPTION_RANGE_CHOICES)
    cover_value = models.FloatField("Percentual de Cobertura")
    discount_value = models.FloatField("Valor do Desconto")

    def __str__(self):
        return f"{self.consumer_type} - {self.consumption_range} - {self.discount_value * 100}% desconto"


class Consumer(models.Model):
    name = models.CharField("Nome do Consumidor", max_length=128)
    document = models.CharField("Documento(CPF/CNPJ)", max_length=14, unique=True)
    zip_code = models.CharField("CEP", max_length=8)
    city = models.CharField("Cidade", max_length=128)
    state = models.CharField("Estado", max_length=128)
    consumption = models.IntegerField("Consumo(kWh)", blank=True, null=True)

    distributor_tax = models.FloatField("Tarifa da Distribuidora", blank=True, null=True)
    discount_rule = models.ForeignKey(DiscountRule, on_delete=models.CASCADE, related_name='consumers')

    def __str__(self):
        return self.name
