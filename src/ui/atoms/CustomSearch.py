import flet as ft

from utils.debounce import debounce

SEARCH_BAR_WIDTH = 400

class CustomSearch(ft.SearchBar):
    def __init__(
        self, page, options,
        property,
        *,
        items,
        transform = lambda x : x,
        user_on_change = None
    ):
        self.page = page
        self.options = options

        self.property = property

        self.transform = transform
        self.user_on_change = user_on_change

        self.all_controls = [
            ft.ListTile(
                title = ft.Text(transform(item)),
                data = item,
                on_click = lambda e : self.on_change_sum(e)
            )

            for item in items
        ]

        super().__init__(
            value = getattr(self.options, self.property),
            controls = [], # Do not initialize with self.all_controls,
            # Else there is noticeable hang time.
            # Clicking the view will set all_controls later, so we're square.
            # Why *that* does not cause hang time, I do not know.

            view_trailing = [
                ft.IconButton(
                    icon = ft.icons.CLOSE,
                    on_click = lambda _ : self.clear()
                )
            ],

            on_change = lambda e : self.on_search(e),
            on_tap = lambda _ : self.open_view(),

            on_focus = lambda _ : self.on_focus_handler(),

            width = SEARCH_BAR_WIDTH
        )

    def builtin_on_change(self, e):
        # Because the display text is different from the underlying value,
        # We cannot simply use self.value to control the options.

        setattr(self.options, self.property, e.control.data)
        self.close_view(self.transform(e.control.data))

        # Also, for some reason, setting self.value here has no effect.

    def on_change_sum(self, e):
        self.builtin_on_change(e)

        if self.user_on_change is not None:
            self.user_on_change(None)

    # NOT an override, extraneous argument
    def open_view(self, reset_list = True):
        if reset_list:
            self.controls = self.all_controls

        super().open_view()

        self.page.update()

    # Override
    def close_view(self, text):
        self.value = self.transform(getattr(self.options, self.property))
        self.controls = self.all_controls

        super().close_view(text)

        self.page.update()

    def on_focus_handler(self):
        self.value = self.transform(getattr(self.options, self.property))
        self.page.update()

    @debounce(0.2)
    def on_search(self, e):
        self.open_view(reset_list = False)

        self.controls = [
            control for control in self.all_controls \
            if e.data in self.transform(control.data)
        ]

        self.update()

    def clear(self):
        self.value = ''
        self.controls = self.all_controls
        self.page.update()
