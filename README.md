# Blender Light Temperature Addon

## Overview

The Blender Light Temperature Addon allows you to set the color temperature for light objects directly within Blender's Data Properties panel. Once you specify the temperature, the RGB color of the light object updates automatically.

The plugin uses a simplified algorithm to approximate the RGB values for color temperatures in Kelvin, which was written using ChatGPT 4.0. According to ChatGPT, it is based on the concept of Planckian locus and is inspired by Tanner Helland's method. I actually don't have a clue about any of this, but it looks good.

## Features

- Adds a "Color Temperature" field in the Data Properties panel for light objects.
- Adds a bunch of Presets that cover light sources in the range from 1000K to 12000K.
- Automatic update of the light's RGB color based on the chosen color temperature.

## Installation

1. **Download the Repository**: Clone this GitHub repository to your local machine or download it as a ZIP file.

    ```
    git clone https://github.com/esmo/lighting-color-temperature.git
    ```

    Or click on `Code` > `Download ZIP`.

2. **Open Blender**: Launch Blender and go to `Edit > Preferences > Add-ons > Install`.

3. **Install Addon**: Navigate to the downloaded folder and select the Python file (`lighting-color-temperature.py`), then click `Install Add-on`.

4. **Activate Addon**: In the Add-ons tab, you will see your addon listed. Check the box to activate it.

## Usage

1. **Select a Light Object**: In Blender, select the light object you want to modify.

2. **Navigate to Data Properties**: Go to the `Data Properties` panel.

3. **Set Temperature**: You will see a "Color Temperature" field. Enter the desired temperature value (in Kelvins) and the RGB color of the light will automatically update.

## Contributing

Feel free to fork the project and submit pull requests for bug fixes or additional features. Please adhere to the existing coding style and comment liberally.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Blender Foundation for the amazing open-source tool.

For any issues, please [create an issue](https://github.com/esmo/lighting-color-temperature/issues) on GitHub or contact the maintainers.
