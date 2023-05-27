import datetime
import discord
from discord.ext import commands
from discord.ui import Item

intents = discord.Intents.all()  # intents du bot (all)
bot = discord.Bot(intents=intents, )


@bot.event
async def on_ready():  # regarde si le bot est en ligne
    print("AMONG US BOT READY")
    #bot.add_view(choix_urgence_start())
    await bot.change_presence(activity=discord.Game("Among us"))


salon = 999082043566727319                                                      # A changé par l'id du salon vocal que vous voulez paramétrer pour le jeu


class choix_urgence_start(discord.ui.View):
    def __init__(self, *items: Item):
        super().__init__(*items, timeout=None)

        # information pour le jeu
        self.channel_depart = bot.get_channel(salon)
        self.membres_dans_le_salon_depart = self.channel_depart.members
        self.membres_ids = []
        for i in self.membres_dans_le_salon_depart:
            self.membres_ids.append(i.id)
            print(self.membres_ids)
        self.role = None
        self.start = False

    async def check(self, interaction):                 #vérifie si l'utilisateur ayant appuyé sur un bouton fait partie du jeu en cours ou non
        user = interaction.user.id
        if not user in self.membres_ids:
            await interaction.response.send_message("`Vous n'êtes pas dans la partie actuelle !`", ephemeral=True,
                                                    delete_after=10.0)
            return False                                #renvoie FALSE s'il ne fait pas partie du jeu en cours
        else:
            return True                                 #renvoie TRUE s'il fait partie du jeu en cours

    @discord.ui.button(label="URGENCE", row=0, style=discord.ButtonStyle.danger, custom_id="button-urgence")
    async def URGENCE(self, buttons, interaction):
        if await choix_urgence_start.check(self, interaction) != True:          #regarde si l'utilisateur ayant intéragie avec le bouton fait partie du jeu en cours avec la fonction CHECK inclue dans la class choix_urgence_start
            return
        if self.start == False:                                                 #regarde si la variable self.start (defaut FALSE) est sur FALSE. Si elle est sur TRUE, c'est que le bouton START a été déclanché
            await interaction.response.send_message("`Urgence déjà déclanché !`", ephemeral=True, delete_after=10.0)
            return
        self.start = False
        ctx_all_salons = interaction.guild.channels  # récupère tous les salons de la guild
        for i in ctx_all_salons:
            u = i.name
            for deplacement in self.membres_ids:
                if u == str(
                        deplacement):                                           # regarde si les noms de tous les salons de la guild correspondent aux ids des participants du jeu
                    personne = interaction.guild.get_member(deplacement)
                    try:
                        await personne.move_to(self.channel_depart)             #déplace le membre dans le salon de départ
                    except discord.HTTPException:                               #Si une erreur est retourné pour un utilisateur n'ayant pas été trouvé, elle est ignoré
                        pass
                    await i.delete()                                            #supprime le salon privé du joueur
            if u == "IMPOSTEUR(S)":                                             #Si un salon ayant le nom IMPOSTEUR(S) est trouvé, il sera aussi supprimé.
                await i.delete()
        await interaction.response.send_message("`Urgence déclanché !`", ephemeral=True, delete_after=10.0)

    @discord.ui.button(label="START", row=0, style=discord.ButtonStyle.success, custom_id="button-start")
    async def START(self, buttons, interaction):
        if await choix_urgence_start.check(self, interaction) != True:
            return
        if self.start == True:                                                  #pareil que pour l'URGENCE mais avec TRUE
            await interaction.response.send_message("`Start déjà déclanché !`", ephemeral=True, delete_after=10.0)
            return
        self.start = True

        # créer les salons vocaux par rapport aux membres
        for membres_noms in self.membres_dans_le_salon_depart:
            await interaction.guild.create_voice_channel(membres_noms.id, reason=f"Jeux among us")

        # creer les permissions sur les salons
        for i in interaction.guild.roles:
            if i.name == "@everyone":
                self.role = i

        #définie la variable "perms" avec la permission view_channel du rôle "everyone" sur FALSE
        perms = interaction.channel.overwrites_for(self.role)
        perms.view_channel = False


        salon_de_jeux = []
        ctx_all_salons = interaction.guild.channels  # récupère tous les salons de la guild

        for i in ctx_all_salons:

            u = i.name  # récupère les noms de tous les aslons de la guild
            for j in self.membres_ids:
                if u == str(j):                                                     # regarde si le nom du salons est égale a une id d'un membre dans la liste "list_membres_par_id" qui a été convertis en STR
                    salon_de_jeux.append(u)  # rajout du nom du salon valide par la condition dans une list
                    for x in salon_de_jeux:

                        if u == x:                                                  # regarde si les noms de tous les salons de la guild correspondent avec les noms des salons créer pour les membres participant aux jeux
                            recherche = i.id  # change le nom des salons valides par leurs ids
                            salon = bot.get_channel(recherche)  # recherche les salons avec les ids
                            await salon.set_permissions(self.role,
                                                        overwrite=perms)            # change la permissions des salons trouver par la recherche

            # déplacer les membres dans leurs salons respectifs
            for deplacement in self.membres_ids:
                if u == str(deplacement):                                           # regarde si les noms de tous les salons de la guild correspondent aux ids des salons des membres créer pour le jeux
                    salon_associe = bot.get_channel(i.id)
                    personne = interaction.guild.get_member(deplacement)
                    try:
                        await personne.move_to(salon_associe)
                    except discord.HTTPException:
                        pass
        await interaction.response.send_message("`Start déclanché !`", ephemeral=True, delete_after=10.0)

    @discord.ui.button(label="IMPOSTEUR", row=1, style=discord.ButtonStyle.blurple, custom_id="button-imposteur")
    async def IMPOSTEUR(self, buttons, interaction):

        global list_salon_name, u
        global list_salon

        ctx_all_salons = interaction.guild.channels  # récupère tous les salons de la guild

        for i in interaction.guild.roles:
            if i.name == "@everyone":
                self.role = i
        perms = interaction.channel.overwrites_for(self.role)
        perms.view_channel = False
        user = interaction.user.id

        if await choix_urgence_start.check(self, interaction) != True:
            return
        if self.start != True:
            await interaction.response.send_message("`Partie non déclanchée !`", ephemeral=True, delete_after=10.0)
            return

        list_salon_name = []
        list_salon = []
        for i in ctx_all_salons:
            u = i.name
            list_salon_name.append(u)
            list_salon.append(i)

            for j in self.membres_ids:

                if u == str(j):
                    pass


        if not "IMPOSTEUR(S)" in list_salon_name and str(interaction.user.id) in list_salon_name:               # regarde si il n'y a pas un salon se nommant IMPOSTEUR(S) et si l'id de l'utilisateur correspond au nom d'un des salons créé pour le jeux.
            salon_creer = await interaction.guild.create_voice_channel("IMPOSTEUR(S)", reason=f"Jeux among us") #crée le salon vocal pour les imposteurs
            salon = bot.get_channel(salon_creer.id)                                                             #récupère l'id du salon tout juste créé
            await salon.set_permissions(self.role, overwrite=perms)
            personne = interaction.guild.get_member(user)
            try:
                await personne.move_to(salon)                                                                   #déplace le membre ayant appuyé sur le bouton dans le salon imposteur.
            except discord.HTTPException:                                                                       # Si cette erreur est retourné (membre introuvable dans le salon) il ne fait rien.
                pass
        else:
            print(interaction.user.id, list_salon_name)

        # si le salon imposteur est déjà créé
        for s in list_salon:
            if s.name == "IMPOSTEUR(S)":
                salon = bot.get_channel(s.id)
                personne = interaction.guild.get_member(user)
                try:
                    await personne.move_to(salon)
                except discord.HTTPException:
                    pass

        await interaction.response.send_message("`Imposteur déclanché !`", ephemeral=True, delete_after=10.0)


