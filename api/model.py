import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

class Model:
    def __init__(self, df):
        def create_sequences(df, seq_length=1, n_predictions=1):
            X, y = [], []
            for i in range(len(df) - seq_length - n_predictions + 1):
                X.append(df.iloc[i:i + seq_length, 1:].values)  # Измените на 1:, чтобы исключить 'Open Time'
                y.append(
                    df.iloc[i + seq_length:i + seq_length + n_predictions, 4].values)  # Предсказание n значений Close
            return np.array(X), np.array(y)

        # Подготовка данных
        X, y = create_sequences(df[['Open Time', 'Open', 'High', 'Low', 'Close']], seq_length=1)

        # Преобразуем y в массив float32
        y = y.astype(np.float32)

        # Убедимся, что X и y имеют правильные формы
        print("X shape:", X.shape)
        print("y shape:", y.shape)

        # Определение модели
        model = Sequential([
            LSTM(64, activation='relu', input_shape=(X.shape[1], X.shape[2])),
            Dense(4)  # Предсказываем только одно значение (Close)
        ])

        model.compile(optimizer='adam', loss='mse')

        # Обучение модели
        model.fit(X, y, epochs=50, batch_size=32)

        # Предсказание на следующий час
        last_data = df[['Open', 'High', 'Low', 'Close']].values[-1].reshape(1, 1, 4)
        self.prediction = model.predict(last_data)