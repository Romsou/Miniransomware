import os

from pathlib import Path
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


private_key_text = b"""-----BEGIN PRIVATE KEY-----
MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCmnf/Ka/TBIThi
+ulsLvUbWKHCZNg15CwPCCwZwl8UAg80dZfpbsj61hyMy6m/5QkIC+KeO9RN9Wq9
OSeNLnjoj3QwBA8ke7or1cvAQEIPouyrRVKm9qTVlUn+adPKnR7vMK2PYTn+TYNo
+sdzCM24UB+mKqN/r408NBtFQx3gsHUPCBwjJNFUBhJ7N7FmUFrQQwMRR2cfqqVh
GiKseFFvVJsqmjoCyQFl2pNHYYjTi0DCbbM8U27dvbsbLqfKiSdh6xX5SD6K5bar
/teYYQaQUdiJeB/dLn60nfQMmyXi+kTweOwVTrI6lr70HX/vC+58ephJ83ot5YUO
2nGjXSC/AgMBAAECggEBAJQpkBrK4T0Uc3XhNc0T/LYynLWmw3U4z80WMVE+vRmn
symtIEdeUq5r07uIKA0SeHOFTiHzhhlFEYPu3TL4jmAPoPxJv8VrmOP+HE97VMNe
2CJ9ZMBAN9gOB1yLcuCL08RTfyMvDEkNWLvztYSf4X/zEBHNfNLAo1FT7KQsyNbR
5AGXsFZPTSsyQW7Ri5bwCxpRxXAta4tqEIhBKBS+Oh3+Y5mH+SYAIpYG2QJcBceQ
tgtE0Zlp8QhbtnljHZfiRLxd5+CrF6Ws2Y9Po3pPYFqZYoEllm723Q2ICUcBxm7W
Xm0Q2IezAkqQwIVRxBjkHXPXuncu+bBGaI3x4fZsAzECgYEA0vBniinGaEH2cmj7
yhWR7rOGtEUlQSywfoQrpYzRXjU3fDrhx+xtUseztVAgN9KqKuJuHxlNfOqvDebW
0QJzKJqg1myQbk69tIU/8b5Yfh22BWP9FnnMMvv0A188c8hvlMkYjZ2GTZxXALys
1W0sB9sxZSSQc9Yr/SpKaS9GQeUCgYEAyjXE/r9BI7c/gxwNRvp0Wg520NTahX8N
9FqZtRrqWTd1VC0/Pzyze0iVcf7t2pF37M2QCNDRzSVQ1hrU91qO2HQUeKTbMy60
Gt97PwiFtt7JEK1z+Zkpt50yFcqRde3j86e1h0Yn2OeTqDnoVei5qj0k1dlcGRXc
Ddoq4KCofdMCgYAhvaiiNgpxlNOJ+3cDHS4po3fRkBnkcfSNWDDvGzZGPnbwnS6O
XyghjKYXQ4jTxRPJJkz9FnwJljSIIbuM1Tp8bTd69QSpUFkR7hqLXaokCjaaaCMM
nFDoetrOS0aNMqt+fig6Rs87zN0x1fxDa2IWo54kEpQ0ozaIGWKrro8rbQKBgQCT
cyQEExh/38cbZuAzqrwfUz7Gxv/VqrFVRp+g1VCf3/XZfOkKxsumEWaQarGs2LiX
X8ow83yZWCWbCpPTDyDsq7ClzKjeqKbClcX8T82ZbNk3JRRVpJ8r+h+kjkMFuIOp
j9iqHLk/zJX6bMeDpaGFhvKOUeJ7lFoTa8wqYlya6wKBgQCseDV+9toMbysFO5uN
N2lwI53NWO9NyM1607eZ1ormCWCAt2miDCA1PhB4HdX6O2lj94+Um7U3A7t30Ifu
Lmx2HxwIAcVwE5UpvUrY0o0Rr9SOe0I5OFzgqs3jvAy+852xMJ2xm7IPs35YnHaD
t9ZdKGP8Up1RdIQ7HIgNIw5ovw==
-----END PRIVATE KEY-----
"""


def main():
    private_key = load_private_key()
    decrypt_files(private_key)


def load_private_key():
    private_key = serialization.load_pem_private_key(private_key_text, password=None, backend=default_backend())
    return private_key


def decrypt_files(private_key):
    files_to_decrypt = [file for file in os.listdir('poc_data') if 'encrypted' in file]

    for file in files_to_decrypt:
        print(file)
        with open(Path(f'poc_data/{file}'), 'rb') as encrypted_file:
            decrypted_content = private_key.decrypt(
                encrypted_file.read(),
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

        decrypted_filename = file.replace('encrypted', 'decrypted')
        with open(Path(f'poc_data/{decrypted_filename}'), 'wb') as decrypted_file:
            decrypted_file.write(decrypted_content)


if __name__ == '__main__':
    main()
