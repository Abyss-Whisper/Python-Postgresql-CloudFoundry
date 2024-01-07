import json,base64,requests,datetime
class MindSphere():
    def __init__(self,app_Name:str,app_Version:str,tenant:str,gateway_URL:str,client_ID:str,client_Secret:str) -> None:
        self.app_Name = app_Name
        self.app_Version = app_Version
        self.tenant = tenant
        self.gateway_URL = gateway_URL
        self.client_ID = client_ID
        self.client_Secret = client_Secret

    #pegar o token
    def getToken(self):
        if("" in [self.client_ID,self.client_Secret]):
            print("Please set your credentials")
            return False
        secret = (base64.b64encode(f"{self.client_ID}:{self.client_Secret}".encode())).decode()
        headers = {
            "Content-Type":"application/json",
            "X-SPACE-AUTH-KEY":f"Bearer {secret}"
        }
        response = requests.post(f"{self.gateway_URL}api/technicaltokenmanager/v3/oauth/token?appName={self.app_Name}&appVersion={self.app_Version}&hostTenant={self.tenant}&userTenant={self.tenant}",headers=headers)
        return response.text
    
    #pega apenas o Access Token
    def getBearerToken(self):
        token_data = json.loads(self.getToken())
        if "access_token" in token_data:
            return token_data["access_token"]
        else:
            return "Token não encontrado, ou possível outro erro"
        print(getBearerToken)
    #Insere um dado ao Asset
    def putTimeSeriesData(self,assetId:str,aspectName:str,payload:dict):

        '''Crie um dicionário e envie o parâmetro payload, no dicionário crie uma chave _time e defina seu valor como None
        Examplo:
            putTimeSeriesData(assetId,aspectName,{"_time":None,"Temperature":90.50})
        '''
        headers = {
            "Authorization":'bearer '+self.getBearerToken(),
            "Content-Type":"application/json",
        }
        url = f"{self.gateway_URL}api/iottimeseries/v3/timeseries/{assetId}/{aspectName}"
        payload.update({"_time":datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()})
        print(requests.put(url,json=[payload],headers=headers).status_code)
    
    #Retorna um timeseries de um asset
    def getTimeSeries(self,assetID,aspectName,fromDateTime,toDateTime):
        headers = {
            "Authorization":'Bearer '+self.getBearerToken(),
            "Content-Type":"application/json",
        }
        if(fromDateTime=="" or toDateTime==""):
            url = f"{self.gateway_URL}api/iottimeseries/v3/timeseries/{assetID}/{aspectName}"
            return json.loads(requests.get(url,headers=headers).text)
        url = f"{self.gateway_URL}api/iottimeseries/v3/timeseries/{assetID}/{aspectName}?from={fromDateTime}&to={toDateTime}"
        return json.loads(requests.get(url,headers=headers).text)