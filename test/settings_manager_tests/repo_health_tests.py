try: 
    import unittest
    from mock import Mock, MagicMock

except:
    print("Can't import mocking packages, are you on a dev machine?")

import sys
sys.path.append('./src')

from settings import settings_manager

########################################################
# IMPORTANT!!
# Run from easycut-smartbench folder, with 
# python -m test.settings_manager_tests.repo_health_tests


class RepoHealthTests(unittest.TestCase):
    """docstring for RepoHealthTests"""

    dangling_text = "\
                    dangling blob c923ce37b90be5d85530df1986f3ad5048231e81\n \
                    dangling blob ec30dad33d8be9bc45a6e24d33c3ff0789ad8350\n \
                    dangling blob 4f7d9a39fee89a6e04cdce99fbfb46e7eeb61573\n \
                    dangling tree ff15f366de6dcc3049afb66551d8ccfc28abde3d\n \
                    dangling blob 7b34b14e123d9a9332ca979727e823966166ff00\n \
                    dangling blob 6e76ddf08612b292a1271c5f829da79c8d5ccd7e\n \
                    dangling blob d2ca2faf7ef19c1652179370039e0fd5ed23e222\n \
                    dangling blob 2fe889c4a45f51caef5704cb4eec4f8acb68021d"
        

    def setUp(self):
        # If the set_up method raises an exception while the test is running, 
        # the framework will consider the test to have suffered an error, 
        # and the runTest (or test_X_Name) method will not be executed.

        self.sm = Mock()
        self.set =  settings_manager.Settings(self.sm)


    def test_do_git_fsck(self):
        fsck_out = self.set.do_git_fsck()

        print("FSCK OUTPUT")
        print(self.set.details_of_fsck)
        print("END OF OUTPUT")
        assert fsck_out, 'returns False'
        


if __name__ == "__main__":
    #import sys;sys.argv = get('', 'Test.)estName']
    unittest.main()