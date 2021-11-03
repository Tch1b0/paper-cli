from api import *
from rich import print
from save import selected_builds, selected_mc_version, build_name
import re


def project_list():
    counter = 0
    for item in projects():
        print('(' + str(counter) + ') ' + item)
        counter += 1


def version_group_list(project_number):
    counter = 0
    for item in version_groups(project_number):
        print('(' + str(counter) + ') ' + item)
        counter += 1


def build_list(project_number, mc_version):
    counter = 0
    returnvalue = version_group_builds(project_number, mc_version)
    print(returnvalue)
    sorted_val = sorted(returnvalue, key=lambda k: k['build'], reverse=True)
    for item in sorted_val:
        try:
            print('(' + str(counter) + ') ' + 'Build: ' + str(item['build']) + ' for MC version ' + str(item['version']))
            link = '[link=https://github.com/PaperMC/Paper/commit/{commit_number}]'.format(
                commit_number=str(item['changes'][0]['commit']))
            unformated_summary = str(item['changes'][0]['summary']).format()
            matches = re.search(r"#(\d*)", unformated_summary)
            if matches:
                issueurl = '[link=https://github.com/PaperMC/Paper/issues/{group}]{urltext}[/link]'.format(
                    group=matches.group(1), urltext=matches.group())
                summery_without_url = re.sub(r"#(\d*)", "", unformated_summary, 1)
                formated_summary = summery_without_url[:matches.start()] + issueurl + summery_without_url[matches.start():]
            else:
                formated_summary = unformated_summary

            print('     [{commitlink}{commitshort}[/link]] {summary}'.format(commitlink=link,
                                                                             commitshort=str(item['changes'][0]['commit'])[
                                                                                         :7], summary=formated_summary))
            build_name.append(counter)
            build_name.append(item['downloads']['application']['name'])
            selected_builds.append(counter)
            selected_builds.append(item['build'])
            selected_mc_version.append(counter)
            selected_mc_version.append(item['version'])
            counter += 1
        except IndexError:
            print('an issue ocured skiping ' + str(item['build']))