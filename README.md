# Virtual Keyboard

## Installation

1. Clone the repository:
```
git clone https://github.com/your-username/virtual-keyboard.git
```
2. Install the required dependencies:
```
pip install opencv-python cvzone pynput numpy
```

## Usage

1. Run the `virtualkeyboard.py` script:
```
python virtualkeyboard.py
```
2. The virtual keyboard will be displayed on the screen.
3. Use your hand gestures to interact with the keyboard:
   - Move your index finger to hover over the desired key.
   - Bring your index and middle fingers close together to "click" the key.
4. The typed text will be displayed at the bottom of the screen.

## API

The `virtualkeyboard.py` file contains the following functions:

- `drawAll(img, buttonList)`: Draws the virtual keyboard buttons on the image.
- `Button(pos, text, size)`: Represents a single button on the virtual keyboard.


## License

This project is licensed under the [MIT License](LICENSE).

## Testing

To run the tests, execute the following command:
```
python -m unittest discover tests
```
