# Tools

The tools help you to `Fix` a dataset metadata or `Migrate` a folder of images to a valid dataset for example.

## Commands 

Lost the `metadata.json` from a dataset or subset? Try:
    
    python Main.py --mode fix --path_origin <PATH_TO_SUBSET_OR_DATASET> 
    
    
Need migrate a folder to a dataset in Kootstrap? Try:

    python Main.py --mode migrate --path_origin <PATH_FOLDER_WITH_CLASSES> --path_destiny <PATH_TO_KOOTSTRAP_FOLDER> 
    
Copy or move files to inside a dataset? Try:
    
    python Main.py --mode transfer --path_origin <PATH_FOLDER_WITH_CLASSES> --path_destiny <PATH_TO_KOOTSTRAP_FOLDER> 
    
#### Arguments

* **--mode**: Use `fix` to recovery a metadata, `migrate` to create a new metadata or `transfer` to move files.

* **--path_origin**: Path origin of data, in `fix` need be a dataset ou subset. To `migrate` or `transfer` a folder with data to migrate.

* **--path_destiny**: On `migrate` you need set the Kootstrap folder and `transfer` any folder.

* **--copy_way**: To `migrate` or `transfer` if set with `move` after copy will remove the original file.

* **--max_files_by_class**: To `migrate` or `transfer` set a limit to create a dataset.
