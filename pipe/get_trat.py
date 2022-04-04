import pandas as pd
import numpy as np


class Tabelas:

    colunas = ['CompanySize', 'OperatingSystem', 'Country', 'CommunicationTools', 'LanguageWorkedWith']

    def __init__(self,  data):

        # lista com arrays das colunas originais
        self.tabelas = [data[col].unique() for col in self.colunas]

        # criacao dos dataframes com relacao one_to_one com respondente
        self.empresa = self.id_name_df(self.tabelas[0]).rename(columns={'nome': 'tamanho'})
        self.sistema_operacional = self.id_name_df(self.tabelas[1])
        self.pais = self.id_name_df(self.tabelas[2])

        # criacao do dataframe principal
        self.respondente = self.resp_tab(data)

        # criacao dos dataframes com relacao many_to_many com respondente
        data = data.rename(columns= {'LanguageWorkedWith': 'linguagem_programacao',
                                     'CommunicationTools': 'ferramenta_comunic'})
        self.linguagem_programacao, self.resp_usa_linguagem = self.sep_lista(data[['Respondent', 'linguagem_programacao']])
        self.ferramenta_comunic, self.resp_usa_ferramenta = self.sep_lista(data[['Respondent', 'ferramenta_comunic']])



    def resp_tab(self, data):

        df = data[['Respondent', 'OpenSource', 'CompanySize',
                   'OperatingSystem', 'Country', 'Hobby', 'ConvertedSalary']]


        df.loc[df['CompanySize'].isna(), 'CompanySize'] = 'Not informed'
        df = df.merge(self.empresa,
                      how='left',
                      left_on='CompanySize',
                      right_on='tamanho').rename(columns={'id': 'empresa_id'}).drop(columns=['CompanySize',
                                                                                             'tamanho'])

        df.loc[df['Country'].isna(), 'Country'] = 'Not informed'
        df = df.merge(self.pais,
                      how='left',
                      left_on='Country',
                      right_on='nome').rename(columns={'id': 'pais_id'}).drop(columns=['Country',
                                                                                       'nome'])

        df.loc[df['OperatingSystem'].isna(), 'OperatingSystem'] = 'Not informed'
        df = df.merge(self.sistema_operacional,
                      how='left',
                      left_on='OperatingSystem',
                      right_on='nome').rename(columns={'id': 'sistema_operaciona_id'}).drop(columns=['OperatingSystem',
                                                                                                     'nome'])


        df = df.rename(columns={'Respondent': 'respondente',
                                'OpenSource': 'contrib_open_source',
                                'Hobby': 'programa_hobby',
                                'ConvertedSalary': 'salario'})

        # df.columns = ['id', 'contrib_open_source', 'programa_hobby', 'salario']
        df.contrib_open_source = pd.get_dummies(df.contrib_open_source, drop_first=True)
        df.programa_hobby = pd.get_dummies(df.programa_hobby, drop_first=True)

        df.salario = df.salario.fillna(0)
        salar_mes = (lambda x: (x/12) * 3.81)
        df.salario = df.salario.apply(salar_mes)

        df = df.reset_index().rename(columns={'index': 'id'})
        return df


    def sep_lista(self, coluna):
        atts_list = []
        df_keys = pd.DataFrame({'respondente': [], 'itens': []})
        coluna = coluna.fillna('Not informed')
        for id, items in coluna.to_numpy():
            lista = items.split(';')
            parcial = pd.DataFrame({'respondente': id, 'itens': lista})
            df_keys = pd.concat((df_keys, parcial))
            for item in lista:
                if item not in atts_list:
                    atts_list.append(item)

        df = self.id_name_df(np.array(atts_list))
        df_cx = df_keys.merge(df,
                           right_on='nome',
                           left_on='itens',
                           how='left').rename(columns={'id': f'{coluna.columns[1]}_id'}).drop(columns=['nome', 'itens'])

        df_cx = df_cx.merge(self.respondente, how='left', on='respondente').rename(columns={'id': 'respondente_id'})
        df_cx = df_cx[['respondente_id', f'{coluna.columns[1]}_id']]

        return df, df_cx


    def id_name_df(self, lista):
        df = pd.DataFrame(lista, columns=['nome']).fillna('Not informed')
        id_name = df.reset_index().rename(columns={'index': 'id'})
        return id_name


    def dfs(self):
        lista = [('respondente', self.respondente),
                 ('empresa', self.empresa), ('sistema_operacional', self.sistema_operacional), ('pais', self.pais),
                 ('ferramenta_comunic', self.ferramenta_comunic), ('resp_usa_ferramenta', self.resp_usa_ferramenta),
                 ('linguagem_programacao', self.linguagem_programacao), ('resp_usa_linguagem', self.resp_usa_linguagem)]

        return lista




if __name__ == '__main__':
    df = pd.read_csv('base_de_respostas_10k_amostra.csv')

    tabelas = Tabelas(df)
    lista = tabelas.dfs()


    spot=213
