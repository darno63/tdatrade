import time
import json
from calendar import timegm
import urllib.parse as up

from data import get_user_principals


class Principals():

  def __init__(self):
    self.principals = get_user_principals('streamerSubscriptionKeys,streamerConnectionInfo').json()
    self.account_id = self.principals['accounts'][0]['accountId']
    self.source_id = self.principals['streamerInfo']['appId']

  def uri(self):
    return "wss://" + self.principals['streamerInfo']['streamerSocketUrl'] + "/ws"
  

  def _get_epoch_ts(self):
    stream_token_ts = self.principals['streamerInfo']['tokenTimestamp']
    struct_time = time.strptime(stream_token_ts, '%Y-%m-%dT%H:%M:%S+0000')
    return timegm(struct_time) * 1000


  def _json_to_query(self, json):
    query =  '&'.join([f'{key}={val}' for key, val in json.items()])
    return up.quote(query)


  def _create_credentials(self):
    return {
    "userid": self.principals['accounts'][0]['accountId'],
    "token": self.principals['streamerInfo']['token'],
    "company": self.principals['accounts'][0]['company'],
    "segment": self.principals['accounts'][0]['segment'],
    "cddomain": self.principals['accounts'][0]['accountCdDomainId'],
    "usergroup": self.principals['streamerInfo']['userGroup'],
    "accesslevel": self.principals['streamerInfo']['accessLevel'],
    "authorized": "Y",
    "acl": self.principals['streamerInfo']['acl'],
    "timestamp": self._get_epoch_ts(),
    "appid": self.principals['streamerInfo']['appId']
    }

  """
  def _base_request(self, service, requestid, command, keys, fields):
    request = {"requests": [{
                 "service": service,
                 "requestid": requestid,
                 "command": command,
                 "account": self.principals['accounts'][0]['accountId'],
                 "source": self.principals['streamerInfo']['appId'],
                 "parameters": {
                   "keys": keys,
                   "fields": fields
                 }}]}
    return json.dumps(request)
  """

  def _base_request(self, service, requestid, command, parameters: dict):
    request = {"requests": [{
                 "service": service,
                 "requestid": requestid,
                 "command": command,
                 "account": self.principals['accounts'][0]['accountId'],
                 "source": self.principals['streamerInfo']['appId'],
                 "parameters": parameters
                 }]}
    return json.dumps(request)

  def login_request(self):
    request = {"requests": [{
                 "service": "ADMIN",
                 "requestid": 0,
                 "command": "LOGIN",
                 "account": self.principals['accounts'][0]['accountId'],
                 "source": self.principals['streamerInfo']['appId'],
                 "parameters": {
                   "token": self.principals['streamerInfo']['token'],
                   "version": "1.0",
                   "credential": up.urlencode(self._create_credentials())
                 }}]}
    return json.dumps(request)

  def logout(self):
    return self._base_request("ADMIN", "0", "LOGOUT", {})

  def quality_of_service(self, qoslevel: int):
    params = {"qoslevel": str(qoslevel)}
    return self._base_request("ADMIN", "2", "QOS", parameters=params)

  def chart_equity(self, ticker):
    params = {
      "keys": ticker,
      "fields": "0,1,2,3,4,5,6,7,8" 
    }
    return self._base_request("CHART_EQUITY", 5, "SUBS", parameters=params)

  def chart_futures(self, ticker):
    params = {
      "keys": ticker,
      "fields": "0,1,2,3,4,5,6,7"
    }
    return self._base_request("CHART_FUTURES", 6, "SUBS", parameters=params)

  def quote_request(self, ticker):
    params = {
      "keys": ticker,
      "fields": "0,1,2,3,4,5,6,7,8" 
    }
    return self._base_request("QUOTE", 4, "SUBS", parameters=params)


  def create_request(self, func):
    request = func(self.principals['accounts'][0]['accountId'], self.principals['streamerInfo']['appId'])
    return json.dumps(request)