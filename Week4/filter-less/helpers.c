#include "helpers.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>

// task 1: grayscale
// we need to take an average of RGB values of pixels from the original image
// then we need to translate them into black and white values
// black pixel has a hexadecimal value of 0x00
// white pixel has a hexadecimal value of 0xff
// all of converted pixels will be in between these two b&w values

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // the struct RGBTRIPLE is supposedly storing the RGB values for each pixel
    // RGBTRIPLE image[0][0] contains RGB values for upper-left corner pixel
    // RGBTRIPLE has an integer value for rgbtBlue, integer value for rgbtGreen
    // and integer value for rgbtRed

    // start a loop that will cycle through all pixels one at a time
    // To iterate over a two-dimensional array, you’ll need two loops, one nested inside the other.
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
    // cycle through each pixel
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

            // if larger than 255
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
    // cycle through each pixel
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < 0.5 * width; j++)
        {
            // for each pixel's width, it should be swapped
            int newvalue = width - 1 - j;

            // use temporary variable to host
            RGBTRIPLE tmp = image[i][newvalue];
            image[i][newvalue] = image[i][j];
            image[i][j] = tmp;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // creating a copy of an image
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    // cycling over pixels
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // declaring average
            float avgRed;
            float avgGreen;
            float avgBlue;

            // declaring colors
            // red
            int Red = copy[i][j].rgbtRed;
            int Red_UpL = copy[i - 1][j - 1].rgbtRed;
            int Red_Up = copy[i - 1][j].rgbtRed;
            int Red_UpR = copy[i - 1][j + 1].rgbtRed;
            int Red_RowL = copy[i][j - 1].rgbtRed;
            int Red_RowR = copy[i][j + 1].rgbtRed;
            int Red_DownL = copy[i + 1][j - 1].rgbtRed;
            int Red_Down = copy[i + 1][j].rgbtRed;
            int Red_DownR = copy[i + 1][j + 1].rgbtRed;

            // green
            int Green = copy[i][j].rgbtGreen;
            int Green_UpL = copy[i - 1][j - 1].rgbtGreen;
            int Green_Up = copy[i - 1][j].rgbtGreen;
            int Green_UpR = copy[i - 1][j + 1].rgbtGreen;
            int Green_RowL = copy[i][j - 1].rgbtGreen;
            int Green_RowR = copy[i][j + 1].rgbtGreen;
            int Green_DownL = copy[i + 1][j - 1].rgbtGreen;
            int Green_Down = copy[i + 1][j].rgbtGreen;
            int Green_DownR = copy[i + 1][j + 1].rgbtGreen;

            // blue
            int Blue = copy[i][j].rgbtBlue;
            int Blue_UpL = copy[i - 1][j - 1].rgbtBlue;
            int Blue_Up = copy[i - 1][j].rgbtBlue;
            int Blue_UpR = copy[i - 1][j + 1].rgbtBlue;
            int Blue_RowL = copy[i][j - 1].rgbtBlue;
            int Blue_RowR = copy[i][j + 1].rgbtBlue;
            int Blue_DownL = copy[i + 1][j - 1].rgbtBlue;
            int Blue_Down = copy[i + 1][j].rgbtBlue;
            int Blue_DownR = copy[i + 1][j + 1].rgbtBlue;

            // for top left pixel (4 pixels)
            if (i == 0 && j == 0)
            {
                // calculating averages
                avgRed = (Red + Red_Down + Red_RowR + Red_DownR) / 4.0;
                avgGreen = (Green + Green_Down + Green_RowR + Green_DownR) / 4.0;
                avgBlue = (Blue + Blue_Down + Blue_RowR + Blue_DownR) / 4.0;
            }

            // for top right pixel (4 pixels)
            else if (i == 0 && j == width - 1)
            {
                // calculating averages
                avgRed = (Red + Red_Down + Red_RowL + Red_DownL) / 4.0;
                avgGreen = (Green + Green_Down + Green_RowL + Green_DownL) / 4.0;
                avgBlue = (Blue + Blue_Down + Blue_RowL + Blue_DownL) / 4.0;
            }

            // for bottom left pixel (4 pixels)
            else if (i == height - 1 && j == 0)
            {
                // calculating averages
                avgRed = (Red + Red_Up + Red_RowR + Red_UpR) / 4.0;
                avgGreen = (Green + Green_Up + Green_RowR + Green_UpR) / 4.0;
                avgBlue = (Blue + Blue_Up + Blue_RowR + Blue_UpR) / 4.0;
            }

            // for bottom right pixel (4 pixels)
            else if (i == height - 1 && j == width - 1)
            {
                // calculating averages
                avgRed = (Red + Red_Up + Red_RowL + Red_UpL) / 4.0;
                avgGreen = (Green + Green_Up + Green_RowL + Green_UpL) / 4.0;
                avgBlue = (Blue + Blue_Up + Blue_RowL + Blue_UpL) / 4.0;
            }

            // for top row (6 pixels)
            else if (i == 0 && j != width - 1 && j != 0)
            {
                // calculating averages
                avgRed = (Red + Red_RowL + Red_RowR + Red_Down + Red_DownL + Red_DownR) / 6.0;
                avgGreen = (Green + Green_RowL + Green_RowR + Green_Down + Green_DownL + Green_DownR) / 6.0;
                avgBlue = (Blue + Blue_RowL + Blue_RowR + Blue_Down + Blue_DownL + Blue_DownR) / 6.0;
            }

            // for bottom row (6 pixels)
            else if (i == height - 1 && j != width - 1 && j != 0)
            {
                // calculating averages
                avgRed = (Red + Red_RowL + Red_RowR + Red_Up + Red_UpL + Red_UpR) / 6.0;
                avgGreen = (Green + Green_RowL + Green_RowR + Green_Up + Green_UpL + Green_UpR) / 6.0;
                avgBlue = (Blue + Blue_RowL + Blue_RowR + Blue_Up + Blue_UpL + Blue_UpR) / 6.0;
            }

            // for left column (6 pixels)
            else if (j == 0 && i != height - 1 && i != 0)
            {
                // calculating averages
                avgRed = (Red + Red_RowR + Red_Up + Red_UpR + Red_Down + Red_DownR) / 6.0;
                avgGreen = (Green + Green_RowR + Green_Up + Green_UpR + Green_Down + Green_DownR) / 6.0;
                avgBlue = (Blue + Blue_RowR + Blue_Up + Blue_UpR + Blue_Down + Blue_DownR) / 6.0;
            }

            // for right column (6 pixels)
            else if (j == width - 1 && i != height - 1 && i != 0)
            {
                // calculating averages
                avgRed = (Red + Red_RowL + Red_Up + Red_UpL + Red_Down + Red_DownL) / 6.0;
                avgGreen = (Green + Green_RowL + Green_Up + Green_UpL + Green_Down + Green_DownL) / 6.0;
                avgBlue = (Blue + Blue_RowL + Blue_Up + Blue_UpL + Blue_Down + Blue_DownL) / 6.0;
            }

            // center (9 pixels)
            else
            {
                // calculating averages
                avgRed = (Red + Red_RowL + Red_RowR + Red_Up + Red_UpL + Red_UpR + Red_Down + Red_DownL + Red_DownR) / 9.0;
                avgGreen =
                    (Green + Green_RowL + Green_RowR + Green_Up + Green_UpL + Green_UpR + Green_Down + Green_DownL + Green_DownR) /
                    9.0;
                avgBlue =
                    (Blue + Blue_RowL + Blue_RowR + Blue_Up + Blue_UpL + Blue_UpR + Blue_Down + Blue_DownL + Blue_DownR) / 9.0;
            }
            // assigning to the pixel
            image[i][j].rgbtBlue = round(avgBlue);
            image[i][j].rgbtGreen = round(avgGreen);
            image[i][j].rgbtRed = round(avgRed);
        }
    }
    return;
}
