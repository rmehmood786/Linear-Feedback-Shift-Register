# LFSR.py
"""
COM6014 – Practical Task 1
Linear Feedback Shift Register (LFSR)

This file contains:
1) A GENERAL, reconfigurable LFSR class (size, taps, state) with methods to
   set/get parameters and to emit the next stream bit (which updates state).
2) A BASIC 4-bit LFSR demo that matches the lecture example:
   - size n = 4
   - taps = [3, 2] (Fibonacci form; 0 = LSB)
   - output bit is the LSB (R0)
   - initial state = 0b0110
   The program prints the (state, next_bit) 30 times. The first 15 states
   then repeat (period = 2^4 - 1 = 15) and the next_bit equals the R0 bit.

Conventions (Fibonacci form, right-shift):
- State is an n-bit integer (0 < state < 2^n).
- Output bit = LSB (bit 0) before shifting.
- Feedback bit = XOR of the positions given by `taps` (0-based; 0 = LSB).
- New state = (state >> 1) | (feedback << (n-1)).

Author: Rashid Mehmood
License: MIT
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Tuple, List


def _parity(x: int) -> int:
    """Return XOR parity (0 or 1) of integer x."""
    return x.bit_count() & 1


@dataclass
class LFSR:
    """
    General (reconfigurable) Fibonacci LFSR.

    Methods you’ll use for the assignment:
      - set_size(n), get_size()
      - set_state(s), get_state()
      - set_taps(taps), get_taps()
      - next_bit()  -> int   (emits next stream bit and updates state)

    Indexing:
      taps are zero-based bit positions in the CURRENT state.
      Example: taps=(3,2) for a 4-bit LFSR gives the classical maximal period.

    Example:
        l = LFSR(n=4, state=0b0110, taps=(3,2))
        for _ in range(3):
            print(l.get_state_bits(), l.next_bit())
    """
    n: int
    state: int
    taps: Tuple[int, ...] = (3, 2)  # default to the classic 4-bit maximal taps

    def __post_init__(self) -> None:
        self.set_size(self.n)
        self.set_state(self.state)
        self.set_taps(self.taps)

    # ----- setters/getters required by the brief -----

    def set_size(self, n: int) -> None:
        if n <= 1:
            raise ValueError("n must be > 1")
        self.n = int(n)
        # mask to keep state within n bits
        self._mask_n = (1 << self.n) - 1

    def get_size(self) -> int:
        return self.n

    def set_state(self, s: int) -> None:
        if not isinstance(s, int):
            raise TypeError("state must be int")
        if s <= 0 or s >= (1 << self.n):
            raise ValueError(f"state must be in [1, 2^n - 1]; got {s}")
        self.state = s & self._mask_n

    def get_state(self) -> int:
        return self.state

    def get_state_bits(self) -> str:
        """Return state as zero-padded binary string of width n (R_{n-1}...R0)."""
        return format(self.state, f"0{self.n}b")

    def set_taps(self, taps: Iterable[int]) -> None:
        ts = tuple(int(t) for t in taps)
        if any(t < 0 or t >= self.n for t in ts):
            raise ValueError(f"tap positions must be within 0..{self.n-1}")
        self.taps = ts
        # precompute a tap mask for speed
        self._tap_mask = 0
        for t in self.taps:
            self._tap_mask |= (1 << t)

    def get_taps(self) -> Tuple[int, ...]:
        return self.taps

    # ----- core operation -----

    def next_bit(self) -> int:
        """
        Emit the next stream bit (LSB before shift) and update the register.
        This is the 'get next stream bit' required in the brief.
        """
        out = self.state & 1
        fb = _parity(self.state & self._tap_mask)  # XOR of tapped bits
        self.state = ((self.state >> 1) | (fb << (self.n - 1))) & self._mask_n
        return out

    # ----- extras (useful but not required) -----

    def period(self, limit: int | None = None) -> int:
        """
        Return the cycle length before the state repeats (<= 2^n - 1).
        """
        start = self.state
        seen = set([start])
        steps = 0
        max_steps = (1 << self.n) - 1 if limit is None else int(limit)
        while steps < max_steps:
            self.next_bit()
            steps += 1
            if self.state == start:
                return steps
            if self.state in seen:  # safety for non-maximal polynomials
                return steps
            seen.add(self.state)
        return steps

    def bits(self, k: int) -> List[int]:
        """Convenience: emit k bits."""
        return [self.next_bit() for _ in range(k)]


# -------------------------- BASIC DEMO (Section 2) ----------------------------

def basic_demo() -> None:
    """
    Implements Section 2 of the brief:
      - size = 4, taps hard-wired (3,2), initial state = 0110
      - print (state, next_bit) 30 times
      - observe that 15 states repeat (period = 15)
      - next_bit equals the LSB (R0) of the printed state
    """
    l = LFSR(n=4, state=0b0110, taps=(3, 2))  # classic 4-bit maximal LFSR
    print("Basic LFSR (n=4, taps=[3,2], init=0110) — 30 iterations")
    print("Iter  State  NextBit(R0)")
    print("-------------------------")
    first_state = l.get_state()
    for i in range(1, 31):
        s_bits = l.get_state_bits()
        next_bit = l.next_bit()
        print(f"{i:>2}    {s_bits}      {next_bit}")

    # sanity notes for the marker (not required, but helpful)
    # After 15 steps we should return to the initial state (period = 15).
    l2 = LFSR(n=4, state=0b0110, taps=(3, 2))
    per = l2.period()
    print("\nNotes:")
    print(f"- Observed period (should be 15): {per}")
    print("- NextBit is always the LSB of the 'State' column.")


# -------------------------- GENERAL DEMO (Section 3) --------------------------

def general_demo() -> None:
    """
    Section 3 demonstration:
    - Shows using the reconfigurable class to instantiate the basic LFSR.
    - Also shows changing size/taps/state via the provided methods.
    """
    # Instantiate to the basic example (a)
    l = LFSR(n=4, state=0b0110, taps=(3, 2))
    print("\nGeneral LFSR instantiated as the basic version:")
    print(f"size={l.get_size()}, taps={l.get_taps()}, state={l.get_state_bits()}")

    # Change configuration (e.g., a 7-bit maximal LFSR taps=(6,5))
    l.set_size(7)
    l.set_taps((6, 5))       # x^7 + x^6 + 1 (maximal)
    l.set_state(0b1010011)
    print(f"Reconfigured: size={l.get_size()}, taps={l.get_taps()}, state={l.get_state_bits()}")
    print("First 10 bits from this configuration:", "".join(str(b) for b in l.bits(10)))


# ------------------------------ script entry ----------------------------------

if __name__ == "__main__":
    # No CLI args needed: pressing Run will execute the required basic demo.
    basic_demo()
    # Optional: also show the general class usage
    general_demo()
