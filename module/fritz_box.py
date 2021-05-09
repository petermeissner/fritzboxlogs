
import requests
import hashlib
from xml.etree.ElementTree import XML as xml_parse
from dataclasses import dataclass



@dataclass
class FritzInfo:
  session_id: str 
  challenge:  str 
  block_time: str 
  rights:     str 


def f_request(url: str = "http://fritz.box/login_sid.lua") -> FritzInfo:
  res        = requests.get(url)
  xml        = xml_parse(res.content)
  
  info = FritzInfo(
      session_id = xml.findtext("./SID"),
      challenge  = xml.findtext("./Challenge"),
      block_time = xml.findtext(".BlockTime"),
      rights     = xml.findtext(".Rights")
    )
  
  return info



def f_get_session(user: str = "", password: str = "") -> FritzInfo:

  # initial request
  info = f_request(url = "http://fritz.box/login_sid.lua") 
  
  # hash challange and password
  md5 = hashlib.md5()
  md5.update(info.challenge.encode('utf-16le'))
  md5.update('-'.encode('utf-16le'))
  md5.update(password.encode('utf-16le'))
  response = info.challenge + '-' + md5.hexdigest()

  # request with response to challenge
  url = 'http://fritz.box/login_sid.lua?username=' + user + '&response=' + response
  info = f_request(url = url)

  # check if session was established
  if info.session_id == '0000000000000000':
    raise PermissionError('access denied')

  return info



