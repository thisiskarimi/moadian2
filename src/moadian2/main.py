import os
import tempfile
import json
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal
import requests
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding
from cryptography.x509 import load_pem_x509_certificate
from .dto import Packet
from .encryption import sign, encrypt
from .settings import *


class Moadian():

    def __init__(self, fiscal_id, private_key, certificate) -> None:
        self.certificate = load_pem_x509_certificate(certificate)
        self.private_key = load_pem_private_key(private_key, password=None)
        self.fiscal_id = fiscal_id

    def get_cert(self):
        return self.certificate.public_bytes(
            Encoding.PEM).decode().replace(
                "-----BEGIN CERTIFICATE-----", '').replace(
                    "-----END CERTIFICATE-----",'')

    def _get_tax_gov_key(self):
        # look for a file containing key
        temp_dir = tempfile.gettempdir()
        filename = "tax_gov_key"
        where_to_find = os.path.join(temp_dir, filename)
        if os.path.isfile(where_to_find):
            try:
                with open(where_to_find) as f:
                    k = json.load(f.read())
                return k['id'], k['key']
            except Exception:
                pass
        srv_info = self._get_server_information()
        k = srv_info["publicKeys"][0]
        # save it for further uses
        with open(where_to_find, 'w') as f:
            json.dump(k, f)
        return k

    def _prepare_tax_gov_key(self):
        server_public_key = self._get_tax_gov_key()["key"]
        server_public_key = "-----BEGIN PUBLIC KEY-----\n" + \
        server_public_key + "\n-----END PUBLIC KEY-----"
        return server_public_key

    def _send_http_request(self, url, method="get", headers={}, need_token=True, **kwargs):
        if need_token:
            token = self._get_token()
            headers["Authorization"] = "Bearer {}".format(token)
        response = requests.request(method, url, headers=headers, **kwargs)
        return response.json()

    def _get_token(self):
        result = self._send_http_request(NONCE_URL, need_token=False)
        payload = json.dumps({
            "nonce": result["nonce"],
            "clientId": self.fiscal_id
        })
        jwt = sign(payload, self.private_key, self.get_cert())
        return jwt

    def _get_server_information(self):
        return self._send_http_request(SERVER_INFORMATION_URL)

    def send_invoice(self, invoice):
        #invoice = self._parse_invoice(invoice)
        server_public_key = self._prepare_tax_gov_key()
        signed_invoice = sign(invoice, self.private_key, self.get_cert())
        encrypted_invoice = encrypt(signed_invoice, server_public_key)
        packets = [Packet(encrypted_invoice, self.fiscal_id).build()]
        headers = {"Content-Type": 'application/json'}
        return self._send_http_request(INVOICE_URL, "post", headers, data=json.dumps(packets))

    def inquiry(self, 
                status: Literal["SUCCESS", "FAILED", "TIMEOUT", "IN_PROGRESS"]=None,
                page_num: int=1, page_size: int = 10):
        params = {
            "pageNumber": page_num,
            "pageSize": page_size,
            "status": status,
        }
        return self._send_http_request(INQUIRY_URL, params=params)

    def inquiry_by_reference_id(self, reference_id: list):
        params = {"referenceIds": reference_id}
        return self._send_http_request(INQUIRY_BY_REFERENCE_ID_URL, params=params)

    def inquiry_by_uid(self, uid: list):
        params = {"uidList": uid, "fiscalId": self.fiscal_id}
        return self._send_http_request(INQUIRY_BY_UID_URL, params=params)

    def get_fiscal_information(self):
        params = {"memoryId": self.fiscal_id}
        return self._send_http_request(FISCAL_INFORMATION_URL, params=params)

    def get_tax_payer(self, economic_code):
        params = {"economicCode": economic_code}
        return self._send_http_request(TAXPAYER_URL, params=params)
