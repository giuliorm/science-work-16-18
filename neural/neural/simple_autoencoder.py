from keras.layers import Input, Dense
from keras.models import Model


class SimpleAutoencoder:

    def __init__(self, shape,
                 encoding_dim=32,
                 first_activation='relu',
                 second_activation='sigmoid',
                 optimizer='adadelta',
                 loss='binary_crossentropy'):
        self.__encoding_dim = encoding_dim
        # this is the size of our encoded representations
        # 32 floats -> compression of factor 24.5, assuming the input is 784 floats

        # this is our input placeholder
        if shape is None:
            raise ValueError("Cannot create a model with None shape")
        input = Input(shape=shape)
        # "encoded" is the encoded representation of the input
        encoded = Dense(encoding_dim, activation=first_activation)(input)
        # "decoded" is the lossy reconstruction of the input
        decoded = Dense(shape[0], activation=second_activation)(encoded)

        # this model maps an input to its reconstruction
        self.__autoencoder = Model(input, decoded)
        # this model maps an input to its encoded representation
        self.__encoder = Model(input, encoded)
        # create a placeholder for an encoded (32-dimensional) input
        encoded_input = Input(shape=(encoding_dim,))
        # retrieve the last layer of the autoencoder model
        decoder_layer = self.__autoencoder.layers[-1]
        # create the decoder model
        self.__decoder = Model(encoded_input, decoder_layer(encoded_input))

        self.__autoencoder.compile(optimizer=optimizer, loss=loss)

    def fit(self, x_train, x_test, epochs=50, batch_size=256, shuffle=True):
        self.__autoencoder.fit(x_train, x_train,
                        epochs=epochs,
                        batch_size=batch_size,
                        shuffle=shuffle,
                        validation_data=(x_test, x_test))


    def predict(self, data):
        encoded = self.__encoder.predict(data)
        decoded = self.__decoder.predict(encoded)
        return decoded
