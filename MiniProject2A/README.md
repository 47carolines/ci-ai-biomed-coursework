<b>Mini-project 2A. Classification of accelerometer data using the micro:bit</b>

Develop a workflow for classifying accelerometer data recorded with the micro:bit.

1. Study the [Movement data logger](https://microbit.org/projects/make-it-code-it/movement-data-logger/) tutorial to learn about accelerometer data recording with micro:bit. These additional tutorials might be useful: [Python data logger](https://microbit.org/projects/make-it-code-it/python-wireless-data-logger/), [Sensitive step counter](https://microbit.org/projects/make-it-code-it/sensitive-step-counter/?editor=python), [User guide – Data logging](https://microbit.org/get-started/user-guide/data-logging/#what-is-data-logging?).

2. Create a MakeCode or Python script to record accelerometer data from the micro:bit to your PC. You can transfer the data either via a wire or through a radio connection.

3. Record the following movement sequence:

* Hold the micro:bit steady for 5 seconds,

* Shake the micro:bit for 5 seconds,

* Hold the micro:bit steady for 5 seconds,

* Shake the micro:bit for 5 seconds.

You should get approximately 20 seconds of recorded data.

4. Use [this notebook](https://colab.research.google.com/github/cyneuro/ML_camp/blob/main/camp_logreg_microbit.ipynb) to estimate a model for classifying whether the micro:bit is being held steady or being shaken. The notebook uses logistic regression as an example, but you are free to use any other model or create a rule-based classification system. Report the classification accuracy and give suggestions on how to improve it.