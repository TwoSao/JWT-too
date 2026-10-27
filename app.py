
import base64
import hashlib
import hmac
import json
from datetime import datetime
from zoneinfo import ZoneInfo

token = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9."
    "eyJzdWIiOiIxMDI0IiwibmFtZSI6Ik1hcmkgTWFhc2lrYXMiLCJyb2xlIjoic3R1ZGVudCIsImlhdCI6MTc2MTIwNjQwMCwiZXhwIjoxNzYxMjEwMDAwfQ."
    "ZL6DsKKTa2hRmEkkMASGBI7hZW8ot5bJS2I800xVTwM"
)
SECRET_KEY = "saladus123"

# Base64URL dekodeerimine
def b64url_decode(text):
    text += "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text)


# Base64URL kodeerimine
def b64url_encode(data):
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


# JWT jagamine kolmeks osaks
header_b64, payload_b64, signature = token.split(".")

header = json.loads(b64url_decode(header_b64))
payload = json.loads(b64url_decode(payload_b64))


print("=== OSA 1: JWT DEKODEERIMINE ===")
print("Header:", header)
print("Payload:", payload)

tz = ZoneInfo("Europe/Tallinn")

issued_at = datetime.fromtimestamp(payload["iat"], tz)
expires_at = datetime.fromtimestamp(payload["exp"], tz)

print("Valjastatud:", issued_at.strftime("%d.%m.%Y %H:%M:%S"))
print("Aegub:", expires_at.strftime("%d.%m.%Y %H:%M:%S"))

duration = payload["exp"] - payload["iat"]
print("Kehtivusaeg:", duration // 60, "minutit")

now = datetime.now(tz).timestamp()
print("Kehtib praegu:", now < payload["exp"])


# Allkirja arvutamine
def calculate_signature(header_part, payload_part, secret):
    message = f"{header_part}.{payload_part}".encode()
    signature_bytes = hmac.new(
        secret.encode(),
        message,
        hashlib.sha256
    ).digest()

    return b64url_encode(signature_bytes)


print("\n=== OSA 2: ALLKIRJA KONTROLL ===")

correct_signature = calculate_signature(
    header_b64, payload_b64, "saladus123"
)

wrong_signature = calculate_signature(
    header_b64, payload_b64, "saladus124"
)

print(
    "Oige voti:",
    hmac.compare_digest(correct_signature, signature)
)

print(
    "Vale voti:",
    hmac.compare_digest(wrong_signature, signature)
)

# OSA 3: Tokeni võltsimise katse
print("\n=== OSA 3: TOKENI VOTSIMINE ===")

# Muudame kasutaja rolli
forged_payload = dict(payload)
forged_payload["role"] = "admin"

# Kodeerime muudetud payload'i uuesti
forged_payload_b64 = b64url_encode(
    json.dumps(
        forged_payload,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")
)

# Jätame vana allkirja alles
forged_token = (
    f"{header_b64}.{forged_payload_b64}.{signature}"
)

# Arvutame muudetud sisu jaoks õige allkirja
forged_signature = calculate_signature(
    header_b64,
    forged_payload_b64,
    SECRET_KEY
)

# Võrdleme uut allkirja vana allkirjaga
print("Algne roll:", payload["role"])
print("Uus roll:", forged_payload["role"])

print(
    "Vana allkiri sobib:",
    hmac.compare_digest(forged_signature, signature)
)

print("Võltsitud token:", forged_token)

print("Algne roll:", payload["role"])
print("Uus roll:", forged_payload["role"])
print("Vana allkiri sobib uue sisuga:",
      hmac.compare_digest(forged_signature, signature))
print("Võltsitud token:", forged_token)

print("\nJWT kontroll on lõpetatud.")
