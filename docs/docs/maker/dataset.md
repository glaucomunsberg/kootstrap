# Definition

The `Dataset.py` is responsible to create the folder and metadata about dataset and the classes received from args params.


## Params

**args**: Args. `type:argparse`

**logger**: logger used in application default value is None. `type:Logger`

## Attributes

**dataset_name** : Return the name of dataset.`type:String` 

**classes** : List of classes used on dataset `type:List`

**dataset_path**: Path to dataset `type:String`

**dataset_md**: Object dataset_md `type:Metadata`

## Methods

**normalizeDatasetName**: Return the name normalized without especial caracters `type:String`

**normalizePathSubset**: Normalize the path to by a absolute path