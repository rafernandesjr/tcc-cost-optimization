# TCC - Otimização de Custos em Ambientes Cloud

Este projeto foi desenvolvido como parte do **Trabalho de Conclusão do MBA em Engenharia de Software da USP/Esalq**, com o título **Otimização de Custos em Ambientes Cloud: Fatores-Chave para Redução de Gastos em Data Lakes**.  
A pesquisa avaliou diferentes fatores arquiteturais e operacionais que impactam custos e desempenho, consolidando boas práticas para o desenvolvimento em ambientes cloud-native.  
Todos os experimentos foram realizados no **Google Cloud Dataflow (Batch)**, na região **southamerica-east1 (São Paulo)**.

## 📊 Contexto
- **Desempenho**: duração total, throughput (registros/s), total de registros processados e status do job.  
- **Uso de recursos**: vCPU-horas, memória GB-horas, uso de disco, volume de shuffle e capacidade provisionada.  
- **Custos**: custo por vCPU, memória e shuffle, além do custo total e custo unitário por milhão de registros processados.  

## 🛠️ Tecnologias
- Python 3.12.9 (versão necessária para evitar problemas com o Apache Beam do Dataflow)  
- Jupyter Notebook  
- Google Cloud Platform (Dataflow, Cloud Storage, e Billing)  
- Pandas, Numpy, Matplotlib  

## 🚀 Estrutura
- `requirements.txt` → dependências necessárias para reproduzir os experimentos  
- `mbapipeline.py` → pipeline principal de execução dos testes no Dataflow  
- `generate_csv.ipynb` → geração de bases de dados sintéticos em .CSV para serem usadas nas análises  
- `t1.ipynb` a `t4.ipynb` → experimentos realizados (Serverless x Dedicado, Preemptível x Sob Demanda, Horizontal x Vertical, Normalizado x Desnormalizado)  
- `runs*.csv` → resultados das execuções com as métricas coletadas
- `analise_resultados.ipynb` → análise das métricas consolidadas  

## 📦 Como executar
1. Ter uma **conta ativa no Google Cloud Platform (GCP)**.  
2. Instalar e configurar o **Google Cloud CLI**:
    ```bash
    gcloud init
    gcloud auth application-default login
    ```
3. Criar ambiente virtual e instalar dependências:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
4. Executar os notebooks em ordem (`generate_csv.ipynb`, `t1-t4.ipynb`, `analise_resultados.ipynb`) para reproduzir os testes.  