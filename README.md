# Blender Light Temperature Addon

## Overview

The Blender Light Temperature Addon allows you to set the color temperature for light objects directly within Blender's Data Properties panel. Once you specify the temperature, the RGB color of the light object updates automatically.

The plugin uses offers 2 ways of calculating the RGB color values from color temperature values:

- using an algorithm based on the work of Tanner Helland that approximates the RGB values for color temperatures in Kelvin. You can find it here: https://tannerhelland.com/2012/09/18/convert-temperature-rgb-algorithm-code.html
- using a table that was computed by Mitchell Charity, which shows the RGB color values for different color temperatures in the CIE 1931 and CIE 1964 color space respectively. The values between the ones in the table are approximated with linear interpolation.
See here for more info: http://www.vendian.org/mncharity/dir3/blackbody/

Drop me a note if you know about a better way.

## Features

- Adds a "Color Temperature" field in the Data Properties panel for light objects.
- Adds a bunch of Presets that cover light sources in the range from 1000K to 20000K.
- Has the option to switch between Tanner Hellands algorithm or the CIE 1931 / 1964 color space tables.
- Automatic update of the light's RGB color based on the chosen color temperature.

## Installation

1. **Download the Repository**: Click on `Code` > `Download ZIP`.

2. **Open Blender**: Launch Blender and go to `Edit > Preferences > Add-ons > Install`.

3. **Install Addon**: Navigate to the downloaded folder and select the ZIP file (should read `lighting-color-temperature-main.zip`), then click `Install Add-on`.

4. **Activate Addon**: In the Add-ons tab, you will see your addon listed. Check the box to activate it.

## Usage

1. **Select a Light Object**: In Blender, select the light object you want to modify.

2. **Navigate to Data Properties**: Go to the `Data Properties` panel.

3. **Set Temperature**: You will see a "Color Temperature" field. Enter the desired temperature value (in Kelvins) or choose a preset from the dropdown, and the RGB color of the light will automatically update.

## Contributing

Feel free to fork the project and submit pull requests for bug fixes or additional features. Please adhere to the existing coding style and comment liberally.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Blender Foundation for the amazing open-source tool.

For any issues, please [create an issue](https://github.com/esmo/lighting-color-temperature/issues) on GitHub or contact the maintainers.
