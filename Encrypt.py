import imageio
import numpy as np

#---------------Read Image to Encrypt---------------
img = imageio.imread('0.png')

l = img.shape[0]
w = img.shape[1]
n = max(l,w)
if n%2:
    n = n + 1
img2 = np.zeros((n,n,3))
img2[:l,:w,:] += img                                            #Making the picture to have square dimensions

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
imageio.imwrite("Key.png", key)

#-------------Encrypting-------------
Enc1 = (np.matmul(A % Mod,img2[:,:,0] % Mod)) % Mod
Enc2 = (np.matmul(A % Mod,img2[:,:,1] % Mod)) % Mod
Enc3 = (np.matmul(A % Mod,img2[:,:,2] % Mod)) % Mod

Enc1 = np.resize(Enc1,(Enc1.shape[0],Enc1.shape[1],1))
Enc2 = np.resize(Enc2,(Enc2.shape[0],Enc2.shape[1],1))
Enc3 = np.resize(Enc3,(Enc3.shape[0],Enc3.shape[1],1))
Enc = np.concatenate((Enc1,Enc2,Enc3), axis = 2)                #Enc = A * image

imageio.imwrite('Encrypted.png',Enc)

print("HEXAGEEKS")
