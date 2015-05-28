import sys
import unittest
import dbus
import dbus.mainloop

sys.path.insert(0, ".")
from coalib.output.dbus.DbusServer import DbusServer


class DbusServerTest(unittest.TestCase):
    def setUp(self):
        self.session_bus = dbus.SessionBus(
            mainloop=dbus.mainloop.NULL_MAIN_LOOP)
        self.dbus_name = dbus.service.BusName("org.coala.v1.test",
                                              self.session_bus)

    def test_apps(self):
        uut = DbusServer(self.session_bus, "/org/coala/v1/test_apps")

        uut.get_or_create_app("app1")
        self.assertEqual(len(uut.apps), 1)
        self.assertIn("app1", uut.apps)

        uut.get_or_create_app("app1")
        self.assertIn("app1", uut.apps)

        uut.dispose_app("app2")
        self.assertNotIn("app2", uut.apps)
        self.assertIn("app1", uut.apps)

        uut.dispose_app("app1")
        self.assertNotIn("app1", uut.apps)

    def test_on_name_lost(self):
        uut = DbusServer(self.session_bus, "/org/coala/v1/test_on_name_lost")
        uut.create_app("app1")

        uut._on_name_lost("", "", "a1")
        self.assertIn("app1", uut.apps)

        uut._on_name_lost("", "app2", "")
        self.assertIn("app1", uut.apps)

        uut._on_name_lost("", "app1", "")
        self.assertNotIn("app1", uut.apps)

    def test_on_disconnected(self):
        def on_disconnected_callback():
            assert 1 == 2

        test_output = 0
        uut = DbusServer(self.session_bus,
                         "/org/coala/v1/test_callback",
                         on_disconnected_callback)
        uut.create_app("app1")
        self.assertRaises(AssertionError, uut.dispose_app, "app1")


if __name__ == "__main__":
    unittest.main(verbosity=2)