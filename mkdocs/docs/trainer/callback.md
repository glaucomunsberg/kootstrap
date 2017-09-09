# Definition

The `Callback.py` is extension of keras callback and provide metadatas to your model.

## Params

**model**: the model. `type:Model->Keras`

**model_metadata**: Args. `type:Metadata`

**logger**: logger used in application default value is None. `type:Logger`

## Methods

**on_epoch_begin**: Event when epoch start

**on_epoch_end**: Event when epoch finish

**on_train_begin**: Event when train start. The epoch 0 start after.

**on_train_end**: Event when train end. The last epoch was finished.