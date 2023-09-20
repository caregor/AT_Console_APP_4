import pytest
import yaml

from bin.checkout import checkout
from bin.deploy import deploy
from bin.hash_calc import calc_crc32
from bin.sshcheckers import ssh_checkout, download_files

with open('config/config.yaml', 'rb') as f:
    data = yaml.safe_load(f)


class TestPositive:
    def test_step1(self, make_folder, clear_folders, make_files):
        # test1
        res1 = ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            "cd {}; 7z a -t{} {}/arx2".format(data['folder_in'], data['arch_type'],
                                                              data['folder_out']),
                            'Everything is Ok')

        res2 = ssh_checkout(data['ip_addr'], data['user'], data['passwd'], "ls {}".format(data['folder_out']),
                            'arx2.{}'.format(data['arch_type']))

        assert res1 and res2, "test1 FAIL"

    def test_step2(self, clear_folders, make_files):
        # test2
        res = []
        res.append(
            ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                         'cd {}; 7z a -t{} {}/arx2'.format(data['folder_in'], data['arch_type'], data['folder_out']),
                         'Everything is Ok'))
        res.append(
            ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                         'cd {}; 7z e arx2.{} -o{} -y'.format(data['folder_out'], data['arch_type'],
                                                              data['folder_ext']),
                         'Everything is Ok'))
        for item in make_files:
            res.append(
                ssh_checkout(data['ip_addr'], data['user'], data['passwd'], 'ls {}'.format(data['folder_ext']), item))
        assert all(res), "test2 FAIL"

    def test_step3(self):
        # test3
        assert ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            'cd {}; 7z t arx2.{}'.format(data['folder_out'], data['arch_type']),
                            'Everything is Ok'), 'test3 FAIL'

    def test_step4(self):
        # step4
        assert ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            'cd {}; 7z u arx2.{}'.format(data['folder_in'], data['arch_type']), ''), 'test4 FAIL'

    def test_step5(self, clear_folders, make_files):
        # step5
        res = []
        res.append(
            ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                         'cd {}; 7z a -t{} {}/arx2'.format(data['folder_in'], data['arch_type'], data['folder_out']),
                         'Everything is Ok'))
        for item in make_files:
            res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                                    'cd {}; 7z l arx2.{}'.format(data['folder_out'], data['arch_type']), item))
        assert all(res), 'test5 FAIL'

    def test_step6(self, clear_folders, make_files, make_subfolder):
        # test6
        res = []
        res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                                'cd {}; 7z a -t{} {}/arx'.format(data['folder_in'], data['arch_type'],
                                                                 data['folder_out']),
                                'Everything is Ok'))
        res.append(
            ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                         'cd {}; 7z x arx.{} -o{} -y'.format(data['folder_out'], data['arch_type'],
                                                             data['folder_ext2']),
                         'Everything is Ok'))

        for item in make_files:
            res.append(
                ssh_checkout(data['ip_addr'], data['user'], data['passwd'], 'ls {}'.format(data['folder_ext2']), item))

        res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'], 'ls {}'.format(data['folder_ext2']),
                                make_subfolder[0]))
        res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                                'ls {}/{}'.format(data['folder_ext2'], make_subfolder[0]), make_subfolder[1]))
        assert all(res), 'test6 FAIL'

    def test_step7(self):
        # test7
        assert ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            'cd {}; 7z d arx.{}'.format(data['folder_out'], data['arch_type']),
                            'Everything is Ok'), 'test7 FAIL'

    def test_step8(self, clear_folders, make_files, clear_local_folders):
        # test8
        res = []
        checkout('mkdir {}'.format(data['folder_in']), "")
        for item in make_files:
            res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'], 'cd {}; 7z h {}'.format(data['folder_in'], item), 'Everything is Ok'))
            download_files(data['ip_addr'], data['user'], data['passwd'], "{}/{}".format(data['folder_in'],item), f"{data['folder_in']}/{item}")
            hash = calc_crc32('{}/{}'.format(data['folder_in'], item))
            print(hash)
            res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'], 'cd {}; 7z h {}'.format(data['folder_in'], item), hash))
        print(res)
        assert all(res), 'test8 FAIL'

@pytest.fixture(scope="class", autouse=True)
def setup_before_class():
    deploy()


@pytest.fixture(scope="class", autouse=True)
def teardown_after_class():
        ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                     f"echo {data['passwd']} | sudo -S rm -f p7zip-full_16.02+dfsg-8_arm64.deb", "")
