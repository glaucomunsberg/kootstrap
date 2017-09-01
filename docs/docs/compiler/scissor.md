# Definition

`Scissor.py` open the file and cut to fit exactly in proporcions described in `scissor.json` file.

## Params

**image_url**: the image url to cut or manipulate. `type:string`

**logger**: logger used in application default value is None. `type:Logger`

## Attributes

**original_image_url** : Return the original url setted  in params.`type:Dataset` 

**original_width**: Original with of image. `type:int`

**original_height**: Original height of image. `type:int`

**image_name** : image name `type:string`

**image_url**: the url image `type:Int`

**image**: A copy of original file `type:Image`

**width**: width after processed `type:Int`

**height**: heigth after processed `type:Int`

**window_height**: width after processed rate `type:Int`

**window_width**: heigth after processed rate `type:Int`

**manipulated**: if the image was cutted `type:bol`