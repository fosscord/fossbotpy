#parses response from gateway

from ..importmanager import Imports
imports = Imports(
	{
		"StartParse": "fossbotpy.gateway.start.parse",
		"GuildParse": "fossbotpy.gateway.guild.parse",
		"UserParse": "fossbotpy.gateway.user.parse",
		"MessageParse": "fossbotpy.gateway.messages.parse",
		"ChannelParse": "fossbotpy.gateway.channels.parse",
	}
)

import copy

#function names are just lowercase types, so for type GUILD_MEMBER_LIST_UPDATE, the function is guild_member_list_update
class Parse(object):
	__slots__ = ['response']
	def __init__(self, response):
		self.response = copy.deepcopy(response)

	def auto(self): #auto parse, does not allow for custom inputs
		resptype = str(self.response.get('t')).lower()
		if hasattr(self, resptype):
			return getattr(self, resptype)()
		return self.response.get('d') #just return the value of d if there's no parse function for it yet

	def ready(self):
		return imports.StartParse().ready(self.response)

	def guild_member_list_update(self):
		return imports.GuildParse().guild_member_list_update(self.response)

	def guild_create(self, my_user_id="0"): #personal user id needed to update personal roles for that guild
		return imports.GuildParse().guild_create(self.response, my_user_id)

	def guild_members_chunk(self):
		return imports.GuildParse().guild_members_chunk(self.response)

	def message_create(self):
		return imports.MessageParse().message_create(self.response)

	def sessions_replace(self, session_id="0"):
		return imports.UserParse().sessions_replace(self.response, session_id)

	def channel_create(self):
		return imports.ChannelParse().channel_create(self.response)

	def channel_delete(self):
		return imports.ChannelParse().channel_delete(self.response)
