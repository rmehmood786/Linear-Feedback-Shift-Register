# Linear Feedback Shift Register (LFSR)

A clean and experimental implementation of a **Fibonacci LFSR** in Python with:

- a **basic 4-bit demo** (prints 30 iterations exactly as in COM6014 Task 1),
- a **general, reconfigurable LFSR class** (size/taps/state),
- and an optional helper to compute **percentage agreement** between a generated stream and a reference sequence.

> **Conventions (Fibonacci, shift-right)**
>
> - State is an `n`-bit integer, `0 < state < 2^n`.
> - **Output bit** = LSB (R0) before shifting.
> - **Feedback bit** = XOR parity of the **tap positions** (0-based; `0 = LSB`) in the current state.
> - New state:  
>   `state = (state >> 1) | (feedback << (n - 1))`.

---

## ✨ Features

- **Basic 4-bit LFSR demo**: `n=4`, taps `(3,2)`, initial state `0b0110`; prints `State` and `NextBit(R0)` for **30** iterations.  
  (The first **15** states repeat — period = `2^4 − 1 = 15`.)
- **General LFSR class**:
  - set/get **size**, **state**, **tap sequence**
  - **next_bit()** updates state and returns the next stream bit
  - convenience methods: **period()**, **bits(k)**, **get_state_bits()**
- **Percentage agreement** utility (optional): compare a generated bitstream with a reference file.

---

## 📦 Requirements

- Python **3.10+**
- No external dependencies

---

## 🚀 Quickstart

Clone and run:

```bash
git clone https://github.com/rmehmood786/Linear-Feedback-Shift-Register.git
cd Linear-Feedback-Shift-Register

# Run the assignment demos (basic + general)
python LFSR.py
