#include "bmp.h"

//typedef struct RGBTRIPLE named image has two arrays – height and width
//image[0] would be the first row, image [0][0] is upper-left corner pixel

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width]);

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width]);

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width]);

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]);
