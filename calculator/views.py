from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Consumer, DiscountRule
from .forms import ConsumerForm 
from calculator_python import calculator
from django.contrib import messages
import pandas as pd


def calcular_economia(request):
    consumer_type = request.GET.get('consumer_type')
    min_consumption = request.GET.get('min_consumption')
    max_consumption = request.GET.get('max_consumption')

    consumers = Consumer.objects.all()

    if consumer_type:
        consumers = consumers.filter(discount_rule__consumer_type=consumer_type)
    
    if min_consumption:
        consumers = consumers.filter(consumption__gte=min_consumption)
    
    if max_consumption:
        consumers = consumers.filter(consumption__lte=max_consumption)
    
    for consumer in consumers:
        consumption = [consumer.consumption]
        distributor_tax = consumer.distributor_tax
        tax_type = consumer.discount_rule.consumer_type

        annual_savings, monthly_savings, applied_discount, coverage = calculator(consumption, distributor_tax, tax_type)

        consumer.annual_savings = annual_savings
        consumer.monthly_savings = monthly_savings
        consumer.applied_discount = applied_discount
        consumer.coverage = coverage

    return render(request, 'calculator/list.html', {
        'consumers': consumers,
        'consumer_type': consumer_type,
        'min_consumption': min_consumption,
        'max_consumption': max_consumption,
    })

def create_consumer(request):
    if request.method == 'POST':
        form = ConsumerForm(request.POST)
        if form.is_valid():
            new_consumer = form.save(commit=False)
            new_consumer.save()
            
            return redirect('consumer_list')
    else:
        form = ConsumerForm()
    
    return render(request, 'calculator/create_consumer.html', {'form': form})

def import_consumers(request):
    if request.method == 'POST' and request.FILES['file']:
        excel_file = request.FILES['file']

        try:
            df = pd.read_excel(excel_file, engine='openpyxl')
        except Exception as e:
            messages.error(request, f"Erro ao processar o arquivo: {str(e)}")
            return redirect('consumer_list')

        for _, row in df.iterrows():
            try:
                # Tentar obter a DiscountRule correta
                discount_rule = DiscountRule.objects.get(consumer_type=row['Tipo'], cover_value=row['Cobertura(%)']/100)

                # Criar o objeto Consumer
                Consumer.objects.create(
                    name=row['Nome'],
                    document=row['Documento'],
                    city=row['Cidade'],
                    state=row['Estado'],
                    consumption=row['Consumo(kWh)'],
                    distributor_tax=row['Tarifa da Distribuidora'],
                    discount_rule=discount_rule,
                )
            except DiscountRule.DoesNotExist:
                messages.error(request, f"Erro: Não foi encontrada uma regra de desconto para o consumidor {row['Nome']} com o tipo {row['Tipo']} e cobertura {row['Cobertura(%)']}.")
            except Exception as e:
                messages.error(request, f"Erro ao importar o consumidor {row['Nome']}: {str(e)}")

        messages.success(request, "Consumidores importados com sucesso!")
        return redirect('consumer_list')

    return redirect('consumer_list')