@bot.command()
async def new_game(ctx):
    # avoir les membres du salon configuré
    global list_membres_par_id
    channel_depart = bot.get_channel(salon)
    if channel_depart == False:
        await ctx.respond("Il n'y a pas assez de joueurs dans le salon vocal (minimum 3) !", ephemeral=True)
        return
    membres_dans_le_salon_depart = channel_depart.members
    if not ctx.author in membres_dans_le_salon_depart:
        await ctx.respond("`!! Vous devez être connecté dans le salon associé pour faire ça !!`", ephemeral=True)
        return

    embed = discord.Embed(title="AMONG US",
                          description="Choisisez un choix par rapport a votre jeux :",
                          timestamp=datetime.datetime.now(),
                          color=15548997)
    embed.add_field(name="__URGENCE__", value="`A appuyer en cas de meurtre ou d'urgence`",
                    inline=True)
    embed.add_field(name="__START__", value="`A appuyer en cas de relancement de partie ou de démarage de partie`",
                    inline=True)
    embed.add_field(name="__IMPOSTEUR__",
                    value="`A appuyer si vous êtes imposteur. Ce bouton se joue sur le fair-play et l'honneteté des joueurs. (BETA TEST)`",
                    inline=True)
    embed.add_field(name="Fonctionnement",
                    value="`A chaque commande effectuer, le bot enregistre les personnes dans le "
                          "salon spécifié. Il est donc impossible qu'un joueur rejoignent la "
                          "partie sans avoir effectuer la commande. Pareil pour ceux qui veulent "
                          "quitter la partie.`",
                    inline=False)
    embed.set_author(name=ctx.author.display_name)

    await ctx.respond(embed=embed, view=choix_urgence_start(), delete_after=10800.0)


@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.respond("`!! Vous ne pouvez pas faire ça !!`", delete_after=10.0)
    elif isinstance(error, discord.ApplicationCommandInvokeError):
        await on_application_command_error(ctx, error.original)
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.respond(
            f"`!! Cette commande est temporairement muette. Attendez {round(error.retry_after, 2)} secondes !!`",
            delete_after=10.0)
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.respond("`!! Veuillez entrer tout les argument nessesaire !!`", delete_after=10.0)
    elif isinstance(error, commands.MemberNotFound):
        await ctx.respond("`!! Membre impossible a trouver !!`", delete_after=10.0)
    elif isinstance(error, commands.BotMissingPermissions):
        await ctx.respond(
            "<:Emergency:1010524007034011668>`!! Je n'ai pas les permissions nessesaire pour faire ça !!`",
            delete_after=10.0)
    elif isinstance(error, commands.UserNotFound):
        await ctx.respond("`!! Utilisateur impossible a trouver !!`", delete_after=10.0)
    elif isinstance(error, commands.CommandInvokeError):
        await ctx.respond(f"`!! {error} !!`",
                          delete_after=10.0)
    else:
        await ctx.respond(f"`!! {error} !!`",
                          delete_after=10.0)
        # raise error


bot.run("YOUR TOKEN")
