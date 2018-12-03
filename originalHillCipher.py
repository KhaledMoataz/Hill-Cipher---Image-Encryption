import imageio
import numpy as np

ourFeature = 1

#---------------Read Image to Encrypt---------------
img = imageio.imread('0.png')

nl = l = img.shape[0]
w = img.shape[1]
n = 4
if l%n:
    nl = (int((l - 1) / n) + 1) * n
img2 = np.zeros((nl,w,3))
img2[:l,:w,:] += img

def f(x, y):
    return x * x + y * y + 10 * x + 10 * y

if (ourFeature):
    img3 = np.zeros((nl,w,3))
    for x in range(nl):
        for y in range(w):
            v = f(x, y)
            img3[x, y, 0] = v
            img3[x, y, 1] = v
            img3[x, y, 2] = v
    img2 = (img2 + img3) % 256
    imageio.imwrite('Step.png', img2)

#-------------Generating Encryption Key-------------
Mod = 256
k = 23                                                          #Key for Encryption

d = np.random.randint(256, size = (int(n/2),int(n/2)))          #Arbitrary Matrix, should be saved as Key also
I = np.identity(int(n/2))
a = np.mod(-d,Mod)

b = np.mod((k * np.mod(I - a,Mod)),Mod)
k = np.mod(np.power(k,127),Mod)
c = np.mod((I + a),Mod)
c = np.mod(c * k, Mod)

A1 = np.concatenate((a,b), axis = 1)
A2 = np.concatenate((c,d), axis = 1)
A = np.concatenate((A1,A2), axis = 0)
Test = np.mod(np.matmul(np.mod(A,Mod),np.mod(A,Mod)),Mod)       #making sure that A is an involutory matrix, A*A = I

# Saving key as an image
key = np.zeros((n + 1, n))
key[:n, :n] += A
# Adding the dimension of the original image within the key
# Elements of the matrix should be below 256
key[-1][0] = int(l / Mod)
key[-1][1] = l % Mod
key[-1][2] = int(w / Mod)
key[-1][3] = w % Mod
#imageio.imwrite("Key.png", key)

#-------------Encrypting-------------
Encrypted = np.zeros((nl,w,3))
for i in range(int(nl/n)):
    Enc1 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,0] % Mod)) % Mod
    Enc2 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,1] % Mod)) % Mod
    Enc3 = (np.matmul(A % Mod,img2[i * n:(i + 1) * n,:,2] % Mod)) % Mod
    
    Enc1 = np.resize(Enc1,(Enc1.shape[0],Enc1.shape[1],1))
    Enc2 = np.resize(Enc2,(Enc2.shape[0],Enc2.shape[1],1))
    Enc3 = np.resize(Enc3,(Enc3.shape[0],Enc3.shape[1],1))
    Encrypted[i * n:(i + 1) * n,:] += np.concatenate((Enc1,Enc2,Enc3), axis = 2)                #Enc = A * image

imageio.imwrite('Encrypted.png',Encrypted)

#-------------Decrypting-------------
Enc = imageio.imread('Encrypted.png')                           #Reading Encrypted Image to Decrypt
nl = int(Enc.shape[0])
# Loading the key
#A = imageio.imread('Key.png')
A = key
n = int(A.shape[0] - 1)
l = int(A[-1][0] * Mod + A[-1][1]) # The length of the original image 
w = int(A[-1][2] * Mod + A[-1][3]) # The width of the original image
A = A[0:-1]

Decrypted = np.zeros((nl,w,3))
for i in range(int(nl/n)):
    Dec1 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,0] % Mod)) % Mod
    Dec2 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,1] % Mod)) % Mod
    Dec3 = (np.matmul(A % Mod,Enc[i * n:(i + 1) * n,:,2] % Mod)) % Mod
    
    Dec1 = np.resize(Dec1,(Dec1.shape[0],Dec1.shape[1],1))
    Dec2 = np.resize(Dec2,(Dec2.shape[0],Dec2.shape[1],1))
    Dec3 = np.resize(Dec3,(Dec3.shape[0],Dec3.shape[1],1))
    Decrypted[i * n:(i + 1) * n,:] += np.concatenate((Dec1,Dec2,Dec3), axis = 2)                #Dec = A * Enc

if (ourFeature):
    Decrypted = (Decrypted - img3) % 256

Decrypted = Decrypted[:l,:w,:]                                            #Returning Dimensions to the real image

imageio.imwrite('Decrypted.png', Decrypted)

print("HEXAGEEKS")
