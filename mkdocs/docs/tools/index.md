# Tools

The tools help you to `Fix` a dataset metadata or `Migrate` a folder of images to a valid dataset for example.

## Commands 

Lost the `metadata.json` from a dataset or subset? Try:
    
    python Main.py --mode fix --path_origin <PATH_TO_SUBSET_OR_DATASET> 
    
    
Need migrate a folder to a dataset in Kootstrap? Try:

    python Main.py --mode migrate --path_origin <PATH_FOLDER_WITH_CLASSES> --path_destiny <PATH_TO_KOOTSTRAP_FOLDER> 
    
#### Arguments

* **--mode**: Use `fix` to recovery a metadata or `migrate` to create a new metadata.

* **--path_origin**: Path origin of data, in `fix` need be a dataset ou subset. To `migrate` a folder with data to migrate.

* **--path_destiny**: Only to `migrate` you need set the Kootstrap folder.

* **--copy_way**: Only to `migrate` if set with `move` after copy will remove the original file.

* **--max_files_by_class**: Only to `migrate` set a limit to create a dataset.
