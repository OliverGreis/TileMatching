import numpy as np

def encrypt(key, message):
    message = message.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for letter in message:
        if letter in alpha:

            letter_index = (alpha.find(letter) + key) % len(alpha)

            result = result + alpha[letter_index]
        else:
            result = result + letter

    return result

def decrypt(key, message):
    message = message.upper()
    alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ""

    for letter in message:
        if letter in alpha:

            letter_index = (alpha.find(letter) - key) % len(alpha)

            result = result + alpha[letter_index]
        else:
            result = result + letter

    return result

word = 'James'


print(list)
Total = [0,0,0,0]
navn1 = "James Washington:"
stemme1 = [0,0,0,1]
encrypted1 = encrypt(3,navn1)
print("Stemme 1 enkrypteret er:",encrypted1,stemme1)
decrypted1 = decrypt(3,encrypted1)
print("Stemme 1 dekrypteret er:",decrypted1,stemme1)
Total = np.add(Total,stemme1)

navn2 = "Elisabeth Smith:"
stemme2 = [0,0,0,1]
encrypted2 = encrypt(3,navn2)
print("Stemme 2 enkrypteret er:",encrypted2,stemme2)
decrypted2 = decrypt(3,encrypted2)
print("Stemme 2 dekrypteret er:", decrypted2,stemme2)
Total = np.add(Total,stemme2)

print(encrypted1,stemme1)
print(encrypted2,stemme2)
print("Den endelige optælling er:", Total)
