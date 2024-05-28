"""
Class for handling the various coordinate systems we're using in the dwt app
"""

from asmcnc.comms.logging_system.logging_system import Logger


class CoordinateSystem(object):
    """Class to store the coordinate system data."""

    def __init__(self, m):
        self.m = m
        self.machine_position = self.MachinePosition(self.m)
        self.working_coordinates = self.WorkingCoordinates(self.m)
        self.drywall_tec_position = self.DrywallTecPosition(
            self.machine_position, self.m
        )
        self.drywall_tec_laser_position = self.DrywallTecLaserPosition(
            self.drywall_tec_position
        )
        self.laser_position = self.LaserPosition(
            self.m, self.machine_position, self.drywall_tec_laser_position
        )
        self.debug = False
        if self.debug:
            self.m.s.bind(m_x=lambda i, value: self.log_pos(value))
            self.m.s.bind(m_y=lambda i, value: self.log_pos(value))

    def log_pos(self, value):
        Logger.debug(
            "M: {}, {} W: {}, {} DWT: {}, {} DWTL: {}, {} laser offset: {}, {} laser coordinates: {}, {}".format(
                self.machine_position.get_x(),
                self.machine_position.get_y(),
                self.working_coordinates.get_x(),
                self.working_coordinates.get_y(),
                self.drywall_tec_position.get_x(),
                self.drywall_tec_position.get_y(),
                self.drywall_tec_laser_position.get_x(),
                self.drywall_tec_laser_position.get_y(),
                self.m.laser_offset_x_value,
                self.m.laser_offset_y_value,
                self.laser_position.get_x(),
                self.laser_position.get_y(),
            )
        )

    class MachinePosition(object):
        """Class to store the machine position."""

        def __init__(self, m):
            self.m = m
            self.x = None
            self.y = None
            self.z = None

        def get_x(self):
            return self.m.mpos_x()

        def get_y(self):
            return self.m.mpos_y()

        def get_z(self):
            return self.m.mpos_z()

    class WorkingCoordinates(object):
        """Class to store the working coordinates."""

        def __init__(self, m):
            self.m = m
            self.x = None
            self.y = None
            self.z = None

        def get_x(self):
            return self.m.x_wco()

        def get_y(self):
            return self.m.y_wco()

        def get_z(self):
            return self.m.z_wco()

    class DrywallTecPosition(object):
        """Class to store the drywall tec coordinates."""

        def __init__(self, machine_position, m):
            self.m = m
            self.machine_position = machine_position
            self.m.s.bind(setting_130=lambda i, value: self.update_x_delta(value))
            self.m.s.bind(setting_131=lambda i, value: self.update_y_delta(value))
            self.x_delta = 0
            self.y_delta = 0
            self.z_delta = 0

        def update_x_delta(self, value):
            self.x_delta = round(value - self.m.limit_switch_safety_distance, 2)

        def update_y_delta(self, value):
            self.y_delta = round(value - self.m.limit_switch_safety_distance, 2)

        def get_x(self):
            return self.machine_position.get_x() + self.x_delta

        def get_y(self):
            return self.machine_position.get_y() + self.y_delta

        def get_z(self):
            return self.machine_position.get_z() + self.z_delta

        def get_mx_from_dwx(self, dw_x):
            """
            Method to get the machine x-coordinate from the drywall tec x-coordinate.

            Parameters:
            dw_x (float): The drywall tec x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return dw_x - self.x_delta

        def get_my_from_dwy(self, dw_y):
            """
            Method to get the machine y-coordinate from the drywall tec y-coordinate.

            Parameters:
            dw_y (float): The drywall tec y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return dw_y - self.y_delta

        def get_mz_from_dwz(self, dw_z):
            """
            Method to get the machine z-coordinate from the drywall tec z-coordinate.

            Parameters:
            dw_z (float): The drywall tec z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return dw_z - self.z_delta

        def move_to_dw(self, dw_x=None, dw_y=None, dw_z=None):
            """
            Method to move the machine to the drywall tec coordinates.

            Parameters:
            dw_x (float): The drywall tec x-coordinate.
            dw_y (float): The drywall tec y-coordinate.
            dw_z (float): The drywall tec z-coordinate.
            """
            if dw_x is None and dw_y is None and dw_z is None:
                return
            move_command = "G0 G53"
            if dw_x is not None:
                move_command += " X{}".format(self.get_mx_from_dwx(dw_x))
            if dw_y is not None:
                move_command += " Y{}".format(self.get_my_from_dwy(dw_y))
            if dw_z is not None:
                move_command += " Z{}".format(self.get_mz_from_dwz(dw_z))
            self.m.s.write_command(move_command)

    class DrywallTecLaserPosition(object):
        """Class to store the drywall tec coordinates (using laser as reference)."""

        def __init__(self, dwt_cooridnates):
            self.dwt_coordinates = dwt_cooridnates
            self.laser_delta_x = self.dwt_coordinates.m.laser_offset_x_value
            self.laser_delta_y = self.dwt_coordinates.m.laser_offset_y_value

        def get_x(self):
            return (
                self.dwt_coordinates.get_x()
                + self.dwt_coordinates.m.laser_offset_x_value
            )

        def get_y(self):
            return (
                self.dwt_coordinates.get_y()
                + self.dwt_coordinates.m.laser_offset_y_value
            )

        def get_z(self):
            return self.dwt_coordinates.get_z()

        def get_mx_from_dwlx(self, dwlx):
            """
            Method to get the machine x-coordinate from the drywall tec laser x-coordinate.

            Parameters:
            dwlx (float): The drywall tec laser x-coordinate.

            Returns:
            float: The corresponding machine x-coordinate.
            """
            return self.dwt_coordinates.get_mx_from_dwx(dwlx - self.laser_delta_x)

        def get_my_from_dwly(self, dwly):
            """
            Method to get the machine y-coordinate from the drywall tec laser y-coordinate.

            Parameters:
            dwly (float): The drywall tec laser y-coordinate.

            Returns:
            float: The corresponding machine y-coordinate.
            """
            return self.dwt_coordinates.get_my_from_dwy(dwly - self.laser_delta_y)

        def get_mz_from_dwlz(self, dwlz):
            """
            Method to get the machine z-coordinate from the drywall tec laser z-coordinate.

            Parameters:
            dwlz (float): The drywall tec laser z-coordinate.

            Returns:
            float: The corresponding machine z-coordinate.
            """
            return self.dwt_coordinates.get_mz_from_dwz(dwlz)

        def move_to_dwl(self, dwl_x=None, dwl_y=None, dwl_z=None):
            """
            Method to move the machine to the drywall tec laser coordinates.

            Parameters:
            dwl_x (float): The drywall tec laser x-coordinate.
            dwl_y (float): The drywall tec laser y-coordinate.
            dwl_z (float): The drywall tec laser z-coordinate.
            """
            if dwl_x is None and dwl_y is None and dwl_z is None:
                return
            move_command = "G0 G53"
            if dwl_x is not None:
                move_command += " X{}".format(
                    -self.dwt_coordinates.x_delta
                    - self.dwt_coordinates.m.laser_offset_x_value
                )
            if dwl_y is not None:
                move_command += " Y{}".format(
                    -self.dwt_coordinates.y_delta
                    - self.dwt_coordinates.m.laser_offset_y_value
                )
            if dwl_z is not None:
                move_command += " Z{}".format(self.get_mz_from_dwlz(dwl_z))
            Logger.debug("Moving to machine coordinates: {}".format(move_command))
            self.dwt_coordinates.m.s.write_command(move_command)

    class LaserPosition(object):
        """Class to store the laser coordinates."""

        def __init__(self, m, machine_position, dwt_laser_position):
            self.m = m
            self.machine_position = machine_position
            self.dwt_laser_position = dwt_laser_position
            self.laser_offset_x = self.dwt_laser_position.laser_delta_x
            self.laser_offset_y = self.dwt_laser_position.laser_delta_y
            self.x = self.machine_position.get_x() + self.laser_offset_x
            self.y = self.machine_position.get_y() + self.laser_offset_y

        def get_x(self):
            return self.machine_position.get_x() + self.laser_offset_x

        def get_y(self):
            return self.machine_position.get_y() + self.laser_offset_x
