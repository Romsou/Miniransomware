# Miniransomware

## Description

This repository contains the proof of concept of a very simple and minimalist ransomware.
It is intentionnally limited to encrypt files contained within the poc_data folder to avoid to encrypt your whole system by accident.

This software is intended for educationnal purpose only and was made for a presentation during a cybersecurity class, please, do not use it to harm systems you don't have authorization to.

You can also use this software to play around and encrypt your own files, however I would not advise using it to implement serious cryptography since I am not a professionnal cryptologist myself.

## Principle

The miniransomware source code contains a hard coded public key which is used to encrypt files, while the decrypter contains the corresponding private key to decrypt the encrypted data.

In a real life scenario, the idea would be to use the miniransomware to encrypt files, while not distributing the decrypter up until the ransom is paid.

Of course, since the goal is not to implement a real attack, only the content of the poc_data folder is encrypted and decrypted.

## Installation

You can easily install any required dependencies with the following command

```bash
python3 -m pip install -r requirements.txt
```
## Usage

### Generate a key pair

```bash
python3 miniransomware.py -g
```

### Encrypt the content of poc_data

```bash
python3 miniransoware.py
```

### Decrypt the content of poc_data

```bash
python3 decrypter.py
```

