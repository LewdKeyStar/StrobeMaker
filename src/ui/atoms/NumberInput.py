import flet as ft

from utils.debounce import debounce

NUMBER_INPUT_WIDTH = 135
ON_CHANGE_DEBOUNCE_TIME = 0.2

class NumberInput(ft.TextField):
    def __init__(
        self, page, options,
        property,
        *,
        editable = True,
        min = 0,
        max = 200,
        increment = 1,
        user_on_change = None
    ):

        self.page = page
        self.options = options
        self.property = property

        self.min = min
        self.max = max
        self.increment = increment

        self.user_on_change = user_on_change

        super().__init__(
            prefix = ft.IconButton(
                ft.icons.KEYBOARD_ARROW_DOWN,
                on_click = lambda _ : self.increment_value(-self.increment)
            ),

            value = getattr(self.options, self.property),
            read_only = not editable,

            suffix = ft.IconButton(
                ft.icons.KEYBOARD_ARROW_UP,
                on_click = lambda _ : self.increment_value(self.increment)
            ),

            width = NUMBER_INPUT_WIDTH,

            on_change = lambda _ : self.on_change_sum()
        )

    def builtin_on_change(self):
        try:
            int_value = (int(self.value) // self.increment) * self.increment
        except Exception:
            int_value = self.min

        print("Clamping : ", max(self.min, min(self.max, int_value)))
        self.value = max(self.min, min(self.max, int_value))

    # Debounce the ENTIRE on_change,
    # Otherwise the part that is debounced is not awaited, leading to race conditions
    @debounce(ON_CHANGE_DEBOUNCE_TIME)
    def on_change_sum(self):
        self.builtin_on_change()

        setattr(self.options, self.property, self.value)
        if self.user_on_change is not None:
            self.user_on_change(None)

    def increment_value(self, increment):
        self.value += increment
        self.on_change_sum()
        self.page.update()
