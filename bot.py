import disnake
from disnake.ext import commands
import asyncio
import json
import os

intents = disnake.Intents.default()
intents.voice_states = True
bot = commands.InteractionBot(intents=intents)

SETTINGS_FILE = "server_settings.json"
CHANNEL_OWNERS_FILE = "channel_owners.json"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_channel_owners():
    if os.path.exists(CHANNEL_OWNERS_FILE):
        with open(CHANNEL_OWNERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_channel_owners(owners):
    with open(CHANNEL_OWNERS_FILE, 'w') as f:
        json.dump(owners, f, indent=4)

TARGET_VOICE_CHANNEL_IDS = load_settings()
CHANNEL_OWNERS = load_channel_owners()

class VoiceControlView(disnake.ui.View):
    def __init__(self, channel, owner_id, moderators=None):
        super().__init__(timeout=None)
        self.channel = channel
        self.owner_id = owner_id
        self.moderators = moderators or []
        
    def is_authorized(self, user_id):
        return user_id == self.owner_id or user_id in self.moderators
    
    @disnake.ui.button(label="Set User Limit", style=disnake.ButtonStyle.primary, emoji="👥")
    async def set_limit(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        await interaction.response.send_modal(
            title="Set User Limit",
            custom_id=f"limit_modal_{self.channel.id}",
            components=[
                disnake.ui.TextInput(
                    label="User Limit (0 = unlimited)",
                    placeholder="Enter number (0-99)",
                    custom_id="limit_input",
                    style=disnake.TextInputStyle.short,
                    max_length=2
                )
            ]
        )
    
    @disnake.ui.button(label="Set Bitrate", style=disnake.ButtonStyle.primary, emoji="🎵")
    async def set_bitrate(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        await interaction.response.send_modal(
            title="Set Bitrate",
            custom_id=f"bitrate_modal_{self.channel.id}",
            components=[
                disnake.ui.TextInput(
                    label="Bitrate in kbps (8-96)",
                    placeholder="Enter bitrate (e.g., 64)",
                    custom_id="bitrate_input",
                    style=disnake.TextInputStyle.short,
                    max_length=2
                )
            ]
        )
    
    @disnake.ui.button(label="Rename Channel", style=disnake.ButtonStyle.primary, emoji="✏️")
    async def rename_channel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        await interaction.response.send_modal(
            title="Rename Channel",
            custom_id=f"rename_modal_{self.channel.id}",
            components=[
                disnake.ui.TextInput(
                    label="New Channel Name",
                    placeholder="Enter new name",
                    custom_id="name_input",
                    style=disnake.TextInputStyle.short,
                    max_length=100
                )
            ]
        )
    
    @disnake.ui.button(label="Kick User", style=disnake.ButtonStyle.danger, emoji="👢")
    async def kick_user(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        members = [m for m in self.channel.members if m.id != self.owner_id]
        if not members:
            await interaction.response.send_message("❌ No users to kick!", ephemeral=True)
            return
        
        options = [
            disnake.SelectOption(label=member.display_name, value=str(member.id))
            for member in members[:25]
        ]
        
        select = disnake.ui.Select(
            placeholder="Select a user to kick",
            options=options,
            custom_id=f"kick_select_{self.channel.id}"
        )
        
        view = disnake.ui.View(timeout=60)
        view.add_item(select)
        
        await interaction.response.send_message("Select a user to kick:", view=view, ephemeral=True)
    
    @disnake.ui.button(label="Block User", style=disnake.ButtonStyle.danger, emoji="🚫", row=1)
    async def block_user(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        await interaction.response.send_modal(
            title="Block User",
            custom_id=f"block_modal_{self.channel.id}",
            components=[
                disnake.ui.TextInput(
                    label="User ID to Block",
                    placeholder="Enter user ID",
                    custom_id="user_id_input",
                    style=disnake.TextInputStyle.short
                )
            ]
        )
    
    @disnake.ui.button(label="Unblock User", style=disnake.ButtonStyle.success, emoji="✅", row=1)
    async def unblock_user(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        blocked_users = []
        for overwrite in self.channel.overwrites:
            if isinstance(overwrite, disnake.Member):
                perms = self.channel.overwrites[overwrite]
                if perms.connect is False:
                    blocked_users.append(overwrite)
        
        if not blocked_users:
            await interaction.response.send_message("❌ No blocked users!", ephemeral=True)
            return
        
        options = [
            disnake.SelectOption(label=member.display_name, value=str(member.id))
            for member in blocked_users[:25]
        ]
        
        select = disnake.ui.Select(
            placeholder="Select a user to unblock",
            options=options,
            custom_id=f"unblock_select_{self.channel.id}"
        )
        
        view = disnake.ui.View(timeout=60)
        view.add_item(select)
        
        await interaction.response.send_message("Select a user to unblock:", view=view, ephemeral=True)
    
    @disnake.ui.button(label="Toggle Video", style=disnake.ButtonStyle.secondary, emoji="📹", row=1)
    async def toggle_video(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if not self.is_authorized(interaction.user.id):
            await interaction.response.send_message("❌ You don't have permission!", ephemeral=True)
            return
        
        everyone_overwrite = self.channel.overwrites_for(interaction.guild.default_role)
        current_video = everyone_overwrite.stream
        
        await self.channel.set_permissions(
            interaction.guild.default_role,
            stream=False if current_video != False else None
        )
        
        status = "disabled" if current_video != False else "enabled"
        await interaction.response.send_message(f"✅ Video has been {status}!", ephemeral=True)
    
    @disnake.ui.button(label="Give Permissions", style=disnake.ButtonStyle.success, emoji="🔑", row=1)
    async def give_permissions(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("❌ Only the owner can grant permissions!", ephemeral=True)
            return
        
        members = [m for m in self.channel.members if m.id != self.owner_id and m.id not in self.moderators]
        if not members:
            await interaction.response.send_message("❌ No users to give permissions!", ephemeral=True)
            return
        
        options = [
            disnake.SelectOption(label=member.display_name, value=str(member.id))
            for member in members[:25]
        ]
        
        select = disnake.ui.Select(
            placeholder="Select a user to give permissions",
            options=options,
            custom_id=f"grant_select_{self.channel.id}"
        )
        
        view = disnake.ui.View(timeout=60)
        view.add_item(select)
        
        await interaction.response.send_message("Select a user to grant permissions:", view=view, ephemeral=True)
    
    @disnake.ui.button(label="Remove Permissions", style=disnake.ButtonStyle.danger, emoji="🔓", row=1)
    async def remove_permissions(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
        if interaction.user.id != self.owner_id:
            await interaction.response.send_message("❌ Only the owner can remove permissions!", ephemeral=True)
            return
        
        if not self.moderators:
            await interaction.response.send_message("❌ No moderators to remove!", ephemeral=True)
            return
        
        options = []
        for mod_id in self.moderators:
            member = interaction.guild.get_member(mod_id)
            if member:
                options.append(disnake.SelectOption(label=member.display_name, value=str(member.id)))
        
        if not options:
            await interaction.response.send_message("❌ No moderators found!", ephemeral=True)
            return
        
        select = disnake.ui.Select(
            placeholder="Select a moderator to remove",
            options=options[:25],
            custom_id=f"revoke_select_{self.channel.id}"
        )
        
        view = disnake.ui.View(timeout=60)
        view.add_item(select)
        
        await interaction.response.send_message("Select a moderator to remove:", view=view, ephemeral=True)

@bot.event
async def on_ready():
    print(f"Bot is ready! Logged in as {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    guild_id = str(member.guild.id)
    
    if after.channel and guild_id in TARGET_VOICE_CHANNEL_IDS:
        target_channel_id = int(TARGET_VOICE_CHANNEL_IDS[guild_id])
        
        if after.channel.id == target_channel_id:
            guild = member.guild
            
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(connect=True),
                member: disnake.PermissionOverwrite(
                    connect=True,
                    manage_channels=True,
                    move_members=True
                )
            }
            
            new_channel = await guild.create_voice_channel(
                f"{member.display_name}'s Voice", 
                category=after.channel.category,
                overwrites=overwrites
            )
            
            await member.move_to(new_channel)
            
            CHANNEL_OWNERS[str(new_channel.id)] = {
                "owner": member.id,
                "moderators": []
            }
            save_channel_owners(CHANNEL_OWNERS)
            
            view = VoiceControlView(new_channel, member.id)
            
            embed = disnake.Embed(
                title="🎙️ Voice Channel Control Panel",
                description=f"Channel Owner: {member.mention}\n\nUse the buttons below to manage your voice channel.",
                color=disnake.Color.blue()
            )
            embed.add_field(name="Available Controls:", value=(
                "👥 Set User Limit\n"
                "🎵 Set Bitrate\n"
                "✏️ Rename Channel\n"
                "👢 Kick User\n"
                "🚫 Block User\n"
                "✅ Unblock User\n"
                "📹 Toggle Video\n"
                "🔑 Give Permissions\n"
                "🔓 Remove Permissions"
            ), inline=False)
            
            try:
                message = await new_channel.send(embed=embed, view=view)
            except:
                pass
            
            async def delete_channel_when_empty():
                while True:
                    await asyncio.sleep(2)
                    if len(new_channel.members) == 0:
                        if str(new_channel.id) in CHANNEL_OWNERS:
                            del CHANNEL_OWNERS[str(new_channel.id)]
                            save_channel_owners(CHANNEL_OWNERS)
                        await new_channel.delete()
                        break
            
            bot.loop.create_task(delete_channel_when_empty())

@bot.event
async def on_modal_submit(interaction: disnake.ModalInteraction):
    custom_id = interaction.custom_id
    
    if custom_id.startswith("limit_modal_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            try:
                limit = int(interaction.text_values["limit_input"])
                if 0 <= limit <= 99:
                    await channel.edit(user_limit=limit)
                    await interaction.response.send_message(f"✅ User limit set to {limit if limit > 0 else 'unlimited'}!", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Invalid limit! Use 0-99.", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)
    
    elif custom_id.startswith("bitrate_modal_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            try:
                bitrate = int(interaction.text_values["bitrate_input"]) * 1000
                if 8000 <= bitrate <= 96000:
                    await channel.edit(bitrate=bitrate)
                    await interaction.response.send_message(f"✅ Bitrate set to {bitrate//1000}kbps!", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ Invalid bitrate! Use 8-96.", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("❌ Please enter a valid number!", ephemeral=True)
    
    elif custom_id.startswith("rename_modal_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            new_name = interaction.text_values["name_input"]
            await channel.edit(name=new_name)
            await interaction.response.send_message(f"✅ Channel renamed to '{new_name}'!", ephemeral=True)
    
    elif custom_id.startswith("block_modal_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            try:
                user_id = int(interaction.text_values["user_id_input"])
                member = interaction.guild.get_member(user_id)
                
                if member:
                    await channel.set_permissions(member, connect=False)
                    
                    if member in channel.members:
                        await member.move_to(None)
                    
                    await interaction.response.send_message(f"✅ {member.mention} has been blocked from this channel!", ephemeral=True)
                else:
                    await interaction.response.send_message("❌ User not found!", ephemeral=True)
            except ValueError:
                await interaction.response.send_message("❌ Invalid user ID!", ephemeral=True)

@bot.event
async def on_dropdown(interaction: disnake.MessageInteraction):
    custom_id = interaction.component.custom_id
    
    if custom_id.startswith("kick_select_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            user_id = int(interaction.values[0])
            member = interaction.guild.get_member(user_id)
            
            if member and member in channel.members:
                await member.move_to(None)
                await interaction.response.send_message(f"✅ {member.mention} has been kicked!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ User not found in channel!", ephemeral=True)
    
    elif custom_id.startswith("unblock_select_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel:
            user_id = int(interaction.values[0])
            member = interaction.guild.get_member(user_id)
            
            if member:
                await channel.set_permissions(member, connect=None)
                await interaction.response.send_message(f"✅ {member.mention} has been unblocked!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ User not found!", ephemeral=True)
    
    elif custom_id.startswith("grant_select_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel and str(channel_id) in CHANNEL_OWNERS:
            user_id = int(interaction.values[0])
            member = interaction.guild.get_member(user_id)
            
            if member:
                CHANNEL_OWNERS[str(channel_id)]["moderators"].append(user_id)
                save_channel_owners(CHANNEL_OWNERS)
                await interaction.response.send_message(f"✅ {member.mention} now has moderator permissions!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ User not found!", ephemeral=True)
    
    elif custom_id.startswith("revoke_select_"):
        channel_id = int(custom_id.split("_")[-1])
        channel = interaction.guild.get_channel(channel_id)
        
        if channel and str(channel_id) in CHANNEL_OWNERS:
            user_id = int(interaction.values[0])
            member = interaction.guild.get_member(user_id)
            
            if user_id in CHANNEL_OWNERS[str(channel_id)]["moderators"]:
                CHANNEL_OWNERS[str(channel_id)]["moderators"].remove(user_id)
                save_channel_owners(CHANNEL_OWNERS)
                await interaction.response.send_message(f"✅ Permissions removed from {member.mention if member else 'user'}!", ephemeral=True)
            else:
                await interaction.response.send_message("❌ User is not a moderator!", ephemeral=True)

@bot.slash_command(name="setvoice")
@commands.has_permissions(administrator=True)
async def set_voice_channel(
    inter: disnake.ApplicationCommandInteraction,
    channel: disnake.VoiceChannel
):
    """
    Set a voice channel for creating private rooms
    
    Parameters
    ----------
    channel: Voice channel that will create private rooms when joined
    """
    guild_id = str(inter.guild.id)
    
    TARGET_VOICE_CHANNEL_IDS[guild_id] = channel.id
    save_settings(TARGET_VOICE_CHANNEL_IDS)
    
    await inter.response.send_message(
        f"✅ Channel {channel.mention} has been set as the voice creator!",
        ephemeral=True
    )

@bot.slash_command(name="removevoice")
@commands.has_permissions(administrator=True)
async def remove_voice_channel(inter: disnake.ApplicationCommandInteraction):
    """Remove the voice creator channel setting"""
    guild_id = str(inter.guild.id)
    
    if guild_id in TARGET_VOICE_CHANNEL_IDS:
        del TARGET_VOICE_CHANNEL_IDS[guild_id]
        save_settings(TARGET_VOICE_CHANNEL_IDS)
        await inter.response.send_message(
            "✅ Voice creator channel has been removed!",
            ephemeral=True
        )
    else:
        await inter.response.send_message(
            "❌ No voice creator channel is set on this server.",
            ephemeral=True
        )

@set_voice_channel.error
@remove_voice_channel.error
async def command_error(inter: disnake.ApplicationCommandInteraction, error):
    if isinstance(error, commands.MissingPermissions):
        await inter.response.send_message(
            "❌ You don't have administrator permissions to use this command!",
            ephemeral=True
        )

@bot.slash_command()
async def hello(inter):
    """Try it!"""
    await inter.response.send_message("Just join the voice, amigo!", ephemeral=True)

bot.run("YOUR_TOKEN_HERE")
