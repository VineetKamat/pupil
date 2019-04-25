"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2019 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""
import typing as t
from eye_movement.utils import Gaze_Data, EYE_MOVEMENT_EVENT_KEY, logger
from eye_movement.model.segment import Classified_Segment
from eye_movement.model.immutable_capture import Immutable_Capture
from eye_movement.model.storage import Classified_Segment_Storage
from eye_movement.worker.offline_detection_task import Offline_Detection_Task
from tasklib.manager import PluginTaskManager


def nop(*args, **kwargs):
    pass


class Eye_Movement_Offline_Controller:
    def __init__(
        self,
        plugin,
        storage: Classified_Segment_Storage,
        on_started: t.Callable[[], None] = nop,
        on_status: t.Callable[[str], None] = nop,
        on_progress: t.Callable[[float], None] = nop,
        on_exception: t.Callable[[Exception], None] = nop,
        on_completed: t.Callable[[], None] = nop,
        on_canceled_or_killed: t.Callable[[], None] = nop,
        on_ended: t.Callable[[], None] = nop,
    ):
        self.g_pool = plugin.g_pool
        self.storage = storage
        self.task_manager = PluginTaskManager(plugin)
        self.eye_movement_task = None

        self._on_started = on_started
        self._on_status = on_status
        self._on_progress = on_progress
        self._on_exception = on_exception
        self._on_completed = on_completed
        self._on_canceled_or_killed = on_canceled_or_killed
        self._on_ended = on_ended

    def classify(self, *args, **kwargs):
        """
        classify eye movement
        """

        if self.g_pool.app == "exporter":
            return

        logger.info("Gaze postions changed. Recalculating.")

        if self.eye_movement_task and self.eye_movement_task.running:
            self.eye_movement_task.kill(grace_period=1)

        capture = Immutable_Capture(self.g_pool.capture)
        gaze_data: Gaze_Data = [gp.serialized for gp in self.g_pool.gaze_positions]

        self.eye_movement_task = Offline_Detection_Task(args=(capture, gaze_data))
        self.task_manager.add_task(self.eye_movement_task)

        self.eye_movement_task.add_observers(
            on_started=self._on_task_started,
            on_yield=self._on_task_yield,
            on_completed=self._on_task_completed,
            on_ended=self._on_task_ended,
            on_exception=self._on_task_exception,
            on_canceled_or_killed=self._on_task_canceled_or_killed,
        )
        self.eye_movement_task.start()

    def _on_task_started(self):
        self.storage.clear()
        self._on_started()
        self._on_progress(0.0)

    def _on_task_yield(self, yield_value):

        status, serialized = yield_value

        if status:
            self._on_status(status)

        if serialized:
            segment = Classified_Segment.from_msgpack(serialized)
            self.storage.add(segment)

            current_ts = segment.end_frame_timestamp
            total_start_ts = self.g_pool.timestamps[0]
            total_end_ts = self.g_pool.timestamps[-1]

            current_duration = current_ts - total_start_ts
            total_duration = total_end_ts - total_start_ts

            progress = max(0.0, min(current_duration / total_duration, 1.0))
            self._on_progress(progress)

    def _on_task_exception(self, exception: Exception):
        self._on_exception(exception)

    def _on_task_completed(self, _: None):
        self.storage.finalize()
        status = "{} segments detected".format(len(self.storage))
        self._on_status(status)
        self._on_progress(1.0)
        self._on_completed()

    def _on_task_canceled_or_killed(self):
        self._on_canceled_or_killed()

    def _on_task_ended(self):
        self._on_ended()
