# Display

While not part of the actual CPU design, I have included a simple display in the main circuit as a basic I/O device.

The display is connected to the output bus. It has a resolution of 64x32 pixels.

Each column is divided into 4 8-bit banks.
We first select a column and the corresponding row bank, then send the pixel values for that bank.

Finally, we load these changes to our display buffer

| Task | Syntax |
|---|---|
| Select Row Bank and Column index | `01[row bank:2][column index: 6]` |
| Fill row data | `10[row data:8]` |
| Load to buffer | `1100000000` |

## Examples

- [dot.S](https://github.com/rnayabed/sutra-1/blob/master/examples/dot.S)

## Shilpi

I have included a simple companion program that can generate program to print something on the display. 

### Usage

```
usage: shilpi [-h] [-v] [-o OUTPUT] [-t] [input]

Simple pixel drawer from the Sutra-1 System

positional arguments:
  input                Input text or file

options:
  -h, --help           show this help message and exit
  -v, --version        Version and copyright information
  -o, --output OUTPUT
  -t, --text
```

### Text mode

```shell
python shilpi.py -t "namaste world"
```

This generates an output assembly file with the name `display-image.S` which can then be compiled by rochoyita

```shell
python rochoyita.py display-image.S
```

This will generate an output file `display-image.hex` that can then be loaded to memory in our `main` circuit inside Logisim Evolution

<img src="https://raw.githubusercontent.com/rnayabed/sutra-1/refs/heads/master/screenshots/shilpi-text.png" alt="Shilpi text mode screenshot">

### Image mode

We can also provide it a 64x32 1-bit image formatted with pixel ON as '#' and OFF as '.'. A blank template is provided in `examples/images/blank.txt`

I have also included some 1-bit images in `examples/images` that can be parsed by shilpi and rendered on Sutra-1

```shell
python shilpi.py examples/images/india.txt
```

This generates an output assembly file with the name `display-image.S` which can then be compiled by rochoyita

```shell
python rochoyita.py display-image.S
```

This will generate an output file `display-image.hex` that can then be loaded to memory in our `main` circuit inside Logisim Evolution

<img src="https://raw.githubusercontent.com/rnayabed/sutra-1/refs/heads/master/screenshots/shilpi-image.png" alt="Shilpi image mode screenshot">