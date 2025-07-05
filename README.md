# LogicEdu

A Python library for creating digital logic circuit animations using [Manim](https://www.manim.community).

## Overview

LogicEdu provides building blocks for creating educational animations of digital logic circuits, computer architecture diagrams, and data flow visualizations. It's built on top of [Manim](https://www.manim.community) and offers a set of components commonly found in digital logic and computer architecture.

## Features

- **Digital Logic Gates**: AND, OR, NOT, NAND, NOR, XOR, XNOR, and more
- **Computer Architecture Components**: ALU, Register File, Memory, Control Units
- **Data Path Elements**: Multiplexers, Adders, Shifters, Sign Extenders
- **Connector System**: Flexible wiring with Manhattan routing support
- **Animation Utilities**: Pre-built animations for circuit construction and data flow

## Installation from source

Install `uv` as instructed by [Manim Community](https://docs.manim.community/en/stable/installation/uv.html#installing-manim-locally).

```bash
git clone https://github.com/BooneJS/logicedu.git
cd logicedu
uv venv
source .venv/bin/activate
uv pip install -e .
```

Try rendering the [examples/demo.py](examples/demo.py) Scene to check the installation.

`manim -pqh logicedu/examples/demo.py Demo`

## Quick Start

```python
from manim import Scene, Create
from logicedu import ALUZ, RegisterFile, ConnectorLine

class MyCircuit(Scene):
    def construct(self):
        # Create an ALU
        alu = ALUZ()
        self.play(Create(alu))
        
        # Create a register file
        regfile = RegisterFile()
        self.play(Create(regfile))
        
        # Connect them
        rf_readdata1_pin = regfile.get_output_by_label("ReadData1")
        if rf_readdata1_pin is None:
            raise ValueError("ReadData1 output pin not found")
        wire = ConnectorLine(
            start_pin=rf_readdata1_pin,
            end_pin=alu.get_input_by_index(0),
            manhatten=True
        )
        self.play(Create(wire))
```

## Documentation

- For additional documentation on LogicEdu, visit [docs/README.md](docs/README.md).
- Since LogicEdu is a set of classes for common logical and architectural shapes on top of Manim, most documentation a user will want to review comes from [Manim Community Docs](https://docs.manim.community/en/stable/).

## Examples

Check out the `examples/` directory for complete animation scripts:

- `examples/cod6_fig4_17.py` - Computer Organization and Design Figure 4.17
- `examples/demo.py` - Component showcase
- `examples/basic_circuits.py` - Simple logic gate examples

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details.

## License

This project is licensed under the Apache License, Version 2.0 - see the [LICENSE](LICENSE) file for details.

## References

1. _Computer Organization and Design, 6th Edition (MIPS)_, David A. Patterson & John L. Hennessy. [Elsevier Book Companion Site][1]

[1]: https://www.elsevier.com/books-and-journals/book-companion/9780128201091
