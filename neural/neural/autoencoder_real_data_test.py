import csv
import sys
import numpy as np
from simple_autoencoder import SimpleAutoencoder
import matplotlib.pyplot as plt

def dataToCSV(path, names, data):
    f = open(path, "w")
    f.write(toCSVLine(names, "%s"))
    #format = "{0}\n{1}"
    for row in data:
        f.write(toCSVLine(row, "%.5f"))
        #result = format.format(result, toCSVLine(row))
    f.close()

def toCSVLine(data, format):
    s = ','.join(format % d for d in data)
    return "{0}\n".format(s)

def CSVToData(path):
    f = open(path, 'r')
    reader = csv.reader(f)
    data = []
    for row in reader:
        data.append(row)
    f.close()
    data = np.asarray(data)
    return np.asarray(data[0,:]), np.asarray(data[1:,:])


def norm(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return abs(np.expand_dims(l2, axis))

def normalized(a, norm):
    return a / norm

def denormalized(a, norm):
    return a * norm

def normalize(v):
    norm=np.linalg.norm(v, ord=1)
    if norm==0:
        norm=np.finfo(v.dtype).eps
    return v/norm

def plot_vec(real, gen, l, inds, names):
    gen_l = [name + "gen" for name in names[inds]]
    real_l = [name + "real" for name in names[inds]]
    gen_l.extend(real_l)
    plt.plot(gen)
    plt.plot(real)
    plt.legend(gen_l)
    #plt.legend(n)
    plt.ylabel(l)
    plt.show()

if __name__ == "__main__":
    dir = "C:\Temp"
    path = "{0}\\01_01.csv".format(dir)
    names, data = CSVToData(path)
    inds = np.asarray(range(len(names) - 1))
    data = np.asarray(data[:,inds]).astype('float32')
    #data = (data[:,:2]).astype('float32') / np.average(data[:,:2])
    nrm = norm(data)
    data = normalized(data, nrm)
    dataToCSV("{0}\\orig_normalized.csv".format(dir), names, data)
    #data = data.reshape((len(data), np.prod(data.shape[1:])))
    #msk = np.random.rand(len(data)) < 0.8
    #x_train = data[msk]
    #x_test = data[~msk]
    #print (x_train.shape)
    #print (x_test.shape)
    #x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    #x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
    #data_r = data.reshape((len(data), np.prod(data.shape[1:])))
    autoencoder = SimpleAutoencoder(shape=(data.shape[1],), encoding_dim=80)
    #data = data.reshape((len(data), np.prod(data.shape[1:])))
    from timeit import default_timer as timer
    start = timer()
    autoencoder.fit(data, data, epochs=3000, batch_size=250, shuffle=True)
    end = timer()
    print("NN learn time is {0}".format(end - start))
    encoded_imgs = autoencoder.predict(data)
    decoded_imgs = autoencoder.predict(encoded_imgs)

    new_path = "{0}\\csv_temp_dec.csv".format(dir)
    # error = []
    # for i in range(data.shape[1]):
    #     error.append(np.subtract(np.asarray(data[:,i], dtype=float), np.asarray(decoded_imgs[:,i], dtype=float)))
    # dataToCSV("{0}\\csv_err.csv".format(dir), names, np.asarray(error))
    #dataToCSV(new_path, names, data)
    #dcd = decoded_imgs.reshape(data.shape[1:])
    #tst = x_test.reshape(data.shape[1:])

    dataToCSV(new_path, names, decoded_imgs)
    #plt.plot(decoded_imgs)

    plot_vec(data, decoded_imgs, "normalized", inds, names)

    #gen_denorm = denormalized(decoded_imgs, nrm)
    #real_denorm = denormalized(data, nrm)

   # plot_vec(real_denorm, gen_denorm, "denormalized", length, names)

    # n = 10  # how many digits we will display
    # plt.figure(figsize=(20, 4))
    # for i in range(n):
    #     # display original
    #     ax = plt.subplot(2, n, i + 1)
    #     plt.imshow(x_test[i].reshape(28, 28))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    #
    #     # display reconstruction
    #     ax = plt.subplot(2, n, i + 1 + n)
    #     plt.imshow(decoded_imgs[i].reshape(28, 28))
    #     plt.gray()
    #     ax.get_xaxis().set_visible(False)
    #     ax.get_yaxis().set_visible(False)
    # plt.show()



