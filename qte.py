import math
import json
import os
import sys
import time


# translates json manifests into a psql script that can be ran
class Manifest:
    def __init__(self,path):
        self.path = path # store path for reference later 
        self.tranlation = ''
        self.root = ''
        self.name = ''
        self.tests = {}

        with open(path) as mfp: #load in data
            self.data = json.load(mfp)
        
        self.root = self.data['root']
        self.name = self.data['name']
        self.tests = self.data['tests']

        self.translate_manifest()
        
    #take in the given files and generate the tests
    #in order to make this work remotely or locally I could read all the files now and 
    # spit them into a sql doc
    # or if i just make it a local thing i can skip reading the files
    def translate_manifest(self):
        #tstring = test string
        tstring = f'\o  {self.name}_qte.txt\n'
        tstring += f'\qecho \'{makebar(40,"$")}\'\n'
        tstring += f'\qecho \'QTE Generated Test\\nName: {self.name}\'\n' #adding title line
        tstring += f'\qecho \'{makebar(40,"$")}\\n\'\n'
        for test in self.tests:
            tstring += f'\qecho \'{test}\\nLoading data from : {self.tests[test]["load"]}\\n\'\n'
            tstring += f'\i {self.root}/{self.tests[test]["load"]}\n'
            tstring += '\qecho \'\''
            i = 0
            for step in self.tests[test]["steps"]:
                tstring += f'\qecho \'STEP{i}\'\n'
                tstring += f'\i {self.root}/{step}\n'
                tstring += "\qecho \'\'\n"
                i+=1
            tstring += '\qecho \'End Test\'\n'
            tstring += f'\qecho \'{makebar(40,"$")}\\n\'\n'

        tstring += '\o'
        self.tranlation = tstring
    
    def make_test(self):
        with open(f'{self.name}.sql','w') as sql:
            sql.write(self.tranlation)

        return


#helpful text utility
def makebar(size, fill):
    return str.ljust('',size,fill)

# this was made for a no longer good idea but still kinda cool so i didnt delete it 
def centertxt(size, text, border):
    lpad = math.floor((size-len(text))/2)-1 #for border
    rpad = math.ceil((size-len(text))/2)-1 # for border
    return (f'{border}{str.ljust("",lpad," ")}{text}{str.ljust("",rpad," ")}{border}')


#con string : postgresql://wcblanco:wint22poopsql99@cse180-db.lt.ucsc.edu:5432/wcblanco

default_config_path = 'config.json'

# a wrapper to make sure the manifests have a config to execute the tests
class Builder:
    def __init__(self):
        self.manifest = None
        self.config = {}

        with open(default_config_path) as cfp:
            self.config = json.load(cfp)


    #make the test, and connstring
    # run the test using the connstring
    def run_manifest(self, mani_path):
        mani = Manifest(mani_path)
        mname = mani.name

        print('making test...')
        mani.make_test()
        time.sleep(0.5)
        print('running test')

        os.system(f'psql -c \'\i {mname}.sql\' {self.build_conn_string()}')
        print('test done!')
        print(f'type \'more {mname}_qte.txt\' to view results')

   #build psql connection string
    def build_conn_string(self):
        if self.config:
            return f'postgresql://{self.config["username"]}:{self.config["password"]}@{self.config["host"]}:{self.config["port"]}/{self.config["dbname"]}'
        else:
            return ''



if len(sys.argv) > 1:
    fpath = sys.argv[1]
    
    if fpath.find('.json') <0:
        print('invalid manifest')
        quit()
    else:
        B = Builder()
        B.run_manifest(fpath)
        quit()

