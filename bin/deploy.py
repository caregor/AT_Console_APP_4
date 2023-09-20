import yaml

from bin.sshcheckers import upload_files, ssh_checkout

with open('config/config.yaml', 'rb') as f:
    data = yaml.safe_load(f)


def deploy():
    res = []
    upload_files(data['ip_addr'], data['user'], data['passwd'], "p7zip-full_16.02+dfsg-8_arm64.deb",
                 "/home/heavy/p7zip-full_16.02+dfsg-8_arm64.deb")
    print('uploaded')
    res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            "echo '111' | sudo -S dpkg -i /home/heavy/p7zip-full_16.02+dfsg-8_arm64.deb", ""))
    print('installing')
    res.append(ssh_checkout(data['ip_addr'], data['user'], data['passwd'],
                            "echo '111' | sudo -S dpkg -s p7zip-full", "Status: install ok installed"))
    print('checking')
    print(res)
    return all(res)
