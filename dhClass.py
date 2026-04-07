from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import serialization

PARAMETERS_PATH = "parameters.pem"


class DH:

    def __init__(self):
        if self.load_parameters() is None:
            self.parameters = dh.generate_parameters(generator=2,key_size=2048)
            self.serialize_upload_to_disk(self.parameters)
        else:
            self.parameters = self.load_parameters()

        self.a_private_key = None
        self.a_public_key = None


    def serialize_upload_to_disk(self,parameters):
        self.dh_parameters_pem = parameters.parameter_bytes(
            encoding=serialization.Encoding.PEM,
            format = serialization.ParameterFormat.PKCS3
        )

        with open(PARAMETERS_PATH,"wb") as file:
            file.write(self.dh_parameters_pem)


    def ready_to_send(self):
         dh_parameters_pem = self.parameters.parameter_bytes(encoding=serialization.Encoding.PEM,format=serialization.ParameterFormat.PKCS3)
         return dh_parameters_pem


    def load_parameters(self):
        try:
            with open(PARAMETERS_PATH, "rb") as f:
                parameters = serialization.load_pem_parameters(
                    f.read()
                )

                return parameters

        except:
            return None


    def create_keys(self):
        self.a_private_key = self.parameters.generate_private_key()
        self.a_public_key = self.a_private_key.public_key()

        return self.a_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo
        )


    def create_shared_key(self,client_key):
        object_client_key = serialization.load_pem_public_key(client_key)
        shared_key =  self.a_private_key.exchange(object_client_key)

        return HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info = b"handshake data",
        ).derive(shared_key)


    def from_bytes_to_object(self,public_key_client):
        return serialization.load_pem_public_key(public_key_client)
