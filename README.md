# Description  

This repository contains examples on software quality, version control and research data management for the Z-INF sub-project of the [CRC 1194 at TU Darmstadt.](https://www.sfb1194.tu-darmstadt.de/sfb_1194/index.en.jsp)

# Examples

## Using pyFoam to prepare parameter variation studies in OpenFOAM 

In order to use the example, an obvious requirement is the [pyFoam](https://openfoamwiki.net/index.php/Contrib/PyFoam) package.  

The 'pyFoam' package has an application that makes it easy to generate parameter variations in OpenFOAM, called 'pyFoamRunParameterVariation.py'. It requires a set of **execution options**, a **template case** and a **parameter file** and o execute properly. 

### Execution options

A list of execution options can be generated with 'pyFoamRunParameterVariation.py --help'. The options that are related to parameter study definition are: 


    Stages
    ------
    Which steps should be executed

    --only-variables        Do nothing. Only read the variables
    --no-clear              Do not clear the case
    --no-templates          Do not rework the templates
    --no-mesh-create        Do not execute a script to create a mesh
    --no-copy               Do not copy original directories
    --no-post-templates     Do not rework the post-templates
    --no-case-setup         Do not execute a script to set initial conditions etc
    --no-final-templates    Do not rework the final-templates
    --no-template-clean     Do not clean template files from 0-directory
    --no-keep-zero-directory-from-mesh-create
                            If the script that creates the mesh generates a
                            '0'-directory with data then this data will be
                            removed. Otherwise it is kept

    Scripts
    -------
    Specification of scripts to be executed

    --mesh-create-script=MESHCREATESCRIPT
                            Script that is executed after the template expansion
                            to create the mesh. If not specified then the utility
                            looks for meshCreate.sh and executes this. If this is
                            also not found blockMesh is executed if a
                            blockMeshDict is found
    --case-setup-script=CASESETUPSCRIPT
                            Script that is executed after the original files have
                            been copied to set initial conditions or similar. If
                            not specified then the utility looks for caseSetup.sh
                            and executes this.
    --derived-parameters-script=DERIVEDPARAMETERSSCRIPT
                            If this script is found then it is executed after the
                            parameters are read. All variables set in this script
                            can then be used in the templates. Default:
                            derivedParameters.py
    --allow-derived-changes
                            Allow that the derived script changes existing values
    --continue-on-script-failure
                            Don't fail the whole process even if a script fails

    Variables
    ---------
    Variables that are automatically defined

    --number-of-processors=NUMBEROFPROCESSORS
                            Value of the variable numberOfProcessors. Default: 1

    Parameter variation
    -------------------
    Parameters specific to the parameter variation

    --inplace-execution     Do everything in the template case (preparation and
                            execution)
    --one-cloned-case-execution
                            Clone to one case and do everything in that case
                            (preparation and execution)
    --every-variant-one-case-execution
                            Every variation gets its own case (that is not erased)
    --no-execute-solver     Only prepare the cases but do not execute the solver
    --cloned-case-prefix=CLONEDCASEPREFIX
                            Prefix of the cloned cases. If unspecified the name of
                            parameter file is used
    --cloned-case-postfix=CLONEDCASEPOSTFIX
                            Postfix of the cloned cases. If unspecified an empty
                            string. Helps to distinguish different sets of
                            variations
    --clone-to-directory=CLONETODIRECTORY
                            Directory to clone to. If unspecified use the
                            directory in which the original case resides
    --single-variation=SINGLEVARIATION
                            Single variation to run
    --start-variation-number=STARTVARIATION
                            Variation number to start with
    --end-variation-number=ENDVARIATION
                            Variation number to end with
    --database=DATABASE     Path to the database. If unset the name of parameter-
                            file appended with '.results' will be used
    --create-database       Create a new database file. Fail if it already exists
    --auto-create-database  Create a new database file if it doesn't exist yet'
    --list-variations       List the selected variations but don't do anything
    --no-database-write     Do not write to the database

    ---------------------------------------


Out of all these options, a minimal set used for generating the parameter study can be used:  

    pyfoamrunparametervariation.py  --no-execute-solver --no-case-setup --no-server-process \
                                    --no-mesh-create --cloned-case-prefix=myStudy \
                                    --every-variant-one-case-execution \
                                    --create-database \
                                    myTemplateCase myParameterFile

With this configuration, only the configuration (input) files will be generated. Mesh generation, initialization, and solver execution should be handled separately. This kind of configuration can be used on a high performance cluster, where the meshing, preprocessing and running should be executed and controlled separately, namely by the workload manager. 

The minimal prepared in './pyFoamParameterStudyExample/runStudy.py' wraps above call of the 'pyFoamRunParameterVariation.py' into a python script that provides helpful information on the type of the study to be prepared and the required parameters. 

### Template case 

An template case must contain: 

    1. *.template files where the substitution of values defined in the parameter file will take place. 
    2. '0.org' directory with initial field data.


An example template case is prepared in ./pyFoamParameterStudyExample/cavity'. An example of the template file is its 'system/blockMeshDict.template', where '@!N!@' 'pyFoam' syntax marks the point of substitution with the 'N' parameter from the parameter file: 

    blocks
    (
        hex (0 1 2 3 4 5 6 7) (@!N!@ @!N!@ 1) simpleGrading (1 1 1)
    );


Same was done to the '0.org/U.template' parameter file to vary the velocity of the moving wall. 


### Parameter file

This is the syntax of the parameter file: 

    values
    {
        solver (icoFoam);

        N
        (
            4 8 16 32 64 
        );

        U
        (
            1 2 3 4 5 6
        ); 
    }


It is simple, a solver is defined with a list of parameter study vectors. 


### Running  

To run the study with the 'cavity' example template case and the 'cavity.parameter' example parameter file, under the options wrapped in the 'runStudy.py' script, execute:

```bash
    ./runStudy.py -c cavity -p cavity.parameter  -s myStudy
```

This creates the parameter directories and the parameter database:

```bash
    > ls
    cavity                     myStudy_00002_cavity  myStudy_00007_cavity  myStudy_00012_cavity  myStudy_00017_cavity  myStudy_00022_cavity  myStudy_00027_cavity
    cavity.parameter           myStudy_00003_cavity  myStudy_00008_cavity  myStudy_00013_cavity  myStudy_00018_cavity  myStudy_00023_cavity  myStudy_00028_cavity
    cavity.parameter.database  myStudy_00004_cavity  myStudy_00009_cavity  myStudy_00014_cavity  myStudy_00019_cavity  myStudy_00024_cavity  myStudy_00029_cavity
    myStudy_00000_cavity       myStudy_00005_cavity  myStudy_00010_cavity  myStudy_00015_cavity  myStudy_00020_cavity  myStudy_00025_cavity  PlyParser_FoamFileParser_parsetab.py
    myStudy_00001_cavity       myStudy_00006_cavity  myStudy_00011_cavity  myStudy_00016_cavity  myStudy_00021_cavity  myStudy_00026_cavity  runStudy.py
```


To understand which variation belongs to which parameter vector, execute


```bash
    > pyFoamRunParameterVariation.py  --list-variations cavity cavity.parameter

    ===============================
    30 variations with 2 parameters
    ===============================


    ==================
    Listing variations
    ==================

    Variation 0 : {'U': 1, 'N': 4}
    Variation 1 : {'U': 1, 'N': 8}
    Variation 2 : {'U': 1, 'N': 16}
    Variation 3 : {'U': 1, 'N': 32}
    Variation 4 : {'U': 1, 'N': 64}
    Variation 5 : {'U': 2, 'N': 4}
    Variation 6 : {'U': 2, 'N': 8}
    Variation 7 : {'U': 2, 'N': 16}
    Variation 8 : {'U': 2, 'N': 32}
```

Execution of each individual simulation on the Lichtenberg cluster can be managed easily with a one line for loop: 

```bash
    for case in myStudy_00*; do cd $case; sbatch ../blockMesh.sbatch; cd ..; done
```

Of course, the 'blockMesh.sbatch' SLURM script should be prepared and available in the study directory, as well as other SLURM scripts responsible for starting your pre-processing and running applications (solvers). 

The script can also be wrapped into a short SHELL script named for example 'bulkeval' 

```bash
    #! /usr/bin/bash

    PATTERN=$1
    CMD=$2

    for dir in "$PATTERN"*; do cd $dir; eval "$CMD" && cd ..; done 
```

This can now be used as 


```bash
    bulkeval myStudy_00 "sbatch ../blockMesh.sbatch"
```

### Reducing the parameter set (trivially)

Execute

```bash 
    pyFoamRunParameterVariation.py --list-variations cavity cavity.parameter 
```

Choose the variations that are to be generated (manually in a trivial case, or processing the variation set based on some conditions), then execute the `pyFoamRunParameterVariation.py` with the option to run an individual variation. 

An example is available in 'pyFoamParameterStudyExample/runReducedStudy.sh'.  


### Parameterizing schemes (strings with spaces between them) using aliases

OF schemes will usually have multiple values for the same parameter value. The syntax may look like this for a convection scheme 

    Gauss limited vanLeer superScheme 0.7; 

The syntax can sometimes vary the number of elements. Example, for grad schemes:  

    Gauss linear; // Two strings 

or

    pointCellsLeastSquares; // One string

If quotations are used in the parameter file:  

    gradScheme
    (
        "Gauss linear" pointCellsLeastSquares
    ); 

pyFoam complains. One way to avoid this is to rely on the macro preprocessor in OpenFOAM, and define a file with scheme aliases, for example 'pyFoamParameterStudyExample/schemeAlias': 

    // Grad schemes

    Linear  Gauss linear;
    PLSQ    pointCellsLeastSquares; 

This defines alias names for schemes, that will then all only have a single word. This file is then included and the aliases are used in an OpenFOAM configuration file. For example, in 'pyFoamParameterStudyExample/cavity/system/fvSchemes.template'

    #include "../../schemeAlias"

    ddtSchemes
    {
        default         Euler;
    }

    gradSchemes
    {
        default         Gauss linear;
        grad(p)         Gauss linear;
        grad(U)         $|-gradScheme-|;  
    }

The parameter file of the variation study now contains another vector for gradient schemes:  

    values
    {
        solver (icoFoam);

        N
        (
            16 32 64 
        );

        U
        (
            1 2 3 
        ); 

        gradScheme
        (
            Linear PLSQ
        ); 
    }
