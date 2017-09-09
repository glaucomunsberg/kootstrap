# Definition

The `Generator.py` is responsible to create keras generator to train and validation. The job need compile under the informations inside of dataset/subset and model metadata.


## Params

**metadata_model**: metadata to model. `type:Metadata`

## Attributes

**imageDateGeneratorValidation** : The DataGenerator keras to validation set.`type:ImageDataGenerator` 

**imageDateGeneratorTrain** : The DataGenerator keras to train set `type:ImageDataGenerator`

## Methods

**getTrainGenerator**: Return the trainer generator `type:ImageDataGenerator`

**getValidationGenerator**: Return the validatior generator `type:ImageDataGenerator`