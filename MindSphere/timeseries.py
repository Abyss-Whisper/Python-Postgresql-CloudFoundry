from config import MindSphere
import json
import datetime
import pandas as pd

mindsphere = MindSphere(app_Name="cardapiodigita20",
                        app_Version="v1.0.0",
                        tenant="debr2",
                        gateway_URL="https://gateway.eu1.mindsphere.io/" ,
                        client_ID="debr2-cardapiodigita20-v1.0.0",
                        client_Secret="KhMlcZVzS8YlfvfuCPDSdENRCEE6gvSaFTadq90kVZ9"
                        )

assetId = "31fd2a70282b44dfa2e27c3b1fc6c4eb" #insira aqui o assetID do seu asset
aspectName = "varPython" #insira aqui o aspectName do seu asset
fromDateTime = "2023-07-19T00:00:00Z" #de
toDateTime = "2023-10-16T10:00:00Z"#até

#print(mindsphere.getBearerToken()) #printa o token

#print(mindsphere.getTimeSeries(assetId,aspectName,fromDateTime,toDateTime)) #printa a requisição GET, de acordo com o asset e com o Aspect

print(mindsphere.getTimeSeries(assetId,aspectName,"","")) #retorna o último timestamp disponível

now = datetime.datetime.now() #tempo atual
print(mindsphere.putTimeSeriesData(assetId,aspectName,{"_time":now,"velo":"100", "temp":"100"})) #utiliza o PUT para colcoar TimeSeries