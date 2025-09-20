import flet as ft
from dataclasses import dataclass

# This class only exists because we apparently can't built a flet Event ourselves.
# There's no way that that's the case, I must be missing something...

@dataclass
class CustomEvent:
    value: 'typing.Any'
    control: ft.Control
