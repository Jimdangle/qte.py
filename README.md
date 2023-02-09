# qte.py
## Q : Quick
## T : Test
## E : Evaluator

made by Cal Blanco

Qte.py was made in order to help speed up the testing process for my homework assignments in CSE180. 
However the intention is to generally be able to process sequences of psql tests

Qte.py was made to be lightweight and easily usable from the command line (homeworks are done in a unix timeshare command line)


---

## Setup

1. **Config File**

Qte needs at least two *json* files to work correctly. 
One that is required before running the script is a file name `config.json` placed in the same directory as this script.
> if the config.json is not found in the same dir as qte.py the script will not work 
> more accurately, if the config is not found in the current working directory you call the script in

`config.json` instructs qte.py on how to connect to the psql server. You should have access to all of this information when you connect to psql through the terminal. 

your config should look like this
```
 {
  "username": <username for account>,
  "password": <password for acc>,
  "host": <host for db>,
  "port": <port for host>,
  "dbname": <database name>
 }
```

I've included a default config with the host and port already filled out for the class. 

**One thing of note: for me my username and dbname were the same : i used 'wcblanco' for both**

2. **Manifest Files**


Once we have a config file we can begin to run tests. In order to tell qte.py how to run the tests we will need to make some `manifests`. All these are, are json files with a specific format.

*example manifest.json**
```
{
    "name": "test_manifest",
    "root": "/afs/cats.ucsc.edu/users/g/wcblanco/Lab2",
    "tests":
    {
        "test1":
        {
            "load": "load.sql",
            "steps": 
            [
                "query1.sql",
                "query2.sql",
                "query3.sql"
            ]
        },
        "test2":
        {
            "load": "lab2tests/load_query1.sql",
            "steps":[ "query1.sql"]
        }

    }
}
```

The `name` tells qte.py what you would like this particular test sequence to be called and determines the name of the output file as well as some other internal features.

`root` tells qte.py where to look for all of the files you will specify in your tests. So make sure to place all of your testing files, and sql files with some common ancenstor as the root.

`tests` tell qte.py which tests should be run and in what order to run them. 

**name, root, and tests** must all be spelled exactly as they are in your file

Inside of the `tests` attribute we can name our tests what ever we want, however `load` and `steps` must appear

example test

```
"test_name":
        {
            "load": "loadfilename.sql",
            "steps": 
            [
                "step1_filename.sql",
                ...,
                "stepn_filename.sql
                
            ]
        }
```

`load` specifies what file to load into the database before running the tests. So if you were to use the given load data for lab2 you would specify the name relative to the root file. 


---

## Usage
Now that we have our files loaded up usage is fairly straight forward.

*assuming you have qte.py, a config.json, and the path to the manifest you want to run all in your timeshare*

To run qte.py type `python3 qte.py <path_to_manifest>` and it will generate and run your tests on the database. 

`path_to_manifest` can be relative or absolute. So you can place the manifest in the same dir as qte.py or somewhere else. Just be careful to ensure the relative path you provide is accurate.

In order to view results just type in `less <manifest_name>_qte.txt`













