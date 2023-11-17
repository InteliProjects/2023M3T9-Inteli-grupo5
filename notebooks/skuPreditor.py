import pandas as pd
import datetime

sku_columns = [
 'sku_encoded',
 'supplier_delivery_time',
 'has_stock_encoded',
 'sku_weight',
 'unit_price',
 'sku_length',
 'avg_website_visits_last_week',
 'sku_encoded',
 'color_encoded'
]

class Sku:

    @staticmethod
    def to_dict(df):
        sku_dict = {}

        # Agrupando por SKU e iterando sobre cada grupo
        for sku, group in df.groupby('sku_encoded'):
            # Pegando a primeira linha do grupo, já que os valores não mudam
            first_row = group.iloc[0]
            
            # Criando um subdicionário para armazenar informações que não mudam para esse SKU
            sub_dict = {}
            for col in sku_columns:
                sub_dict[col] = first_row[col]
            
            # Adicionando o subdicionário ao dicionário principal
            sku_dict[sku] = sub_dict
        return sku_dict

    @staticmethod
    def info(sku, sku_dict):
        return sku_dict.get(sku, False)


class SalesPredictor:
    
    @staticmethod
    def create_new_instance(sku, sku_dict, a_date, **kwargs):
        # Buscando informações fixas sobre o SKU
        sku_info = Sku.info(sku, sku_dict)
        
        if not sku_info:
            return None
        
        # Separa o ano, mês e dia da string a_date
        year, month, day = map(int, a_date.split('-'))
        
        # Criando o novo dicionário com informações fixas e variáveis
        instance_data = {**sku_info, **kwargs}
        
        # Transformando em um DataFrame do Pandas
        new_instance = pd.DataFrame([instance_data])

        # Separa o ano, mês e dia da string a_date
        year, month, day = map(int, a_date.split('-'))
        
        new_instance['date'] = a_date
        new_instance['date'] = pd.to_datetime(new_instance['date'], format='%Y-%m-%d')

        # Extraindo os componentes da date
        new_instance['ano'] = year
        new_instance['dia'] = day
        new_instance['dia_da_semana'] = new_instance['date'].dt.weekday
        new_instance['semana_do_ano'] = new_instance['date'].dt.isocalendar().week
        new_instance['dia_do_ano'] = new_instance['date'].dt.dayofyear
                
        new_instance['sku_encoded'] = sku

        return new_instance


    # @staticmethod
    # def create_new_instance(sku_dict, a_date, **kwargs):
    #     # Buscando informações fixas sobre o SKU
    #     sku_info = Sku.info(sku_dict['sku_encoded'], sku_dict)
        
    #     if not sku_info:
    #         return None
        
    #     # Criando o novo dicionário com informações fixas e variáveis
    #     instance_data = {**sku_info, **kwargs}
    
    #     # Transformando em um DataFrame do Pandas
    #     new_instance = pd.DataFrame([instance_data])

    #     # Separa o ano, mês e dia da string a_date
    #     year, month, day = map(int, a_date.split('-'))
        
    #     new_instance['date'] = a_date
    #     new_instance['date'] = pd.to_datetime(new_instance['date'], format='%Y-%m-%d')

    #     # Extraindo os componentes da date
    #     new_instance['ano'] = year
    #     new_instance['dia'] = day
    #     new_instance['dia_da_semana'] = new_instance['date'].dt.weekday
    #     new_instance['semana_do_ano'] = new_instance['date'].dt.isocalendar().week
    #     new_instance['dia_do_ano'] = new_instance['date'].dt.dayofyear
        
    #     return new_instance
