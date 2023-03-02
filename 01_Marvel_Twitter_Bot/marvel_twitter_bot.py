import hashlib
import os
import time

import requests
import tweepy
from dotenv import load_dotenv

load_dotenv()


auth = tweepy.OAuthHandler(os.getenv("CONSUMER_API_KEY"), os.getenv("CONSUMER_API_SECRET_KEY"))
auth.set_access_token(os.getenv("ACCESS_TOKEN"), os.getenv("ACCESS_TOKEN_SECRET"))

twitter_api = tweepy.API(auth)

# Enviar un Tweet
twitter_api.update_status("Hola Granola")

# Marvel API

# 1. Obtener public y private key del sitio de Marvel
public_key = os.getenv("MARVEL_PUBLIC_KEY")
private_key = os.getenv("MARVEL_PRIVATE_KEY")

# 2. Definir un timestamp para ejecutar la llamada
ts = str(time.time())

# 3. Creamos el hash md5 con el lineamiento que nos indico Marvel
# ts - a timestamp (or other long string which can change on a request-by-request basis)
# hash - a md5 digest of the ts parameter, your private key and your public key (e.g. md5(ts+privateKey+publicKey)
hash_code = hashlib.md5(f"{ts}{private_key}{public_key}".encode("utf-8")).hexdigest()

# 4. Llamar a algun endpoint indicado en la documentaction. Por ejemplo el de personajes
marvel_url = (
    f"http://gateway.marvel.com/v1/public/characters?ts={ts}&hash={hash_code}&apikey={public_key}"
)

# Listo!
response = requests.get(marvel_url)

print(response.json)
