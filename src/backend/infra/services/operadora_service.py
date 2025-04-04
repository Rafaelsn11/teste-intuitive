import pandas as pd
from pathlib import Path
import csv

class OperadoraService:
    def __init__(self):
        current_dir = Path(__file__).parent.parent
        csv_path = current_dir / "sql" / "datas" / "Relatorio_cadop.csv"
        try:
            self.df_operadoras = pd.read_csv(
                csv_path,
                encoding='utf-8',
                sep=';',
                quoting=csv.QUOTE_ALL,
                on_bad_lines='skip'  # Pula linhas com problemas
            )
        except FileNotFoundError:
            raise Exception(f"Arquivo CSV não encontrado em {csv_path}")
        except Exception as e:
            raise Exception(f"Erro ao carregar arquivo CSV: {str(e)}")

    def search_operadoras(self, query: str):
        # Converte a query para minúsculas para busca case insensitive.
        query_lower = query.lower()
        # Filtra os registros que contenham o texto da query na coluna "nome".
        resultados = self.df_operadoras[self.df_operadoras['Nome_Fantasia'].str.lower().str.contains(query_lower, na=False)]
        # Converte o DataFrame filtrado em uma lista de dicionários.
        return resultados.replace({pd.NA: None}).replace({float('nan'): None}).to_dict(orient='records')