#!/usr/bin/env python 

from optparse import OptionParser
from subprocess import call

help_text = """

Runs the pyFoamRunParameterVariation.py to generate a parameter study suitable for the execution on a cluster. 

Uses the folloving options:  


- '--no-execute-solver' : do not start the solver in serial.
- '--no-case-setup': do not execute case setup scripts. 
- '--no-server-process': do not start a server process. 
- '--no-mesh-create': do not create the mesh. 
- '--every-variant-one-case-execution': every parameter variation is a new case directory.
- '--create-database': create the database to enable listing variations. 

"""

parser = OptionParser(usage=help_text)

parser.add_option("-c", "--templateCase", dest="templateCase",
                  help="Template case name.") 

parser.add_option("-p", "--parameterFile",
                  dest="parameterFile", help="Parameter file.")

parser.add_option("-s", "--studyName",
                  dest="studyName", help="Name of the parameter study.")

(options, args) = parser.parse_args()

if not options.templateCase:   
    parser.error('Template case not given.')

if not options.parameterFile:   
    parser.error('Parameter file not given.')

templateCase=options.templateCase
parameterFile=options.parameterFile
studyName=options.studyName

call (['pyFoamRunParameterVariation.py', '--no-execute-solver', '--no-case-setup', 
       '--no-server-process', '--no-mesh-create', "--cloned-case-prefix=%s" % studyName, 
       '--every-variant-one-case-execution', '--create-database', 
       templateCase, parameterFile]) 

