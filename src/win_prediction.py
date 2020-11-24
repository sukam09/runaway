import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.layers.experimental import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import minmax_scale

import numpy as np
import pandas as pd
import os
import glob


def win_prediction():
    # Ignore tensorflow guide message
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    # Make numpy values easier to read.
    np.set_printoptions(precision=3, suppress=True)

    # Assign random seed
    tf.random.set_seed(123)

    all_file_list = glob.glob(os.path.join('../data/', 'recent_match_data_*'))
    all_data = []
    for file_ in all_file_list:
        df = pd.read_csv(file_)
        all_data.append(df)
    
    # Preprocess train, feature, label set
    recent_match_data_train = pd.concat(all_data, axis=0, ignore_index=True)
    recent_match_data_train.pop('Unnamed: 0')  # Ignore irrelevant data
    recent_match_data_features = recent_match_data_train.copy()
    recent_match_data_labels = recent_match_data_features.pop('win')

    # Convert feature and label set to numpy array
    recent_match_data_features = np.array(recent_match_data_features)
    recent_match_data_labels = np.array(recent_match_data_labels)

    x = recent_match_data_features
    y = np.zeros((len(recent_match_data_labels), 2))
    for idx in range(len(recent_match_data_labels)):
        y[idx][recent_match_data_labels[idx]] = 1  # Convert to one-hot vector

    # 0~1 scaling
    x = minmax_scale(x, axis=0, copy=True)

    # Train, valid, test set split
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=123)
    x_train, x_valid, y_train, y_valid = train_test_split(x_train, y_train, test_size=0.125, random_state=123)

    recent_match_data_model = tf.keras.Sequential([
        layers.Dense(64, activation='relu'),
        layers.Dense(32, activation='relu'),
        # layers.Dense(2, activation='softmax')
        layers.Dense(2, activation='sigmoid')
    ])

    # Train
    recent_match_data_model.compile(
        loss=tf.losses.MeanSquaredError(),
        optimizer=tf.optimizers.Adam(),
        metrics=['accuracy'],
    )

    recent_match_data_model.fit(
        x_train,
        y_train,
        epochs=100,
        validation_data=(x_valid, y_valid),
        batch_size=1,
        verbose=1
    )

    # Evaluate and predict
    loss, acc = recent_match_data_model.evaluate(
        x_test,
        y_test,
        batch_size=1,
        verbose=1
    )
    y_pred = recent_match_data_model.predict(x_test)

    print('\n' + '=' * 100 + '\n승패 예측 결과\n' + '=' * 100)
    for i in range(len(y_pred)):
        # print(np.argmax(y_pred[i]))
        if np.argmax(y_pred[i]) == 1:
            print('승리')
        else:
            print('패배')


# For debug
win_prediction()
