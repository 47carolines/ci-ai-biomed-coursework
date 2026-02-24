<b>Mini-project 2B: Emotion recognition with big data and large-scale neural networks</b>

<b>IMPORTANT:</b> in this project you might encounter unfamiliar code and a lot of errors. This is normal and expected. Learning how to solve these problems with generative AI is a part of the project.

 

In project 1B, you trained a small neural network to classify emotions of a single subject from the "Emotion Recognition and using EEG and Computer Games" dataset. The task for project 2B is to train several bigger models on the full dataset, utilizing the computational capabilities of FABRIC.

1. Set up a FABRIC node with an appropriate number of CPU cores and at least 10 GB of storage. Set up a conda environment like you did for project 1B and transfer the code you developed in Experiment 2.

2. Take a quick look at the full dataset on Kaggle: [Link](https://www.kaggle.com/datasets/wajahat1064/emotion-recognition-using-eeg-and-computer-games/data). You can view the dataset's files in the "Data Explorer" panel on the right. The dataset has 28 subjects labeled S01, S02, etc., and each subject has multiple data folders. The data you need for trading is located at `(Subject label)/Preprocessed/.csv format/`. You can find the information on which file corresponds to which emotion in the dataset's description on Kaggle.

3. Download the dataset to your FABRIC node. Note that the dataset occupies 2.4 GB.

4. Modify your code from Experiment 2 in the following way. Add code for reading and preprocessing the full dataset. Train and test the model. Add functionality to record train and test accuracy and train and test runtime. 

5. Starting from the architecture of Experiment 2, systematically increase the size of the network (by increasing the number of layers and/or layer size) and record train and test accuracy and runtime. Try at least 5 increments and make sure you observe an increasing trend in runtime. Collect the recorded accuracy and runtime in a table.

 
<b>To submit</b>

A single Word document with

1. The comparative table with results you recorded (at least 6 cases: baseline + 5 increments).

2. 4 plots visualizing the 4 metrics from the table.

3. A brief discussion of the results.