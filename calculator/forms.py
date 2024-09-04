import re
from django import forms
from .models import Consumer

class ConsumerForm(forms.ModelForm):
    class Meta:
        model = Consumer
        fields = ['name', 'document', 'zip_code', 'city', 'state', 'consumption', 'distributor_tax', 'discount_rule']

    def clean_document(self):
        document = self.cleaned_data['document']
        document = re.sub(r'\D', '', document)

        if len(document) == 11 and self.is_valid_cpf(document):
            return document
        elif len(document) == 14 and self.is_valid_cnpj(document):
            return document
        else:
            raise forms.ValidationError("Documento inválido. Insira um CPF ou CNPJ válido.")

    def is_valid_cpf(self, cpf):    
        """
        Função para validar CPF
        """
        
        return True

    def is_valid_cnpj(self, cnpj):
        """
        Função para validar CNPJ
        """
        
        return True 
