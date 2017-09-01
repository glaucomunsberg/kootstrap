# Definition

`Compiler.py` is a class that cut imagens and transfer the files from dataset to subsets.

## Params

**args**: Args. `type:argparse`

## Attributes

**dataset_name** : Return the name of dataset.`type:string` 

**dataset_path** : return the path to files `type:string`

**dataset_md**: the dataset metadata `type:Metadata`

**subsets_path**: return the dataset path `type:string`

**subset_name**: name received to subsets `type:string`

**subset_path**: return the subset folder path `type:string`

**subset_md**: the metadata compiled with informations received by args the dataset path `type:Metadata`

**subset_test_path**: path to test folder of subset `type:string`

**subset_train_path**: path to train folder of subset `type:string`

**list_of_classes**: name of classes manipulated `type:string`