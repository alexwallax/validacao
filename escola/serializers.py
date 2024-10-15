from rest_framework import serializers
from escola.models import Estudante,Curso, Matricula
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime


class EstudanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estudante
        fields = ['id','nome','email','cpf','data_nascimento','celular']

'''
    def validate_cpf(self,cpf):
        if len(cpf) != 11:
	        raise serializers.ValidationError('O cpf deve ter 11 digito!')
        return cpf
    
    def validate_nome(self, nome):
	    if  not nome.isalpha():
		    raise serializers.ValidationError('O nome só pode ter letras!')
	    return nome 
        
    def validate_celular(self, celular):
	    if len(celular) != 13:
		    raise serializers.ValidationError('O celular precisa ter 13 digito!')
	    return celular
'''

def validate(self, dados):
	if len(dados['cpf']) != 11:
		raise serializers.ValidationError({'cpf':'O cpf deve ter 11 digito!'})
	if  not dados['nome'].isalpha():
		raise serializers.ValidationError({'nome': 'O nome só pode ter letras!'})
	if len(dados['celular']) != 13:
		raise serializers.ValidationError({'celular': 'O celular precisa ter 13 digito!'})
	return dados

def validar_email(email):
    try:
        validate_email(email)
        return True  
    except ValidationError:
        return False  

def validar_data(data_nascimento):
    formato = "%Y-%m-%d"  
    try:
        datetime.strptime(data_nascimento, formato)
        return True 
    except ValueError:
        raise ValidationError(f"Data '{data_nascimento}' é inválida. Use o formato YYYY-MM-DD.")

     

      
class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = '__all__'

class MatriculaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matricula
        exclude = []

class ListaMatriculasEstudanteSerializer(serializers.ModelSerializer):
    curso = serializers.ReadOnlyField(source='curso.descricao')
    periodo = serializers.SerializerMethodField()
    class Meta:
        model = Matricula
        fields = ['curso','periodo']
    def get_periodo(self,obj):
        return obj.get_periodo_display()

class ListaMatriculasCursoSerializer(serializers.ModelSerializer):
    estudante_nome = serializers.ReadOnlyField(source = 'estudante.nome')
    class Meta:
        model = Matricula
        fields = ['estudante_nome']
        
        
        