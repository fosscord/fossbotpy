#handles building the superproperties dictionary. also includes getting the build number (since this is part of the super properties)

import ua_parser.user_agent_parser
import re

from ..requestsender import Wrapper
from ..logger import Logger

class SuperProperties:
    '''
    https://luna.gitlab.io/fosscord-unofficial-docs/science.html#super-properties-object
    '''
    __slots__ = ['edited_s', 'build_num', 'log']
    def __init__(self, s, build_num='request', log={'console':True, 'file':False}):
        self.edited_s = Wrapper.edited_req_session(s, {'remove': ['Authorization', 'X-Super-Properties']})
        self.build_num = build_num
        self.log = log

    def request_build_number(self):
        Logger.log('Retrieving Fosscord\'s build number...', None, self.log) 
        try: #getting the build num is kinda experimental since who knows if fosscord will change where the build number is located...
            extra_mods = {'update':{'Sec-Fetch-Dest': 'document', 'Sec-Fetch-Mode': 'navigate','Sec-Fetch-Site': 'none'}}
            fosscord_login_page_exploration = Wrapper.send_request(self.edited_s, 'get', 'https://dev.fosscord.com/login', header_modifications=extra_mods, log=False).text #log set to False cause this takes up console space w/o giving meaningful info
            file_with_build_num = 'https://dev.fosscord.com/assets/'+re.compile(r'assets/+([a-z0-9]+)\.js').findall(fosscord_login_page_exploration)[-2]+'.js' #fastest solution I could find since the last js file is huge in comparison to 2nd from last
            req_file_build = Wrapper.send_request(self.edited_s, 'get', file_with_build_num, log=False).text #log set to False cause this is a big file
            index_of_build_num = req_file_build.find('buildNumber')+14
            fosscord_build_num = int(req_file_build[index_of_build_num:index_of_build_num+5])
            Logger.log('Fosscord is currently on build number '+str(fosscord_build_num), None, self.log)
            return fosscord_build_num
        except Exception as e:
            Logger.log('Could not retrieve fosscord build number.', None, self.log)
            Logger.log(e, None, self.log)
            return None

    def get_super_properties(self, user_agent, locale):
        parseduseragent = ua_parser.user_agent_parser.Parse(user_agent)
        browser_ver_list = [parseduseragent['user_agent']['major'], parseduseragent['user_agent']['minor'], parseduseragent['user_agent']['patch']]
        os_ver_list = [parseduseragent['os']['major'], parseduseragent['os']['minor'], parseduseragent['os']['patch']]
        sp = {
            'os': parseduseragent['os']['family'],
            'browser': parseduseragent['user_agent']['family'],
            'device': '',
            'system_locale': locale,
            'browser_user_agent': parseduseragent['string'],
            'browser_version': '.'.join(filter(None, browser_ver_list)),
            'os_version': '.'.join(filter(None, os_ver_list)),
            'referrer': '',
            'referring_domain': '',
            'referrer_current': '',
            'referring_domain_current': '',
            'release_channel': 'stable',
            'client_build_number': 85108,
            'client_event_source': None
        }
        if locale == None:
        	sp.pop('system_locale')
        if self.build_num == 'request':
            reqbuild_num = self.request_build_number()
            if reqbuild_num != None:
                sp['client_build_number'] = reqbuild_num
        else:
            sp['client_build_number'] = int(self.build_num)
        return sp
