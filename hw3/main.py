import hashlib as h

message = 'i love computer security'
print(message)

hash = h.sha256(message.encode())
print('## <hashlib>')
print(hash.hexdigest())