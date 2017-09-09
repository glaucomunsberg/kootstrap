# Definition

The `Mananger.py` is responsible mananger informations to `Trainer.py` class.


## Params

**args**: Args. `type:argparse`

**logger**: logger used in application default value is None. `type:Logger`

## Attributes

**model** : Return the model Keras loaded.`type:Model->Keras` 

**model_name** : Name of this model `type:String`

**metadata**: Return the metadata from Trainer `type:Metadata`

**path_load_subset**: Path to subset dataset/subset `type:String`

**path_model**: Path to model folder `type:String`

**path_model_test**: Path to model test folder `type:String`

**path_model_file**: Path to model file .json `type:String`

**path_model_weights_file**: Path to weights file .h5 `type:String`

**path_dataset**: Path to dataset folder `type:String`

**dataset_set_type**: Type of set. If is dataset or subset `type:String`

**files_attached_md**: Name of files used in train and validation action `type:Metadata`

## Methods

**getModel**: Return the model to train `type:Model->Keras`

**getCallbacks**: Return the `Callback.py` instance to this train `[type:Callback]`

**printModel**: Print the model

**save**: Execute the command `saveWeights` and `saveModel`

**saveWeights**: Save the wiegths from model

**saveModel**: Save the model in .json file format

**configFitGenerator**: get generators and informations used in `fit_generator` or `fit` method. `{"g_train":type:ImageDataGenerator, "g_validation":type:ImageDataGenerator, "steps_per_epoch_train":type:Int, "steps_per_epoch_validation":type:Int, "epochs":type:Int}`

