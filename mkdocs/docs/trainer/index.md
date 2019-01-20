# Trainer

The trainer train a model with a dataset or subset create by you. Try execute the `Main.py` class.

## Commands 

Start finetuning in image net with the subset `imagenet_per90_porp_default` created in maker.
    
    python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default
    
    
Start finetuning in .h5 weights with the subset `imagenet_per90_porp_default` created in maker.

    python Main.py --model_name model_example_1 --load_data imagenet_per90_porp_default --load_weights <PATH_FILE>.h5  
    
    
#### Arguments

* **--model_name**: Name of model . Default `<name_dataset/name_subset>_<serial_number>`.

* **--load_model_file**: load from a .json file the model

* **--load_data**: Use a name of `dataset` or from a `subsets`.

* **--load_weights**: Load the weights to model

* **--annotation**: text annotation used you to describe the model.

