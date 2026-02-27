import os
import numpy as np
import pandas as pd
import torch
import time

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# -------------------------------------------------
# Constants
# -------------------------------------------------

SAMPLE_RATE = 32
CLIP_LENGTH = 2
CLIP_SIZE = CLIP_LENGTH * SAMPLE_RATE

games = ["boring", "calm", "horror", "funny"]

torch.manual_seed(0)
np.random.seed(0)

# -------------------------------------------------
# Dataset Path (CHANGE IF NEEDED)
# -------------------------------------------------

ROOT_DATASET_PATH = os.path.expanduser(
    "./Dataset - Emotion Recognition data Based on EEG Signals and Computer Games/Database for Emotion Recognition System Based on EEG Signals and Various Computer Games - GAMEEMO/GAMEEMO"
)

# -------------------------------------------------
# Dataset Loader
# -------------------------------------------------

def load_full_dataset(root_path):

    X_all = []
    y_all = []

    for subject_id in range(1, 29):

        subject_folder = f"(S{subject_id:02d})"

        for game_id in range(1, 5):

            csv_path = os.path.join(
                root_path,
                subject_folder,
                "Preprocessed EEG Data",
                ".csv format",
                f"S{subject_id:02d}G{game_id}AllChannels.csv"
            )

            if not os.path.exists(csv_path):
                continue

            try:
                df = pd.read_csv(csv_path)

                if "T7" not in df.columns:
                    continue

                data = df["T7"].dropna().to_numpy()

                if len(data) < CLIP_SIZE:
                    continue

                clips = np.array_split(
                    data,
                    max(1, len(data) // CLIP_SIZE)
                )

                for clip in clips:
                    if len(clip) == CLIP_SIZE:
                        X_all.append(clip)
                        y_all.append(game_id - 1)

            except Exception:
                continue

    X = np.array(X_all, dtype=float)
    y = np.array(y_all, dtype=int)

    X = np.expand_dims(X, 1)

    print("Dataset shape:", X.shape)

    return X, y

# -------------------------------------------------
# Model Builder
# -------------------------------------------------

def build_model(channels, layers):

    model_layers = []

    in_channels = 1

    for _ in range(layers):

        model_layers.append(
            torch.nn.Conv1d(
                in_channels,
                channels,
                kernel_size=4,
                padding="same"
            )
        )

        model_layers.append(torch.nn.ReLU())

        in_channels = channels

    model_layers.append(torch.nn.Flatten())

    model_layers.append(torch.nn.Linear(channels * 64, 4))
    model_layers.append(torch.nn.LogSoftmax(dim=1))

    return torch.nn.Sequential(*model_layers)

# -------------------------------------------------
# Training Function
# -------------------------------------------------

def train_model(model, train_loader, test_loader, epochs):

    optimizer = torch.optim.Adam(model.parameters(), lr=0.0001)

    train_start = time.time()

    last_train_acc = 0

    for epoch in range(epochs):

        model.train()

        train_preds = []
        train_true = []

        for X_batch, y_batch in train_loader:

            optimizer.zero_grad()

            logits = model(X_batch).squeeze()

            loss = torch.nn.functional.nll_loss(logits, y_batch)

            loss.backward()
            optimizer.step()

            pred = torch.argmax(torch.softmax(logits, dim=1), dim=1)

            train_preds.extend(pred.detach().numpy())
            train_true.extend(y_batch.numpy())

        last_train_acc = accuracy_score(train_true, train_preds)

        print(f"Epoch {epoch+1} Train Acc = {last_train_acc:.4f}")

    train_runtime = time.time() - train_start

    # Test evaluation
    model.eval()

    test_preds = []
    test_true = []

    with torch.no_grad():

        for X_batch, y_batch in test_loader:

            logits = model(X_batch).squeeze()

            pred = torch.argmax(torch.softmax(logits, dim=1), dim=1)

            test_preds.extend(pred.numpy())
            test_true.extend(y_batch.numpy())

    test_acc = accuracy_score(test_true, test_preds)

    return train_runtime, last_train_acc, test_acc

# -------------------------------------------------
# Experiment Runner
# -------------------------------------------------

def run_experiments():

    print("Loading dataset...")

    X, y = load_full_dataset(ROOT_DATASET_PATH)

    if len(X) == 0:
        print("Dataset empty.")
        return

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3
    )

    batch_size = 32

    train_loader = torch.utils.data.DataLoader(
        list(zip(
            torch.Tensor(X_train),
            torch.Tensor(y_train).long()
        )),
        batch_size=batch_size,
        shuffle=True
    )

    test_loader = torch.utils.data.DataLoader(
        list(zip(
            torch.Tensor(X_test),
            torch.Tensor(y_test).long()
        )),
        batch_size=batch_size
    )

    # Scaling experiment configs
    configs = [
        (4, 2, 10),
        (8, 2, 10),
        (16, 3, 15),
        (32, 4, 15),
        (64, 5, 20)
    ]

    results = []

    for channels, layers, epochs in configs:

        print(f"\nTraining model C={channels} L={layers}")

        model = build_model(channels, layers)

        runtime, train_acc, test_acc = train_model(
            model,
            train_loader,
            test_loader,
            epochs
        )

        results.append([
            channels,
            layers,
            runtime,
            train_acc,
            test_acc
        ])

        pd.DataFrame(
            results,
            columns=[
                "Channels",
                "Layers",
                "Runtime",
                "TrainAcc",
                "TestAcc"
            ]
        ).to_csv("results.csv", index=False)

        print("Saved results.csv")

# -------------------------------------------------

if __name__ == "__main__":
    run_experiments()