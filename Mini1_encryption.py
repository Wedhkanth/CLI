import random
import string

characters = list(" "+string.ascii_letters + string.punctuation + string.digits)
#print(characters)

key = characters.copy()
random.shuffle(key)

plain_text=input("Enter the text to be encrypted: ")
cypher_text = ""

#ENCRYPTION
for letter in plain_text:
    index=characters.index(letter)
    cypher_text += key[index]

print(f"Original Text: {plain_text}")
print(f"Encrypted Text: {cypher_text}")

#DECRYPTION
plain_text1=""
cypher_text1=input("Enter the text to be decrypted: ")
for letter in cypher_text1:
    index=key.index(letter)
    plain_text1 += characters[index]

print(f"Original Text: {cypher_text1}")
print(f"Decrypted Text: {plain_text1}")

 