# Maker

The tester run the model generated in `Trainer` and test the predictions.

## Commands 

To use a subset of test images in a model try:
    
    python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default
    
#### Arguments

* **--model_name**: Name or path to a model in datasets folder.

* **--load_data**: Path to any subset or dataset compiled by koopstrap to test, if None we use the test set from subset of train.

* **--test_name**: Name to this test, if empty save a composition from serial number and the dataset tested

* **--epoch**: Set the epoch with weigths that you want save.

* **--classes**: if empty and --classes_load_file empty the Compiler use all classes inside the dataset. Separete classes wite comma.


* **--set**: Choose if the test will use the train, validation or test set of images on subset else selected a dateset the arg will by ignorated.

* **--annotation**: annotation.