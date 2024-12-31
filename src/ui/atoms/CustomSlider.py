import flet as ft

from ui.atoms.NumberInput import NumberInput

class CustomSlider(ft.Container):
    def __init__(
        self, page, options,
        property,
        *,

        min,
        max,
        increment,
        user_on_change,

        enclosing_width = 800
    ):

        self.page = page
        self.options = options

        self.property = property

        self.min = min
        self.max = max
        self.increment = increment

        self.user_on_change = user_on_change

        self.enclosing_width = enclosing_width
        self.inner_width = 0.9 * self.enclosing_width
        self.slider_width = 0.8 * self.inner_width
        self.input_width = 0.2 * self.inner_width

        self.slider = ft.Slider(
            min = min,
            max = max,
            divisions = (max - min) // increment,
            value = getattr(self.options, self.property),

            label = "{value}",

            on_change = lambda _ : self.update_value_from_slider()
        )

        self.input = NumberInput(
            page,
            options,
            property,

            editable = False,
            min = min,
            max = max,
            increment = increment,

            user_on_change = lambda _ : self.input_user_on_change_wrapper()
        )

        super().__init__(
            ft.Row(
                [
                    ft.Container(self.slider, width = self.slider_width),
                    ft.Container(self.input, width = self.input_width),
                ],
                width = self.inner_width,
                alignment = ft.MainAxisAlignment.CENTER
            ),

            width = self.enclosing_width
        )

    def input_user_on_change_wrapper(self):
        self.slider.value = self.input.value

        if self.user_on_change is not None:
            self.user_on_change(None)

    def update_value_from_slider(self):
        setattr(self.options, self.property, int(self.slider.value))
        self.input.value = getattr(self.options, self.property)

        if self.user_on_change is not None:
            self.user_on_change(None)
