### 1 - Visão geral

<hr />

Utilizar a MLP para fazer a previsão de uma das variáveis meteorológicas a partir dos dados provenientes das estações mantidas pelo Instituto Nacional de Meteorologia (INMET). Utilizar o script disponível em [https://github.com/AdrianoPereira/cap421homework0203/blob/main/helpers/download_station_data/inmet_downloader.py](https://github.com/AdrianoPereira/cap421homework0203/blob/main/helpers/download_station_data/inmet_downloader.py) para baixar todos os dados das estações convencionais entre 01 de janeiro de 2000 a 31 de dezembro de 2021. 

### 2 - Dados

<hr />

O [Portal do INNET](https://portal.inmet.gov.br) possui diversos dados, que incluem: imagens de satélite, radar, saídas de modelos numéricos e estações meteorológicas. Nesta proposta, pretende-se utilizar os dados das estações meteorológicas, que possuem uma boa cobertura no território brasileiro, conforme mostrado na Figura [1](#cfig01).

<p id="cfig01">
<img src="https://raw.githubusercontent.com/AdrianoPereira/CAP421/main/cap421homework0203/homework03/images/stations_inmet.png" title="Estações meteorológicas do INMET" style="width: 100%;"/>
<span style="display: block; text-align: center;"><strong>Figura 1</strong>: Estações meteorológicas INMET.</span>
</p>

A sugestão de utilizar as estações convencionais se dá pelo fato de que, o período de dados das estações convencionais é maior e também, várias estações automáticas posseum *flags* que indicam inoperância ou problema com os dados, veja alguns exemplos na Figura [2](#cfig02). O período delimitado foi escolhido arbitrariamente, acreditando que 20 anos seja o bastante para ter um conjunto de dados suficiente para treinar um modelo de *deep learning*.

<p id="cfig02">
<img src="https://raw.githubusercontent.com/AdrianoPereira/CAP421/main/cap421homework0203/homework03/images/conventional_stations_available.png" title="Estações meteorológicas do INMET" style="width: 100%;"/>
<span style="display: block; text-align: center;"><strong>Figura 2</strong>: Informaçoes de algumas estações meteorológicas automáticas.</span>
</p>

Os dados das estações convencionais do INMET são registrados três vezes por dia nos horários 00:00h, 12:00h e 18:00h. Cada registro possui 19 atributos, sendo 12  variáveis meteorológicas e o restante são informações a respeito da estação. O bloco abaixo mostra um exmeplo com todos os dados de um registro.

```json
[
    {
        "UMID_MED": "96.25",
        "DT_MEDICAO": "2000-05-17",
        "DC_NOME": "ITAITUBA",
        "UMID_HORA": "91",
        "TEMP_HORA": "27.6",
        "INSO_HORA": "1.5",
        "NEBU_HORA": "9",
        "TEMP_MED": "24.54",
        "CHUVA": null,
        "VENT_VEL": "0",
        "VL_LATITUDE": "-4.276986",
        "TEMP_MIN": null,
        "TEMP_MAX": "27.6",
        "UF": "PA",
        "PRESS_EST": "1007",
        "VENT_DIR": "0",
        "CD_ESTACAO": "82445",
        "VL_LONGITUDE": "-55.993087",
        "HR_MEDICAO": "0000"
    },
    {
        "UMID_MED": null,
        "DT_MEDICAO": "2000-05-17",
        "DC_NOME": "ITAITUBA",
        "UMID_HORA": "98",
        "TEMP_HORA": "23.8",
        "INSO_HORA": null,
        "NEBU_HORA": "10",
        "TEMP_MED": null,
        "CHUVA": "28.1",
        "VENT_VEL": "0",
        "VL_LATITUDE": "-4.276986",
        "TEMP_MIN": "22.1",
        "TEMP_MAX": null,
        "UF": "PA",
        "PRESS_EST": "1010.2",
        "VENT_DIR": "0",
        "CD_ESTACAO": "82445",
        "VL_LONGITUDE": "-55.993087",
        "HR_MEDICAO": "1200"
    },
    {
        "UMID_MED": null,
        "DT_MEDICAO": "2000-05-17",
        "DC_NOME": "ITAITUBA",
        "UMID_HORA": "93",
        "TEMP_HORA": "24.6",
        "INSO_HORA": null,
        "NEBU_HORA": "10",
        "TEMP_MED": null,
        "CHUVA": null,
        "VENT_VEL": "0",
        "VL_LATITUDE": "-4.276986",
        "TEMP_MIN": null,
        "TEMP_MAX": null,
        "UF": "PA",
        "PRESS_EST": "1008.3",
        "VENT_DIR": "0",
        "CD_ESTACAO": "82445",
        "VL_LONGITUDE": "-55.993087",
        "HR_MEDICAO": "1800"
    }
]
```

Descrição dos atributos, de acordo com a [documentação da API](https://portal.inmet.gov.br/manual/manual-de-uso-da-api-esta%C3%A7%C3%B5es):
* `UMID_MED`: Umidade relativa do ar, medida em %.
* `DT_MEDICAO`: Data da medição no formato YYYY-MM-DD.
* `DC_NOME`: Nome do município onde a estação está localizada.
* `UMID_HORA`: Umidade relativa do ar, medida em %.
* `TEMP_HORA`: Temperatura, medida em °C.
* `INSO_HORA`: Descrição não encontrada.
* `NEBU_HORA`: Descrição não encontrada.
* `TEMP_MED`: Temperatura média, medida em °C.
* `CHUVA`: Precipitação total, medida em mm.
* `VENT_VEL`: Velocidade do vento. Medido em m/s.
* `VL_LATITUDE`: Latitude da localização da estação.
* `TEMP_MIN`: Temperatura mínima, medida em °C.
* `TEMP_MAX`: Temperatura máxima, medida em °C.
* `UF`: Sigla do município onde a estação está localizada.
* `PRESS_EST`: Pressão atmosférica em mB.
* `VENT_DIR`: Direção do vento em °.
* `CD_ESTACAO`: Identificador da estação.
* `VL_LONGITUDE`: Longitude da localização da estação.
* `HR_MEDICAO`: Hora em que a medição foi feita.

#### 2.2 - Baixar dados

Para baixar os dados pode ser utilizado o script disponível em: `inmet_downloader.py`. Uma das formas para baixar os dados utilizando o script, está descrita a seguir.

**Baixar repositório**
```console
git clone https://github.com/AdrianoPereira/cap421homework0203.git && cd cap421homework0203
```

**Instalar dependências**
```console
pip install -r requirementes.txt
```

**Baixar dados de uma estação**
```console
python helpers/download_station_data/inmet_downloader.py --start <data inicial> --end <data final> --munic <município> --state <estado> --stid <id da estação> 
```
* `<data inicial>`: Data inicial no formato YYYY-MM-DD (Ex: `2020-10-03`).
* `<data inicial>`: Data final no formato YYYY-MM-DD (Ex: `2020-10-04`).
* `<município>`: Munícipio onde a estação está localizada (Ex. `ITAITUBA`).
* `<estado>`: Sigla do estado onde a estação está localizada (Ex. PA).
* `<id da estação>`: Identificador da estação (Ex. `82445`).

### 3 Metodologia
<hr />

A seguir, algumas ideis para aplicar a DNN:
* **Ideia 01**: Para cada estação, utilizar todas as variáveis para prever uma a temperatura média diária.

* **Ideia 02**: Para cada estação, utilizar todas as variáveis para prever uma o acumulado de chuva diário.

* **Ideia 03**: Para cada estação, utilizar todas as variáveis para prever o acumulado de chuva mensal.

* **Ideia 04**: Para cada estação, utilizar os dados dos dois primeiros horários para prever as variáveis do terceiro horário.

* **Ideia 05**: Criar classes do acumulado de chuva diário e aplicar a DNN para classificação.

* **Ideia 06**: Criar classes do acumulado de chuva mensal e aplicar a DNN para classificação.

...
