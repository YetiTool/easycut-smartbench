from asmcnc.comms.localization import Localization
from asmcnc.comms.logging_system.logging_system import Logger
from asmcnc.comms.router_machine import RouterMachine, Axis
from asmcnc.geometry.job_envelope import BoundingBox

"""
The logic for this module was taken from screen_check_job.py and has been cleaned up slightly,
but going forward it would be nice to refactor and bulk out this module so it can be used in other places.
I didn't end up using it for DWT, but it could be useful going forward.
"""


class JobChecker(object):
    """Job checking module"""

    router_machine = None  # type: RouterMachine
    localization = None  # type: Localization

    def __init__(self, router_machine, localization):
        self.router_machine = router_machine
        self.localization = localization  # TODO: Make localization a singleton

    def get_axis_max_travel(self, axis):
        # type: (Axis) -> float
        """
        Get the specified axis' max travel (with limit switch distance subtracted)
        :param axis: router_machine.Axis (Axis.X, Axis.Y, Axis.Z)
        :return: The max travel for the axis
        """
        if axis == Axis.X:
            return (
                self.router_machine.grbl_x_max_travel
                - self.router_machine.limit_switch_safety_distance
            )
        elif axis == Axis.Y:
            return (
                self.router_machine.grbl_y_max_travel
                - self.router_machine.limit_switch_safety_distance
            )
        elif axis == Axis.Z:
            return (
                self.router_machine.grbl_z_max_travel
                - self.router_machine.limit_switch_safety_distance
            )

    def get_job_bounds(self, bounding_box, axis):
        # type: (BoundingBox, Axis) -> tuple[float, float]
        """
        Get the boundary of the job in home and far end for an axis
        :param bounding_box: the BoundingBox for the job
        :param axis: the axis
        :return: {axis}_home_max, {axis}_far_end_max
        """
        if axis == Axis.X:
            return (-(self.router_machine.x_wco() - bounding_box.range_x[0]),
                    self.router_machine.x_wco() + bounding_box.range_x[1])
        elif axis == Axis.Y:
            return (-(self.router_machine.y_wco() - bounding_box.range_y[0]),
                    self.router_machine.y_wco() + bounding_box.range_y[1])
        elif axis == Axis.Z:
            return (-(self.router_machine.z_wco() - bounding_box.range_z[0]),
                    self.router_machine.z_wco() + bounding_box.range_z[1])

    def is_job_out_of_bounds(self, job_file_path):
        # type: (str) -> list[str]
        """
        Checks whether the job file fits within available boundary.
        :param job_file_path: The absolute path to the job file.
        :return: A list of strings telling the user how to make the job within bounds (or [])
        """
        steps = []

        job_bounding_box = BoundingBox()
        job_bounding_box.set_job_envelope(job_file_path)

        limit_switch_distance = self.router_machine.limit_switch_safety_distance

        job_x_home_max, job_x_far_max = self.get_job_bounds(job_bounding_box, Axis.X)
        job_y_home_max, job_y_far_max = self.get_job_bounds(job_bounding_box, Axis.Y)
        job_z_home_max, job_z_far_max = self.get_job_bounds(job_bounding_box, Axis.Z)

        Logger.debug("Job X %s, %s" % (str(job_x_home_max), str(job_x_far_max)))
        Logger.debug("Job Y %s, %s" % (str(job_y_home_max), str(job_y_far_max)))
        Logger.debug("Job Z %s, %s" % (str(job_z_home_max), str(job_z_far_max)))

        machine_x_max_travel = self.get_axis_max_travel(Axis.X)
        machine_y_max_travel = self.get_axis_max_travel(Axis.Y)
        machine_z_max_travel = self.get_axis_max_travel(Axis.Z)

        Logger.debug("Max X %s", str(machine_x_max_travel))
        Logger.debug("Max Y %s", str(machine_y_max_travel))
        Logger.debug("Max Z %s", str(machine_z_max_travel))

        if job_x_home_max >= machine_x_max_travel:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "X")
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "X")
                + "\n"
            )

        if job_y_home_max >= machine_y_max_travel:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the home end."
                ).replace("N", "Y")
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum further away from home."
                ).replace("N", "Y")
                + "\n"
            )

        if job_z_home_max >= machine_z_max_travel:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the Z axis at the lower end."
                )
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's Z datum higher up."
                )
                + "\n"
            )

        if job_x_far_max >= -limit_switch_distance:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "X")
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "X")
                + "\n"
            )

        if job_y_far_max >= -limit_switch_distance:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the N axis at the far end."
                ).replace("N", "Y")
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's N datum closer to home."
                ).replace("N", "Y")
                + "\n"
            )

        if job_z_far_max >= -limit_switch_distance:
            steps.append(
                self.localization.get_str(
                    "The job extent over-reaches the Z axis at the upper end."
                )
                + "\n"
                + self.localization.get_bold(
                    "Try positioning the machine's Z datum lower down."
                )
                + "\n"
            )

        return steps
