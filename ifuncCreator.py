import os
import sys

if len(sys.argv) != 3:
    print("Invalid Arguments")
    sys.exit(1)
    

fheader = open(sys.argv[2], "r")
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


ffunction = open(sys.argv[1], "r")
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

seperator = "\n\n// -----------------------------------------------------------------\n\n"

fresolver = open("resolver.txt", "r")                               # Using resolver.txt as iFunc resolver function
resolverFunc = fresolver.read()
fresolver.close()
resolverFunc = str(resolverFunc)

# Altering iFunc function values based on the function names in function.c file
resolverFunc = resolverFunc.replace("<<function_name>>", funcName)  
resolverFunc = resolverFunc.replace("<<function_sve2>>", funcNameSVE2)
resolverFunc = resolverFunc.replace("<<function_sve>>", funcNameSVE)
resolverFunc = resolverFunc.replace("<<function_simd>>", funcNameSIMD)

# Creating final function_altered.c filed with 3 implementations of function.c, including their pragmas and the ifunc resolver
ffunctionAltered = open("function_altered.c", "w")
ffunctionAltered.write(includeSysAux + iFuncProto + pragmaSIMD + funcOriginSIMD + 
                seperator + pragmaSVE + funcOriginSVE + 
                seperator + pragmaSVE2 + funcOriginSVE2 +
                seperator + resolverFunc)

# bash = "gcc -g -O3 main.c function_altered.c -o ifuncMain"
# os.system(bash)
