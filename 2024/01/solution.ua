Input ← (
  &fras "data.in" # Read file
  ⊜⋕⊸∈♭∵°⋕⇡10     # Parse each string of digits
  °⊟⍉ ↯∞_2        # Split into two cols
)

# sum of absolute diffs between sorted cols
P₁ ← /+⌵- ∩⍆

# sum of right col times equality of all combinations
P₂ ← /+♭ ×⟜⊞=

∩&p ⊃P₁P₂ Input
