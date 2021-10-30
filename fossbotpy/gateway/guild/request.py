#points to commands that help request info/actions using the gateway

class GuildRequest(object):
	__slots__ = ['gatewayobj']
	def __init__(self, gatewayobj):
		self.gatewayobj = gatewayobj

	def lazy_guild(self, guild_id, channel_ranges, typing, threads, activities, members, thread_member_lists): #https://arandomnewaccount.gitlab.io/discord-unofficial-docs/lazy_guilds.html
		data = {
		    "op": self.gatewayobj.OPCODE.LAZY_REQUEST,
		    "d": {
		        "guild_id": guild_id,
		        "typing": typing,
		        "threads": threads,
		        "activities": activities,
		        "members": members,
		        "channels": channel_ranges,
		        "thread_member_lists": thread_member_lists
		    },
		}
		if channel_ranges == None:
			data["d"].pop("channels")
		if typing == None:
			data["d"].pop("typing")
		if threads == None:
			data["d"].pop("threads")
		if activities == None:
			data["d"].pop("activities")
		if members == None:
			data["d"].pop("members")
		if thread_member_lists == None:
			data["d"].pop("thread_member_lists")
		self.gatewayobj.send(data)

	def search_guild_members(self, guild_ids, query, limit, presences, user_ids, nonce): #note that query can only be "" if you have admin perms (otherwise you'll get inconsistent responses from fosscord)
		if isinstance(guild_ids, str):
			guild_ids = [guild_ids]
		data = {
		    "op": self.gatewayobj.OPCODE.REQUEST_GUILD_MEMBERS,
		    "d": {"guild_id": guild_ids},
		}
		if isinstance(user_ids, list): #there are 2 types of op8 that the client can send
			data["d"]["user_ids"] = user_ids
		else:
			data["d"]["query"] = query
			data["d"]["limit"] = limit
		if presences != None:
			data["d"]["presences"] = presences
		if nonce != None:
			data["d"]["nonce"] = nonce
		self.gatewayobj.send(data)