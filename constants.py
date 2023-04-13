import os

from dotenv import load_dotenv

load_dotenv()

lnd_dir = os.environ.get("LND_DIR") 
tls_cert_path= os.environ.get("TLS_CERT_PATH") 
tls_cert_path1= os.environ.get("TLS_CERT_PATH1") 
grpc_host = os.environ.get("GRPC_HOST")
grpc_port = os.environ.get("GRPC_PORT")
grpc_port1 = os.environ.get("GRPC_PORT1")
macaroon_path = os.environ.get("MACAROON_PATH") 
macaroon_path1 = os.environ.get("MACAROON_PATH1") 
network = os.environ.get("NETWORK") 