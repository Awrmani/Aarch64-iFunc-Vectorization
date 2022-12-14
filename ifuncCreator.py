#!/usr/bin/python3

import os
import sys

if len(sys.argv) < 2:
    print("------------------------------Invalid Arguments------------------------------\n")
    print("This Program Requires at least 1 function to operate correctly\n")
    print("Add as many function files as needed after ./ifuncCreator\n")
    print("Example: ./ifuncCreator function.c function1.c function2.c ...\n")
    print("Note: As seen in the example above, function header files should not be included in the run command\n\n")
    print("Function header files may or may not be existant in the same directory\n")
    print("Existant header files will not be modified, but they should have the same name as the function file with .h extension\n")
    print("Non-existant header files will be automatically generated using makeheaders feature\n")
    print("generated header file will have the same name as the function file with .h extension and it will include the function prototype\n")
    print("It is necessary for main.c and resolver.txt files to be existant in the same directory\n")
    print("main.c file will not be modified, instead main_test.c will be created and used with the gcc compiler\n")
    print("For more information please visit:\n")
    print("     https://github.com/Awrmani/Aarch64-iFunc-Vectorization\n")
    print("     https://armanvalaee.wixsite.com/arman-valaee-asr/blog\n")
    print("------------------------------Enjoy Using This Tool------------------------------")
    
    
    sys.exit(1)
    
main = open("main.c", "r")
mainContent = main.read()
main.close()
mainIncludes = "// Auto Generated Header File Includes\n"
runScript = "gcc -g -O3 main_test.c "
seperator = "\n\n// -----------------------------------------------------------------\n\n"

function_altered = []
idx = -1
for num in sys.argv:
    
    if (idx == -1):                                                     # Ignore first input          
        idx += 1
        continue
    
    if (num == "compile"):
        break
    
    funcFile = num.split(".")[0]                                        # Find function name and store as string - remove .c
    funcHeader = funcFile + ".h"                                        # Add .h to the function name
    
    if (os.path.isfile(funcHeader) == False):                           # Create the header file if non-existant
        makeFuncHeader = "makeheaders " + num
        os.system(makeFuncHeader)
    

    fheader = open(funcHeader, "r")
    proto = fheader.read()
    fheader.close()
    proto = str(proto)

    start = proto.find("*/")
    end = proto.find(";")
    proto = proto[start + 3 : end + 1]                                  # Original function prototype

    start = proto.find(" ")
    end = proto.find("(")
    funcName = proto[start + 1 : end]                                   # Original function name

    # Adjusting function names based on different implementations
    funcNameSIMD = funcName + "_SIMD"
    funcNameSVE = funcName + "_SVE"
    funcNameSVE2 = funcName + "_SVE2"


    ffunction = open(num, "r")
    funcOrigin = ffunction.read()
    ffunction.close()
    funcOrigin = str(funcOrigin)                                        # Original function.c file content

    includeSysAux = "#include <sys/auxv.h>\n\n"
    iFuncProto = '__attribute__ (( ifunc("resolve_' + funcName + '") )) ' + proto  # Function prototype with the added assembly ifunc attribute

    funcOriginSIMD = funcOrigin.replace(funcName, funcNameSIMD)
    pragmaSIMD = '\n\n#pragma GCC target "arch=armv8-a"\n\n'            # Pragma Used for SIMD function

    funcOriginSVE = funcOrigin.replace(funcName, funcNameSVE)
    pragmaSVE = '\n\n#pragma GCC target "arch=armv8-a+sve"\n\n'         # Pragma Used for SVE function

    funcOriginSVE2 = funcOrigin.replace(funcName, funcNameSVE2)
    pragmaSVE2 = '\n\n#pragma GCC target "arch=armv8-a+sve2"\n\n'       # Pragma Used for SVE2 function

    fresolver = open("resolver.txt", "r")                               # Using resolver.txt as iFunc resolver function
    resolverFunc = fresolver.read()
    fresolver.close()
    resolverFunc = str(resolverFunc)

    # Altering iFunc function values based on the function names in function.c file
    resolverFunc = resolverFunc.replace("<<function_name>>", funcName)  
    resolverFunc = resolverFunc.replace("<<function_sve2>>", funcNameSVE2)
    resolverFunc = resolverFunc.replace("<<function_sve>>", funcNameSVE)
    resolverFunc = resolverFunc.replace("<<function_simd>>", funcNameSIMD)

    function_altered.append(funcFile + "_altered.c")
    # Creating final function_altered.c filed with 3 implementations of function.c, including their pragmas and the ifunc resolver
    ffunctionAltered = open(function_altered[idx], "w")
    ffunctionAltered.write(includeSysAux + iFuncProto + pragmaSIMD + funcOriginSIMD + 
                    seperator + pragmaSVE + funcOriginSVE + 
                    seperator + pragmaSVE2 + funcOriginSVE2 +
                    seperator + pragmaSIMD + seperator + resolverFunc)
    ffunctionAltered.close()
    
    
    newMain = open("main_test.c", "w")
    mainIncludes = mainIncludes + '#include "' + funcHeader + '"\n'
    newMain.write(mainIncludes)
    newMain.close()
    runScript += function_altered[idx] + " "
    idx += 1

newMain = open("main_test.c", "w")
newMain.write(mainIncludes + seperator + mainContent)
newMain.close()

runScript += "-o ifuncMain"

if (sys.argv[-1] == "compile"):
    print("Using command: ")
    print(runScript)
    os.system(runScript)
else:
    print("Altered function(s) using iFunc Resolver have been created\n")
    print("Use the following command tu compile your program:\n")
    print("     gcc -g -o3 main_test.c function_altered.c function1_altered.c ... -o ifuncMain\n\n")
    print("Note: If you plan on using your original main function instead of the main_test.c,\n")
    print("(which is a copy of the original main.c + header files added on top), use main.c instead of main_test.c in the above commands.")
    