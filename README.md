# moadian2

پکیج پایتون برای اتصال به نسخه دوم (با گواهی امضا) سامانه مودیان
## نصب

```python
pip install moadian2
```

## نحوه استفاده

```python
from moadian2 import Moadian

with open("path/to/private.key", "rb") as key_file:
    private_key = key_file.read()

with open("path/to/certificate.file", "rb") as cert_file:
    certificate = cert_file.read()

moadi = Moadian("YOUR-FISCAL-ID", private_key, certificate)
```

### ارسال صورتحساب
```python
invoice = '{"header": {"taxid": "A278W604C8000000004744", "indatim": 1692085800000, "indati2m": 1692085803000, "inty": 1, "inno": "0000001140", "irtaxid": null, "inp": 1, "ins": 1, "tins": "10101704295", "tinb": null, "tob": 2, "bid": null, "sbc": null, "bpc": null, "bbc": null, "ft": null, "bpn": null, "scln": null, "scc": null, "crn": null, "billid": null, "tprdis": 61000000, "tdis": 0, "tadis": 61000000, "tvam": 5490000, "todam": 0, "tbill": 66490000, "setm": 2, "cap": null, "insp": 61000000, "tvop": 5490000, "tax17": null}, "body": [{"sstid": "2330000604708", "sstt": "FooBar", "am": 5, "mu": null, "fee": 12200000, "cfee": null, "cut": null, "exr": null, "prdis": 61000000, "dis": 0, "adis": 61000000, "vra": 9, "vam": 5490000, "odt": null, "odr": null, "odam": null, "olt": null, "olr": null, "olam": null, "consfee": null, "spro": null, "bros": null, "tcpbs": null, "cop": null, "vop": 5490000, "bsrn": null, "tsstam": 66490000}], "payments": []}'
moadi.send_invoice(invoice)
```
```JSON
{"timestamp": 1722344752296, "result": [{"uid": "902bcc4e-d089-4de4-a27d-015a6cf23cba", "packetType": null, "referenceNumber": "4e9cd6e9-e0dd-4e12-bd8f-a872d84b1e54", "data": null}]}
```

### استعلام با uid
```python
moadi.inquiry_by_uid(["a9a63dea-5a91-4d5e-ba67-91f2358a3f0d", "7497b49d-16b4-41a3-a3fe-9e57d613a388"])
```

### استعلام با شماره پیگیری

```python
moadi.inquiry_by_reference_id(["a9a63dea-5a91-4d5e-ba67-91f2358a3f0d", "7497b49d-16b4-41a3-a3fe-9e57d613a388"])
```
### دریافت اطلاعات حافظه مالیاتی
```python
moadi.get_fiscal_information()
```

### دریافت اطلاعات مودی

```python
moadi.get_tax_payer("14003778990")
```
```JSON
{"nameTrade": "پیشخوان الکترونیک ایرانیان منطقه آزاد انزلی", "taxpayerStatus": "ACTIVE", "nationalId": "14003778990"}
```
