Input ← (
  &fras "data.in" # Read file
  ⊜⋕⊸∈♭∵°⋕⇡10     # Parse each string of digits
  °⊟⍉ ↯∞_2        # Split into two cols
)

P₁ ← /+⌵- ∩⍆
P₂ ← /+♭ ×⟜⊞=
∩&p ⊃P₁P₂ Input
