import imageio
import numpy as np
Mod = 256
#-------------Decrypting-------------
Enc = imageio.imread('Encrypted.png')                           #Reading Encrypted Image to Decrypt
# Loading the key
A = imageio.imread('Key.png')
l = A[-1][0] * Mod + A[-1][1] # The length of the original image 
w = A[-1][2] * Mod + A[-1][3] # The width of the original image
A = A[0:-1]

Dec1 = (np.matmul(A % Mod,Enc[:,:,0] % Mod)) % Mod
Dec2 = (np.matmul(A % Mod,Enc[:,:,1] % Mod)) % Mod
Dec3 = (np.matmul(A % Mod,Enc[:,:,2] % Mod)) % Mod

Dec1 = np.resize(Dec1,(Dec1.shape[0],Dec1.shape[1],1))
Dec2 = np.resize(Dec2,(Dec2.shape[0],Dec2.shape[1],1))
Dec3 = np.resize(Dec3,(Dec3.shape[0],Dec3.shape[1],1))
Dec = np.concatenate((Dec1,Dec2,Dec3), axis = 2)                #Dec = A * Enc

Final = Dec[:l,:w,:]                                            #Returning Dimensions to the real image

imageio.imwrite('Decrypted.png',Final)

print("HEXAGEEKS")
