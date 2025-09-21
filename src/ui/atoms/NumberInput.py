import flet as ft

import threading

from utils.debounce import debounce

from ui.CustomEvent import CustomEvent

NUMBER_INPUT_WIDTH = 145

ON_CHANGE_DEBOUNCE_TIME = 1.5
LOOPED_DEBOUNCE_TIME = 3

class NumberInput(ft.TextField):
    def __init__(
        self, page, options,
        property,
        *,

        editable = True,

        min = 0,
        max = 200,
        increment = 1,

        width = NUMBER_INPUT_WIDTH,

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
            prefix = ft.GestureDetector(
                content = ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_DOWN,
                    # This only fires after a mousedown + mouseup,
                    # And thus does not conflict with the GestureDetector handlers below.
                    on_click = lambda _ : self.increment_value(-self.increment)
                ),

                # Ensure that the initial mouse down triggers an increment.
                on_tap_down = lambda _ : self.increment_value(-self.increment),
                # Then, keep triggering increments as long as the mouse is down.
                on_long_press_start = lambda _ : self.loop_increment(-self.increment),
                # And stop when released.
                on_long_press_end = lambda _ : self.stop_looped_increment()
            ),

            value = getattr(self.options, self.property),

            read_only = not editable,

            suffix = ft.GestureDetector(
                content = ft.IconButton(
                    ft.icons.KEYBOARD_ARROW_UP,
                    on_click = lambda _ : self.increment_value(self.increment)
                ),

                # Same as above.
                on_tap_down = lambda _ : self.increment_value(self.increment),
                on_long_press_start = lambda _ : self.loop_increment(self.increment),
                on_long_press_end = lambda _ : self.stop_looped_increment()
            ),

            width = width,

            # The value of the control is only taken into account if either :

            # A. It has been left inactive for a relatively long time (see ON_CHANGE_DEBOUNCE_TIME)
            on_change = lambda _ : self._on_change(),
            # or B. it has been blurred, and thus is no longer being edited.
            on_blur = lambda e : self.on_change_sum(clear_focused_control = True),

            # Signal to Page that any potential keyboard events are happening *here*
            on_focus = lambda _ : self.set_self_as_focus()
        )

    def set_self_as_focus(self):
        self.page.control_in_focus = self

    def builtin_on_change(self, *, skip_clamp_correct = False):
        if not skip_clamp_correct:
            self.clamp_and_correct_value()

        setattr(self.options, self.property, self.value)

    def on_change_sum(self, *, skip_clamp_correct = False, clear_focused_control = False):
        self.builtin_on_change(skip_clamp_correct = skip_clamp_correct)

        if self.user_on_change is not None:
            self.user_on_change(
                CustomEvent(
                    value = self.value,
                    control = self
                )
            )

        if clear_focused_control:
            self.page.control_in_focus = None

    # This needs to be a separate function from on_change_sum(),
    # Purely because it's debounced.
    # Otherwise, either the value keeps changing during edits, or no debounce can happen.
    @debounce(ON_CHANGE_DEBOUNCE_TIME)
    def _on_change(self):
        self.on_change_sum()

    def increment_value(self, increment):
        self.value += increment

        # This is called before on_change to ensure that a click or long press
        # Will not briefly cause the control to display an incorrect value.
        self.clamp_and_correct_value()

        # ...and as such, we skip applying the operation a second time.
        # Note : this is called instead of _on_change,
        # because there is no debounce when using the buttons.
        self.on_change_sum(skip_clamp_correct = True)

        self.page.update()

    def loop_increment(self, increment):

        @debounce(LOOPED_DEBOUNCE_TIME)
        def looped_increment(increment):
            while self.continue_loop:
                self.increment_value(increment)

        self.continue_loop = True

        t = threading.Thread(target = looped_increment, args = (increment,))

        t.start()
        self.increment_thread = t

    def stop_looped_increment(self):
        self.continue_loop = False
        self.increment_thread.join()

    # This cannot be replaced by a @ft.TextField.value.setter,
    # Because we have no access to an underlying field for that property,
    # So we would resort to self.value = ... — causing infinite recursion.

    def clamp_and_correct_value(self):
        val = None

        try:
            val = (int(self.value) // self.increment) * self.increment
        except Exception:
            # This can only be infringed when manually editing the field,
            # And will not trigger with increment and decrement buttons.
            val = self.min
        finally:
            self.value = max(
                self.min,
                min(self.max, val)
            )

    # There is no way to implement looped_increment() with arrow keys,
    # Because flet currently doesn't allow detection of key release
    # (All keyboard events are keydowns)
    # So there's no way to track if keys are being held.

    # By looking around, we can see that such features are in the dev docs,
    # (https://docs.flet.dev/types/keyrepeatevent/)
    # Though absent from the user docs ; 
    # So they will probably become available in the future.

    def on_keyboard_event(self, e):
        if e.key in ["Arrow Up", "Arrow Down"]:
            self.increment_value(self.increment if e.key == "Arrow Up" else -self.increment)
