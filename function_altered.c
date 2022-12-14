#include <sys/auxv.h>

__attribute__ (( ifunc("resolve_adjust_channels") )) void adjust_channels(unsigned char *image,int x_size,int y_size,float red_factor,float green_factor,float blue_factor);

#pragma GCC target "arch=armv8-a"

/*
        
        adjust_channels_SIMD :: adjust red/green/blue colour channels in an image
        
        The function returns an adjusted image in the original location.
        
        Copyright (C)2022 Seneca College of Applied Arts and Technology
        Written by Chris Tyler
        Distributed under the terms of the GNU GPL v2
        
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// ----------------------------------------------------------------- Naive implementation in C

#include <sys/param.h>

void adjust_channels_SIMD(unsigned char *image, int x_size, int y_size, 
        float red_factor, float green_factor, float blue_factor) {

        printf("Using adjust_channels_SIMD() implementation #1 - Naive (autovectorizable)\n");
        
/*

        The image is stored in memory as pixels of 3 bytes, representing red/green/blue values.
        Each of these values is multiplied by the corresponding adjustment factor, with 
        saturation, and then stored back to the original memory location.
        
        This simple implementation causes int to float to int conversions.
        
*/

        for (int i = 0; i < x_size * y_size * 3; i += 3) {
                image[i]   = MIN((float)image[i]   * red_factor,   255);
                image[i+1] = MIN((float)image[i+1] * blue_factor,  255);
                image[i+2] = MIN((float)image[i+2] * green_factor, 255);
        }
}



// -----------------------------------------------------------------



#pragma GCC target "arch=armv8-a+sve"

/*
        
        adjust_channels_SVE :: adjust red/green/blue colour channels in an image
        
        The function returns an adjusted image in the original location.
        
        Copyright (C)2022 Seneca College of Applied Arts and Technology
        Written by Chris Tyler
        Distributed under the terms of the GNU GPL v2
        
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// ----------------------------------------------------------------- Naive implementation in C

#include <sys/param.h>

void adjust_channels_SVE(unsigned char *image, int x_size, int y_size, 
        float red_factor, float green_factor, float blue_factor) {

        printf("Using adjust_channels_SVE() implementation #1 - Naive (autovectorizable)\n");
        
/*

        The image is stored in memory as pixels of 3 bytes, representing red/green/blue values.
        Each of these values is multiplied by the corresponding adjustment factor, with 
        saturation, and then stored back to the original memory location.
        
        This simple implementation causes int to float to int conversions.
        
*/

        for (int i = 0; i < x_size * y_size * 3; i += 3) {
                image[i]   = MIN((float)image[i]   * red_factor,   255);
                image[i+1] = MIN((float)image[i+1] * blue_factor,  255);
                image[i+2] = MIN((float)image[i+2] * green_factor, 255);
        }
}



// -----------------------------------------------------------------



#pragma GCC target "arch=armv8-a+sve2"

/*
        
        adjust_channels_SVE2 :: adjust red/green/blue colour channels in an image
        
        The function returns an adjusted image in the original location.
        
        Copyright (C)2022 Seneca College of Applied Arts and Technology
        Written by Chris Tyler
        Distributed under the terms of the GNU GPL v2
        
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

// ----------------------------------------------------------------- Naive implementation in C

#include <sys/param.h>

void adjust_channels_SVE2(unsigned char *image, int x_size, int y_size, 
        float red_factor, float green_factor, float blue_factor) {

        printf("Using adjust_channels_SVE2() implementation #1 - Naive (autovectorizable)\n");
        
/*

        The image is stored in memory as pixels of 3 bytes, representing red/green/blue values.
        Each of these values is multiplied by the corresponding adjustment factor, with 
        saturation, and then stored back to the original memory location.
        
        This simple implementation causes int to float to int conversions.
        
*/

        for (int i = 0; i < x_size * y_size * 3; i += 3) {
                image[i]   = MIN((float)image[i]   * red_factor,   255);
                image[i+1] = MIN((float)image[i+1] * blue_factor,  255);
                image[i+2] = MIN((float)image[i+2] * green_factor, 255);
        }
}



// -----------------------------------------------------------------



#pragma GCC target "arch=armv8-a"



// -----------------------------------------------------------------

// Resolver function - this function picks which of the
// implementations will be executed when foo() is called
//
// The resolver function is only run once, the first time
// that foo() is called.
//
static void (*resolve_adjust_channels(void)) {
	// Each of these two variables is populated with
	// a bitfield indicating specific hardware 
	// capabilities. hwcaps includes a bit for SVE,
	// and hwcaps2 includes a bit for SVE2
	//
	long hwcaps  = getauxval(AT_HWCAP);
	long hwcaps2 = getauxval(AT_HWCAP2);

	printf("\n### Resolver function - selecting the implementation to use for adjust_channels()\n");
	if (hwcaps2 & HWCAP2_SVE2) {
		return adjust_channels_SVE2;
	} else if (hwcaps & HWCAP_SVE) {
		return adjust_channels_SVE;
	} else {
		return adjust_channels_SIMD;
	}
};