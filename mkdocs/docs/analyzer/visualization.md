# Definition

`Visualization.py` is a class that allow you `see` the activation inside the model

## Params

**args**: the args used `type:Args`

**logger**: logger. `type:Logger`

## Attributes

**path_images** : Return the images path `type:[String]`

**path_destiny** : Return the path to top file `type:String`

**path_model_json**: Return the path model json file `type:String`

**path_model_weights**: Return the path model weights file  `type:String`

**path_test_model_visualization_file**: Return the folder where the file will by save `type:String`

**serial_number**: A serial number `type:String`

**show_both**: Show image side-by-side whit headmap `type:Boolean`

**images_list**: List of images file `type:[String]`

**model**: return the keras model used `type:Model->Keras`

**file_name_out_png**: path to file .png `type:String`

**file_name_out_list_csv**: path to list of images by class .csv `type:String`