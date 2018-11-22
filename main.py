# Texto cifrado en Vigenere grabado en hexadecimales

cipher_hex = 'F96DE8C227A259C87EE1DA2AED57C93FE5DA36ED4EC87EF2C63AAE5B9A7E'
cipher_hex += 'FFD673BE4ACF7BE8923CAB1ECE7AF2DA3DA44FCF7AE29235A24C963FF0DF'
cipher_hex += '3CA3599A70E5DA36BF1ECE77F8DC34BE129A6CF4D126BF5B9A7CFEDF3EB8'
cipher_hex += '50D37CF0C63AA2509A76FF9227A55B9A6FE3D720A850D97AB1DD35ED5FCE'
cipher_hex += '6BF0D138A84CC931B1F121B44ECE70F6C032BD56C33FF9D320ED5CDF7AFF'
cipher_hex += '9226BE5BDE3FF7DD21ED56CF71F5C036A94D963FF8D473A351CE3FE5DA3C'
cipher_hex += 'B84DDB71F5C17FED51DC3FE8D732BF4D963FF3C727ED4AC87EF5DB27A451'
cipher_hex += 'D47EFD9230BF47CA6BFEC12ABE4ADF72E29224A84CDF3FF5D720A459D47A'
cipher_hex += 'F59232A35A9A7AE7D33FB85FCE7AF5923AA31EDB3FF7D33ABF52C33FF0D6'
cipher_hex += '73A551D93FFCD33DA35BC831B1F43CBF1EDF67F0DF23A15B963FE5DA36ED'
cipher_hex += '68D378F4DC36BF5B9A7AFFD121B44ECE76FEDC73BE5DD27AFCD773BA5FC9'
cipher_hex += '3FE5DA3CB859D26BB1C63CED5CDF3FE2D730B84CDF3FF7DD21ED5ADF7CF0'
cipher_hex += 'D636BE1EDB79E5D721ED57CE3FE6D320ED57D469F4DC27A85A963FF3C727'
cipher_hex += 'ED49DF3FFFDD24ED55D470E69E73AC50DE3FE5DA3ABE1EDF67F4C030A44D'
cipher_hex += 'DF3FF5D73EA250C96BE3D327A84D963FE5DA32B91ED36BB1D132A31ED87A'
cipher_hex += 'B1D021A255DF71B1C436BF479A7AF0C13AA14794'

# devuelve lista con los divisores de un numero entero, omite el numero 1 como divisor
def divisores(num):
    divisores = []
    for i in range(2, num / 2):
        if num % i == 0:
            divisores.append(i)
    divisores.append(num)
    return divisores

# devuelve las frecuencias de una lista de numeros en forma de diccionario
def frecuencias(lista):
    conjunto = set(lista)
    frec_dict = {}
    for elem in conjunto:
        frec_dict[elem] = lista.count(elem)
    return frec_dict

# devuelve la llave del valor maximo o minimo de un diccionario
def max_min(dicc, cual):
    if cual:
        val = max(dicc.values())
    else:
        val = min(dicc.values())
    for num in dicc:
        if dicc[num] == val:
            return num

# Busca cadenas repetidas con el largo indicado por n en un mensaje cifrado
# Devuelve un conjunto con las separaciones o distancias entre las coincidencias halladas
def separaciones(msg, n):
    separaciones = set()
    for i in range(0, len(msg) / 2):
        for j in range(i + n, len(msg) - n):
            if msg[i:i + n] == msg[j:j + n]:
                separaciones.add(j - i)
    return separaciones

# Cifra un mensaje en Vigenere usando una clave dada y XOR
def vigenere(msg, key):
    cipher = ''
    for i in range(len(msg)):
        cipher += chr(ord(msg[i]) ^ ord(key[i % len(key)]))
    return cipher

# calcula la sumaproducto de las frecuencias en el stream y las frecuencias en ingles
def sum_sq_q(stream):
    distrib = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.2, 0.8, 4.0, 2.4, 6.8, 7.5, 1.9, 0.1, 6.0, 6.3, 9.1, 2.8, 1.0, 2.4, 0.2, 2.0, 0.1]
    suma = 0
    for i in range(26):
        suma += distrib[i] / 100 * stream.count(chr(i+97)) / len(stream) 
#        print suma
    return suma

# devuelve un caracter que maximiza la probabilidad de ser parte de la clave Vinegere
def test_b(stream):
    max_val = 0
    for i in range(255):
        b = True
        for char in stream:
            if not (32 <= i ^ ord(char) <= 127):
                #print i, ord(streams[0][j]), i ^ ord(streams[0][j])
                b = False
                break
        if b:
            if sum_sq_q(vigenere(stream, chr(i))) > max_val:
                max_val = sum_sq_q(vigenere(stream, chr(i)))
                print i, max_val
                key_letter = chr(i)
    print 
    return key_letter

def main():
    # convierto el hexadecimal en una cadena de caracteres
    cipher_str = ''
    for i in range(0, len(cipher_hex), 2):
        cipher_str += chr(int(cipher_hex[i:i + 2], 16))
        
    # obtengo las separaciones de coincidencias de secuencias de 4 caracteres (o 3 caracteres)
    distancias = separaciones(cipher_str, 4)
    
    # obtengo una lista con los divisores de las separaciones halladas
    divisores_lista = []
    for num in distancias:
        divisores_lista += divisores(num)

    # de la lista de divisores, deduzco la longitud de la clave hallando el divisor que mas se repite
    key_len = max_min(frecuencias(divisores_lista), True)
    
    # obtengo una lista de streams de caracteres tomando un caracter a una separacion dada por key_len
    streams = []
    for j in range(key_len):
        s = ''
        for i in range(j, len(cipher_str), key_len):
            s += cipher_str[i]
        streams.append(s)
    
    print streams
    
    # para cada stream de la lista debo encontrar un caracter K que maximice la posibilidad de producir
    # un mensaje plain_text
    key = ''
    for stream in streams:
        key += test_b(stream)
    
    print key
    
    # usando la clave encontrada decodifico el mensaje Vigenere
    print vigenere(cipher_str, key)
    
main()
