import flet as ft

class CustomSwitch(ft.Switch):
    def __init__(
        self,
        options,
        label,
        property,
        *,
        init_enabled = True,
        user_on_change = None
    ):

        self.options = options
        self.property = property
        self.user_on_change = user_on_change

        super().__init__(
            label = f"  {label}", # Use leading whitespace to compensate for lack of padding
            value = init_enabled,

            on_change = lambda _ : self.on_change_sum()
        )

    def builtin_on_change(self):
        setattr(self.options, self.property, self.value)

    # TODO : Factorize this from NumberInput
    def on_change_sum(self):
        self.builtin_on_change()

        if self.user_on_change is not None:
            self.user_on_change(None)
