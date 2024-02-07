#include "helpers.h"
#include <math.h>

//task 1: grayscale
//we need to take an average of RGB values of pixels from the original image
//then we need to translate them into black and white values
//black pixel has a hexadecimal value of 0x00
//white pixel has a hexadecimal value of 0xff
//all of converted pixels will be in between these two b&w values

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    //the struct RGBTRIPLE is supposedly storing the RGB values for each pixel
    //RGBTRIPLE image[0][0] contains RGB values for upper-left corner pixel
    //RGBTRIPLE has an integer value for rgbtBlue, integer value for rgbtGreen
    //and integer value for rgbtRed

    //start a loop that will cycle through all pixels one at a time
    //To iterate over a two-dimensional array, you’ll need two loops, one nested inside the other.
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate the average of the given RGB integers for each pixel (in hexadecimals)
            int sum = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            float average = sum / 3.0;
            int blackwhite = round(average);

            // use that average to determine the shade of grey (update pixel value)
            image[i][j].rgbtBlue = blackwhite;
            image[i][j].rgbtGreen = blackwhite;
            image[i][j].rgbtRed = blackwhite;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    //cycle through each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // calculate the sepia formula for each color
            int Red = image[i][j].rgbtRed;
            int Blue = image[i][j].rgbtBlue;
            int Green = image[i][j].rgbtGreen;

            float sRed = (.393 * Red) + (.769 * Green) + (.189 * Blue);
            float sGreen = (.349 * Red) + (.686 * Green) + (.168 * Blue);
            float sBlue = (.272 * Red) + (.534 * Green) + (.131 * Blue);

            // rounding the new values
            int sepiaRed = round(sRed);
            int sepiaGreen = round(sGreen);
            int sepiaBlue = round(sBlue);

            //if larger than 255;
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            // assigning sepia values to original pixels
            image[i][j].rgbtBlue = sepiaBlue;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtRed = sepiaRed;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    return;
}
