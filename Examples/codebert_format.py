from pydriller import Git
import random
import hashlib
import json
import sys
import os

count = 0
# start helpers
def generate_dict(commit, code, folder, target):
    # the hash algo they used is just default python hash(), but that changes on each restart
    hash_int = int(hashlib.md5(code.encode()).hexdigest(), 16)
    global count
    d = {
        "project": folder,
        "commit_id": commit.hash,
        "target": target,
        "func": code,
        "idx": count,
        "hash": hash_int,
        # "size": len(code.split("\n")),
        # "message": commit.msg # extra property to make this script work better
    }
    count += 1
    return d
def method_to_code(source, method):
    source_split = source.split("\n")
    start = method.start_line
    end = method.end_line

    # if method.start_line >= len(source_split) or method.name not in source_split[method.start_line]:
    #     print("reached", method.start_line)
    #     for i in range(max(method.start_line - 5, 0), min(method.start_line + 5, len(source_split) - 1)):
    #         if method.name in source_split[i]:
    #             start = i
    #             break
    #     if start == -1:
    #         start = method.start_line

    code_segment = "\n".join(source_split[start-1:end])
    return code_segment
# end helpers

with open("cvefixes.json", "r") as f:
    data = json.load(f)
# 8675
print(len(data))

dup_repo = ['https://github.com/top-think/framework', 'https://github.com/maxsite/cms', 'https://github.com/rust-lang/regex', 'https://github.com/weld/core', 'https://github.com/jarofghosts/glance', 'https://github.com/automattic/mongoose', 'https://github.com/agentejo/cockpit', 'https://github.com/lcobucci/jwt', 'https://github.com/LibreOffice/core', 'https://github.com/oroinc/platform', 'https://github.com/embedthis/goahead', 'https://github.com/sidhpurwala-huzaifa/FreeRDP', 'https://github.com/golang/net', 'https://github.com/kongchuanhujiao/server', 'https://github.com/cockpit-hq/cockpit', 'https://github.com/kaltura/server', 'https://github.com/latchset/mod_auth_mellon', 'https://github.com/pterodactyl/panel', 'https://github.com/istio/envoy', 'https://github.com/Automattic/mongoose', 'https://github.com/npm/cli', 'https://github.com/vadz/libtiff', 'https://github.com/lift/framework', 'https://github.com/totaljs/cms', 'https://github.com/myvesta/vesta', 'https://github.com/DeuxHuitHuit/symphony-2', 'https://github.com/omniauth/omniauth', 'https://github.com/openssl/openssl', 'https://github.com/gogo/protobuf', 'https://github.com/FirelyTeam/spark', 'https://github.com/openzfs/zfs', 'https://github.com/elastic/elasticsearch', 'https://github.com/s-cart/core', 'https://github.com/ajenti/ajenti', 'https://github.com/opnsense/core', 'https://github.com/turquoiseowl/i18n', 'https://github.com/mnoorenberghe/ZoneMinder', 'https://github.com/shopware/core', 'https://github.com/embedthis/appweb', 'https://github.com/ractf/core', 'https://github.com/shopware/platform', 'https://github.com/keystonejs/keystone', 'https://github.com/qemu/qemu', 'https://github.com/Ulterius/server', 'https://github.com/icsharpcode/SharpZipLib', 'https://github.com/centreon/centreon', 'https://github.com/OpenPrinting/cups', 'https://github.com/go-vela/server', 'https://github.com/laravel/framework', 'https://github.com/MariaDB/server', 'https://github.com/dweomer/containerd', 'https://github.com/mjg59/linux', 'https://github.com/aawc/unrar', 'https://github.com/zhutougg/c3p0', 'https://github.com/dovecot/core', 'https://github.com/substack/node-shell-quote', 'https://github.com/GNOME/librsvg', 'https://github.com/dotCMS/core', 'https://github.com/jenkinsci/jenkins']
nonvuln_commits = []
vuln_commits = []
nonvuln_hashes = []
vuln_hashes = []
not_find = set()
j = 0
for entry in data:
    try:
        if entry["repo_url"] in dup_repo:
            repo_name = "_".join(entry["repo_url"].split("/")[-2:]).lower()
        else:
            repo_name = entry["repo_url"].split("/")[-1]
        git = Git("/scr/dlvp_local_data/repos/" + repo_name)
        commit = git.get_commit(entry["commit_id"])
        if len(commit.modified_files) == 0:
            continue
        modified_code_files = [mf for mf in commit.modified_files if mf.filename.endswith((".c", ".cpp", ".h", ".cc")) and len(mf.changed_methods) > 0]
        if len(modified_code_files) == 0:
            continue

        # deleted_code = set()
        # added_code = set()
        vuln_code = set()
        nonvuln_code = set()

        for mf in modified_code_files:
            source_before = mf.source_code_before
            source_after = mf.source_code
            changed_methods = mf.changed_methods
            for method in mf.methods_before:
                if method in changed_methods:
                    vuln_code.add(method_to_code(source_before, method))
                else:
                    nonvuln_code.add(method_to_code(source_before, method))
            for method in mf.methods:
                nonvuln_code.add(method_to_code(source_after, method))
            # what if method name changed? don't need to consider since there must be addition and deletion of the function name
            
        #     if len(mf.diff_parsed["added"]) + len(mf.diff_parsed["deleted"]) > 300:
        #         # this is probably a merge of many different patches
        #         break

        #     source_before = mf.source_code_before
        #     source_after = mf.source_code

        #     for deletion in mf.diff_parsed["deleted"]:
        #         found_method = None
        #         for i in range(len(mf.methods_before)):
        #             check = mf.methods_before[i]
        #             if check.start_line <= deletion[0] <= check.end_line:
        #                 # found method before that corresponds to this deletion
        #                 found_method = check
        #                 break

        #         if not found_method:
        #             continue
        #         print("deletion method name", found_method.name)
        #         deleted_code.add(method_to_code(source_before, found_method))

        #     for added in mf.diff_parsed["added"]:
        #         found_method = None
        #         for i in range(len(mf.methods)):
        #             check = mf.methods[i]
        #             if check.start_line <= added[0] <= check.end_line:
        #                 # found method before that corresponds to this addition
        #                 found_method = check
        #                 break

        #         if not found_method:
        #             continue

        #         added_code.add(method_to_code(source_after, found_method))

        # added_code = list(added_code)
        # deleted_code = list(deleted_code)
        
        added_code = list(nonvuln_code)
        deleted_code = list(vuln_code)

        if entry["cls"] == "neg":
            # deleted code must not have been vulnerable in the first place, just wrong
            raise NotImplementedError("parsing neg commit is not implemented yet")
            # for c in deleted_code:
            #     entry = generate_dict(commit, c, repo_name)
            #     if entry["hash"] not in nonvuln_hashes:
            #         nonvuln_commits.append(entry)
            #         nonvuln_hashes.append(entry["hash"])
            # for c in added_code:
            #     entry = generate_dict(commit, c, repo_name)
            #     if entry["hash"] not in nonvuln_hashes:
            #         nonvuln_commits.append(entry)
            #         nonvuln_hashes.append(entry["hash"])
        else:
            for c in deleted_code:
                entry = generate_dict(commit, c, repo_name, 1)
                if entry["hash"] not in vuln_hashes:
                    vuln_hashes.append(entry["hash"])
                    del entry["hash"]
                    vuln_commits.append(entry)
            for c in added_code:
                entry = generate_dict(commit, c, repo_name, 0)
                if entry["hash"] not in nonvuln_hashes:
                    nonvuln_hashes.append(entry["hash"])
                    del entry["hash"]
                    nonvuln_commits.append(entry)
        if (j+1) % 100 == 0:
            print(j+1)
        j += 1
    except Exception as e:
        print(e)
        print(entry)
        not_find.add(entry["repo_url"])
        continue
print(j)
print(len(not_find))
print(not_find)
# 292813
print(count)
# 8932
print(len(vuln_commits))
# 159157
print(len(nonvuln_commits))
with open("cvefixes_vulnerables_converted.json", "w+") as f:
    f.write(json.dumps(vuln_commits))
with open("cvefixes_nonvulnerables_converted.json", "w+") as f:
    f.write(json.dumps(nonvuln_commits))