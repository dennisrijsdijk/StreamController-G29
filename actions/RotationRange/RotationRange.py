from GtkHelper.GenerativeUI.ScaleRow import ScaleRow
from src.backend.DeckManagement.InputIdentifier import Input
from src.backend.PluginManager.ActionCore import ActionCore
from src.backend.PluginManager.EventAssigner import EventAssigner


class RotationRange(ActionCore):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.has_configuration = True

        self.value_slider = ScaleRow(
            action_core=self,
            var_name="value",
            default_value=0,
            min=40,
            max=900,
            title="Rotation Range",
            step=1,
            digits=0,
            draw_value=True,
            round_digits=True,
            add_text_entry=True,
            text_entry_max_length=3,
            can_reset=False
        )

        self.event_manager.add_event_assigner(
            EventAssigner(
                id="set-rotation-range",
                ui_label="Set Rotation Range",
                default_event=Input.Key.Events.DOWN,
                callback=self._on_key_down
            )
        )

    def get_config_rows(self):
        return [
            self.value_slider.widget
        ]

    def _on_key_down(self, _):
        self.plugin_base.backend.set_rotation_range(self.value_slider.get_value())
