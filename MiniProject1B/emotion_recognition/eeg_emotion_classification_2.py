import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import torch
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import time

import os

# Constants
SAMPLE_RATE = 32 # (Hz)
GAMES = ["boring", "calm", "horror", "funny"]

torch.manual_seed(0)
np.random.seed(0)

class LFPDataset(torch.utils.data.Dataset):
    def __init__(self, X, y):
        self.X = X
        self.y = y.long()

    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


def train(n_epoch, model, train_batch_generator, test_batch_generator):
    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    for e in range(n_epoch):
        model.train(True)

        train_loss = []
        train_acc = []
        for X_batch, y_batch in train_batch_generator:
            model.zero_grad()
            logits = model(X_batch).squeeze()
            loss = torch.nn.functional.nll_loss(logits, y_batch)
            loss.backward()
            optimizer.step()

            train_loss.append(loss.item())

            prediction = torch.softmax(logits, dim=1).detach().numpy()
            prediction = np.argmax(prediction, axis=1)
            train_acc.append(
                accuracy_score(y_batch.detach().numpy(), prediction)
            )

        model.train(False)
        test_loss = []
        test_acc = []
        with torch.no_grad():
            for X_batch, y_batch in test_batch_generator:
                logits = model(X_batch).squeeze()
                loss = torch.nn.functional.nll_loss(logits, y_batch)
                test_loss.append(loss.item())

                prediction = torch.softmax(logits, dim=1).detach().numpy()
                prediction = np.argmax(prediction, axis=1)
                test_acc.append(
                    accuracy_score(y_batch.detach().numpy(), prediction)
                )

        print(
            f"Epoch {e}: "
            f"train_loss={np.mean(train_loss):.4f}, "
            f"train_acc={np.mean(train_acc):.4f}, "
            f"test_loss={np.mean(test_loss):.4f}, "
            f"test_acc={np.mean(test_acc):.4f}"
        )

def main():
    # Data loading and preprocessing
    data = []
    for game_id, game in enumerate(GAMES):
        game_data = pd.read_csv(os.path.join("data", f"S01G{game_id + 1}AllChannels.csv"))
        game_data["game"] = game
        data.append(game_data)
    data = pd.concat(data, axis=0, ignore_index=True)

    electrode = "T7"
    data = data[[electrode, "game"]]

    # Clip the data
    clip_length = 2
    clipped_data = []
    y = []
    for game_id, game in enumerate(GAMES):
        clips = np.array_split(
            data[data['game'] == game][electrode].to_numpy(),
            len(data[data['game'] == game]) // (clip_length * SAMPLE_RATE))
        clipped_data.extend(clips)
        y.extend([game_id] * len(clips))
    
    min_length = np.min([len(arr) for arr in clipped_data])
    X = np.vstack([arr[:min_length] for arr in clipped_data], dtype=float)
    y = np.array(y, dtype=int)

    X = np.expand_dims(X, 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    X_train, X_test = torch.Tensor(X_train), torch.Tensor(X_test)
    y_train, y_test = torch.Tensor(y_train), torch.Tensor(y_test)

    batch_size = 32

    train_batch_generator = torch.utils.data.DataLoader(
        LFPDataset(X_train, y_train),
        batch_size=batch_size,
        shuffle=True
    )

    test_batch_generator = torch.utils.data.DataLoader(
        LFPDataset(X_test, y_test),
        batch_size=batch_size,
        shuffle=False
    )

    # Define model
    model = torch.nn.Sequential(
        torch.nn.Conv1d(1, 1, kernel_size=4, padding="same"),
        torch.nn.ReLU(),
        torch.nn.Conv1d(1, 1, kernel_size=4, padding="same"),
        torch.nn.Flatten(),
        torch.nn.Linear(64, 4),
        torch.nn.LogSoftmax(dim=1)
    )

    # Train
    start_time = time.time()
    train(
        n_epoch=100,
        model=model,
        train_batch_generator=train_batch_generator,
        test_batch_generator=test_batch_generator
    )
    print("Training time (seconds):", time.time() - start_time)

    # Predict
    a_clip = X[0]
    prediction = model(torch.tensor(np.expand_dims(a_clip, 1)).float())
    prediction = torch.softmax(prediction, dim=1).detach().numpy()
    prediction = int(np.argmax(prediction, axis=1)[0])
    print("Predicted emotion:", GAMES[prediction])
    print("Predicted emotion (micro:bit skipped):", GAMES[prediction])

main()