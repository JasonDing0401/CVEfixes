# import subprocess

# clone = ['https://github.com/top-think/framework', 'https://github.com/maxsite/cms', 'https://github.com/rust-lang/regex', 'https://github.com/weld/core', 'https://github.com/jarofghosts/glance', 'https://github.com/automattic/mongoose', 'https://github.com/agentejo/cockpit', 'https://github.com/lcobucci/jwt', 'https://github.com/LibreOffice/core', 'https://github.com/oroinc/platform', 'https://github.com/embedthis/goahead', 'https://github.com/sidhpurwala-huzaifa/FreeRDP', 'https://github.com/golang/net', 'https://github.com/kongchuanhujiao/server', 'https://github.com/cockpit-hq/cockpit', 'https://github.com/kaltura/server', 'https://github.com/latchset/mod_auth_mellon', 'https://github.com/pterodactyl/panel', 'https://github.com/istio/envoy', 'https://github.com/Automattic/mongoose', 'https://github.com/npm/cli', 'https://github.com/vadz/libtiff', 'https://github.com/lift/framework', 'https://github.com/totaljs/cms', 'https://github.com/myvesta/vesta', 'https://github.com/DeuxHuitHuit/symphony-2', 'https://github.com/omniauth/omniauth', 'https://github.com/openssl/openssl', 'https://github.com/gogo/protobuf', 'https://github.com/FirelyTeam/spark', 'https://github.com/openzfs/zfs', 'https://github.com/elastic/elasticsearch', 'https://github.com/s-cart/core', 'https://github.com/ajenti/ajenti', 'https://github.com/opnsense/core', 'https://github.com/turquoiseowl/i18n', 'https://github.com/mnoorenberghe/ZoneMinder', 'https://github.com/shopware/core', 'https://github.com/embedthis/appweb', 'https://github.com/ractf/core', 'https://github.com/shopware/platform', 'https://github.com/keystonejs/keystone', 'https://github.com/qemu/qemu', 'https://github.com/Ulterius/server', 'https://github.com/icsharpcode/SharpZipLib', 'https://github.com/centreon/centreon', 'https://github.com/OpenPrinting/cups', 'https://github.com/go-vela/server', 'https://github.com/laravel/framework', 'https://github.com/MariaDB/server', 'https://github.com/dweomer/containerd', 'https://github.com/mjg59/linux', 'https://github.com/aawc/unrar', 'https://github.com/zhutougg/c3p0', 'https://github.com/dovecot/core', 'https://github.com/substack/node-shell-quote', 'https://github.com/GNOME/librsvg', 'https://github.com/dotCMS/core', 'https://github.com/jenkinsci/jenkins']
# for repo in clone:
#     name = "_".join(repo.split("/")[-2:]).lower()
#     repo += ".git"
#     subprocess.call(["git", "clone", repo, name], cwd="/scr/dlvp_local_data/repos")
import json
import random

with open("cvefixes_vulnerables_converted.json", "r") as f:
    dic_lst = json.load(f)
with open("cvefixes_nonvulnerables_converted.json", "r") as f:
    dic_lst += json.load(f)

SEED = 4
random.Random(SEED).shuffle(dic_lst)
with open("train.jsonl", "w+") as f:
    train_lst = dic_lst[:int(len(dic_lst)*0.8)]
    for d in train_lst:
        f.write(json.dumps(d)+'\n')
with open("valid.jsonl", "w+") as f:
    valid_lst = dic_lst[int(len(dic_lst)*0.8):int(len(dic_lst)*0.9)]
    for d in valid_lst:
        f.write(json.dumps(d)+'\n')
with open("test.jsonl", "w+") as f:
    test_lst = dic_lst[int(len(dic_lst)*0.9):]
    for d in test_lst:
        f.write(json.dumps(d)+'\n')