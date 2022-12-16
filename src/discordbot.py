from math import floor
from typing import Literal, List
import random as rng

import os
def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


import discord
from discord import app_commands

import requests
from bs4 import BeautifulSoup
def getdata(url):
    r = requests.get(url)
    return r.text


#   https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self) -> None:
        #self.tree.clear_commands(guild=None)
        await self.tree.sync()

        self.add_view(ColorSelectView())
        self.add_view(RoleSelectView())

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

#region -basics

@client.tree.command()
async def ping(interaction: discord.Interaction):
    """Проверка связи"""
    await interaction.response.send_message(f"Понг {interaction.user.mention}! ({round(client.latency * 1000)}мс)")

@client.tree.command()
@app_commands.rename(
    one = 'первое',
    two = 'второе'
)
@app_commands.describe(
    one='Минимальное число',
    two='Максимальное число',
)
async def random(interaction: discord.Interaction, one: int, two: int):
    """Сгенерировать целое число"""
    await interaction.response.send_message(rng.randint(one, two))
            
@client.tree.command()
@app_commands.rename(ammount='количество')
@app_commands.describe(ammount='Количество последних сообщений')
async def clear(interaction: discord.Interaction, ammount: int):
    """Удалить сообщения"""
    if not interaction.permissions.manage_messages:
        await interaction.response.send_message(":x: Нужны права управлять сообщениями")
        return

    print(f"{interaction.user.name} cleared {ammount} messages")
    await interaction.response.defer()
    await interaction.channel.purge(limit=ammount+1)
    await interaction.channel.send(f"{interaction.user.mention} удалил {ammount} сообщений")

#endregion

#region -spam & funnys

@client.tree.command()
@app_commands.rename(seed='вопрос')
@app_commands.describe(seed='Вопрос на который нужно ответить')
async def crystallball(interaction: discord.Interaction, seed: str = None):
    """Предсказать будущее"""
    rng.seed(seed)
    msg = rng.choice(anwsers)
    await interaction.response.send_message(msg)

@client.tree.command()
@app_commands.rename(user='пользователь')
@app_commands.describe(user='Кого протестировать')
async def amongus(interaction: discord.Interaction, user: discord.Member = None):
    """Ты импостер или нет?"""
    user = user or interaction.user

    anwser = [f"{user} оказался предателем.",f"{user} не был предателем."]
    a = rng.randint(0, 1)
    await interaction.response.send_message(
        f". 　　　。　　　　•　 　ﾟ　　。 　　.\n.　　 。　　　　　 ඞ 。 . 　　 • 　　　　•\n　　ﾟ　　 {anwser[a]}　 。　.\n　　'　　　 {rng.randint(0,1)+a} предателей осталось. 　 　　。\n　　　.　　　 　　.　　　　　。　　 。　. 　\n　　ﾟ　　　.　　　. ,　　　　.　 ."
    )

#endregion

#region gdz
gdz_subj = ["русский","алгебра","немецкий","английский","геометрия","химия","обществознание","литература","история(россии)","физика","обж","география"]
gdz_extra_subj = ["алгебра (дидактика)", "физика (дидактика)"]
gdz_sites = {
    "русский"        :"class-9/russkii_yazik/barhudarov-kruchkov-9/",
    "алгебра"        :"class-9/algebra/makarichev-14/",
    "немецкий"       :"class-9/nemeckiy_yazik/bim-4/",
    "английский"     :"class-9/english/kuzovlev-12/",
    "геометрия"      :"class-7/geometria/atanasyan-7-9/",
    "химия"          :"class-9/himiya/rudzitis-feldman/",
    "обществознание" :"class-9/obshhestvoznanie/bogolyubov/",
    "литература"     :"class-9/literatura/korovina/",
    "история(россии)":"class-9/istoriya/arsentjev/",
    "физика"         :"class-9/fizika/peryshkin-gutnik/",
    "обж"            :"class-9/obj/smirnov/",
    "география"      :"class-9/geografiya/alekseev-a-i/",

    "алгебра (дидактика)" : "class-9/algebra/makarichev-15/",
    "физика (дидактика)"  : "class-9/fizika/didakticheskie-materiali-maron/",
}

class gdzTreeButton(discord.ui.Button['gdzTree']):
    def __init__(self, label: str, index: int = -1, site: str = "", st: discord.ButtonStyle = discord.ButtonStyle.secondary):
        super().__init__(style=st, label=label, disabled=(site == "-"))
        self.label = label
        self.index = index
        self.site = site
        self.st = st

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: gdzTree = self.view

        if view.chunks and (" - " in self.label): # if part of a chunk
            view.clear_items()
            view.tree = view.tree[view.chunk_size*self.index : view.chunk_size*(self.index+1)]
            l = len(view.tree)
            if l > 15:
                view.chunk_size = floor(l/14)
                text_tree = [" ".join(x.get_text().split()) for x in view.tree]
                view.chunks = [text_tree[x:x+view.chunk_size] for x in range(0, l, view.chunk_size)]
                for i, x in enumerate(view.chunks):
                    if x[0] == x[-1]: view.add_item(gdzTreeButton(f"{view.stripname(x[0])}", i))
                    else: view.add_item(gdzTreeButton(f"{view.stripname(x[0])} - {view.stripname(x[-1])}", i))
            else:
                view.chunks = []
                for i, x in enumerate(view.tree):
                    view.add_item(gdzTreeButton(view.stripname(" ".join(x.get_text().split())), i))
            
            content = self.label
            await interaction.response.edit_message(content=content, view=view)
            return
        if view.chunks:
            self.index = self.index * view.chunk_size

        if self.label[0] == "🔃":
            view.fnum = (view.fnum + 1) % len(view.images)
            self.label = f"🔃 {view.fnum+1}/{len(view.images)}"

            image = view.images[view.fnum]["src"][2:]
            name = view.images[view.fnum]["alt"]
            embed=discord.Embed(title="gdz.ru",description=name, color=0x4070d6)
            embed.set_image(url = f"https://{image}")
            await interaction.response.edit_message(content="", embed=embed, view=view)

        elif view.found == 1 or self.site: # if at last step
            if self.site:
                url = self.site
                view.images = []
            else:
                view.sect = view.tree[self.index]
                view.found = 2

                url = view.sect['href']
                
            site=f"https://gdz.ru{url}"
            htmldata = getdata(site)
            soup = BeautifulSoup(htmldata, 'html.parser')

            figure = soup.figure
            while figure != None:
                for fimg in figure.find_all("img"):
                    view.images.append(fimg)
                figure = figure.find_next_sibling("figure")
                
            image = view.images[0]["src"][2:]
            others = soup.find("div", {"class":"tasks-pagination__items"})

            sect = others.a

            tree = []
            while sect != None:
                tree.append(sect)
                sect = sect.find_next_sibling("a")

            
            for i,x in enumerate(tree):
                if x["href"] == url: 
                    a = max(i-2, 0)
                    b = min(a + 4, len(tree)) + 1

            view.clear_items()

            for i in range(a, b):
                x = tree[i]
                if x["href"] == url: 
                    view.add_item(gdzTreeButton(label=view.stripname(x.get_text()),site="-"))
                else:
                    view.add_item(gdzTreeButton(label=view.stripname(x.get_text()),site=x["href"]))

            if len(view.images) > 1 : view.add_item(gdzTreeButton(f"🔃 {view.fnum+1}/{len(view.images)}", 0, st=discord.ButtonStyle.primary))
            view.add_item(discord.ui.Button(label='Ссылка', url=site, style=discord.ButtonStyle.primary))

            name = view.images[view.fnum]["alt"]
            embed=discord.Embed(title="gdz.ru", description=name, color=0x4070d6)
            embed.set_image(url = f"https://{image}")
            await interaction.response.edit_message(content="", embed=embed, view=view)
                
        else: # if searching
            view.sect = view.tree[self.index]
            view.start = view.sect.find_parent("section")

            if (view.sect.find_next_sibling("section")):
                view.sect = view.sect.find_next_sibling("section")
                view.tree = []

                while view.sect != None:
                    view.tree.append(view.sect.header)
                    view.sect = view.sect.find_next_sibling("section")
            else:
                view.sect = view.sect.find_next_sibling("div").a
                view.found = 1
                view.tree = []

                while view.sect != None:
                    view.tree.append(view.sect)
                    view.sect = view.sect.find_next_sibling("a")
            view.clear_items()

            l = len(view.tree)
            if l > 15:
                view.chunk_size = floor(l/14)
                text_tree = [" ".join(x.get_text().split()) for x in view.tree]
                view.chunks = [text_tree[x:x+view.chunk_size] for x in range(0, l, view.chunk_size)]
                for i, x in enumerate(view.chunks):
                    if x[0] == x[-1]: view.add_item(gdzTreeButton(f"{view.stripname(x[0])}", i))
                    else: view.add_item(gdzTreeButton(f"{view.stripname(x[0])} - {view.stripname(x[-1])}", i))
            else:
                view.chunks = []
                for i, x in enumerate(view.tree):
                    view.add_item(gdzTreeButton(view.stripname(" ".join(x.get_text().split())), i))

            content = self.label

            
            await interaction.response.edit_message(content=content, view=view)

class gdzTree(discord.ui.View):
    children: List[gdzTreeButton]

    def __init__(self, subj):
        super().__init__()
        self.subj = subj

        self.found = False

        self.images = []
        self.fnum = 0

        self.chunks = []
        self.chunk_size = 0


        subsite = gdz_sites[self.subj]

        site=f"https://gdz.ru/{subsite}"

        htmldata = getdata(site)
        soup = BeautifulSoup(htmldata, 'html.parser')
        print(f'running /gdz on {subsite}:    {type(htmldata)=}    {type(soup)=}')

        start = soup.find("div", {"class": "task-list"})
        print(f'{type(start)=}')
        self.sect = start.section

        self.tree = []

        while self.sect != None:
            self.tree.append(self.sect.header)
            self.sect = self.sect.find_next_sibling("section")

        
        l = len(self.tree)
        if l > 15:
            self.chunk_size = floor(l/14)
            text_tree = [" ".join(x.get_text().split()) for x in self.tree]
            self.chunks = [text_tree[x:x+self.chunk_size] for x in range(0, l, self.chunk_size)]
            for i, x in enumerate(self.chunks):
                if x[0] == x[-1]: self.add_item(gdzTreeButton(f"{self.stripname(x[0])}", i))
                else: self.add_item(gdzTreeButton(f"{self.stripname(x[0])} - {self.stripname(x[-1])}", i))
        else:
            for i, x in enumerate(self.tree):
                self.add_item(gdzTreeButton(self.stripname(" ".join(x.get_text().split())), i))

    def stripname(self, text):
        if len(text) > 15:
            ntext = f'{text[:10]}{text[10:].split(" ")[0]}'
            if ntext != text: ntext += '...'
            if any(map(str.isdigit, ntext)): 
                return ntext

            ntext = f'{text[:20]}{text[20:].split(" ")[0]}'
            if ntext != text: ntext += '...'
            if any(map(str.isdigit, ntext)): 
                return ntext

            ntext = f'{text[:25]}{text[25:].split(" ")[0]}'
            if ntext != text: ntext += '...'
            return ntext[:80]
        return text
 
@client.tree.command()
@app_commands.rename(subj='предмет')
@app_commands.describe(subj='Предмет по которому задание')
async def gdz(interaction: discord.Interaction, subj: eval(f'Literal{str(gdz_subj)}')):
    """Найти задание на gdz.ru"""
    await interaction.response.send_message(content=subj, view=gdzTree(subj))

@client.tree.command()
@app_commands.rename(subj='предмет')
@app_commands.describe(subj='Предмет по которому задание')
async def extragdz(interaction: discord.Interaction, subj: eval(f'Literal{str(gdz_extra_subj)}')):
    """Найти задание на gdz.ru по дополнительным предметам"""
    await interaction.response.send_message(content=subj, view=gdzTree(subj))

#endregion

#region reddit save
class RedditSave(discord.ui.View):
    def __init__(self, url: str):
        super().__init__()
        id = url.split("/")[6]

        self.add_item(discord.ui.Button(label='Скачать', url=f"https://redditsave.com/info?url={url}"))
        self.add_item(discord.ui.Button(label='Другие разширения', url=f"https://redditsave.com/sd.php?id={id}"))

@client.tree.command()
@app_commands.rename(url='ссылка')
@app_commands.describe(url='Ссылка на пост в Reddit')
async def redditsave(interaction: discord.Interaction, url: str = None):
    """Создать ссылку на RedditSave"""
    if len(url.split("/")) == 9 and url[:25] == "https://www.reddit.com/r/":
        embed = discord.Embed(title="redditsave.com", color=0xff4500)
        await interaction.response.send_message(embed=embed, view=RedditSave(url), ephemeral=True)
        return
    print(url, url[:24], url.split("/"), sep="\n")
    await interaction.response.send_message(":x: Неправильная ссылка на Reddit", ephemeral=True)
#endregion

@client.tree.context_menu(name='Сделать цитату')
async def quote(interaction: discord.Interaction, message: discord.Message):
    """Превращает сообщение в цитату"""
    time=message.created_at
    msg=f'<t:{floor(time.timestamp())}>'
    embed = discord.Embed(title=message.author, color=discord.Colour.blurple())
    embed.add_field(name=message.content,value=msg,inline=True)
    await interaction.response.send_message(embed=embed)


#region colorselect
class ColorSelect(discord.ui.Select):
    def __init__(self):
        super().__init__()

        options = [
            discord.SelectOption(label='Убрать', emoji='❌'),
            discord.SelectOption(label='Красный', emoji='🟥'),
            discord.SelectOption(label='Оранжевый', emoji='🟧'),
            discord.SelectOption(label='Жёлтый', emoji='🟨'),
            discord.SelectOption(label='Лаймовый', emoji='<:light_green_square:1053312895871619122>'),
            discord.SelectOption(label='Зелёный', emoji='🟩'),
            discord.SelectOption(label='Бирюзовый', emoji='<:cyan_square:1053312891639570512>'),
            discord.SelectOption(label='Голубой', emoji='🟦'),
            discord.SelectOption(label='Синий', emoji='<:dark_blue_square:1053312893099188234>'),
            discord.SelectOption(label='Фиолетовый', emoji='🟪'),
            discord.SelectOption(label='Розовый', emoji='<:pink_square:1053312897293500488>'),
            discord.SelectOption(label='Чёрный', emoji='⬛'),
            discord.SelectOption(label='Серый', emoji='<:gray_square:1053312894554611742>'),
            discord.SelectOption(label='Белый', emoji='⬜'),
            discord.SelectOption(label='Тестер', emoji='🧩'),
            discord.SelectOption(label='Хелпер', emoji='🛠️'),
        ]
        super().__init__(placeholder='Выбери себе цвет для ника!', min_values=1, max_values=1, options=options, custom_id="colorpicker")

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        roles = {
            'красный':   793090908018311188,
            'оранжевый': 793091325456154644,
            'жёлтый':    793091826017239070,
            'лаймовый':  793093436710322196,
            'зелёный':   753968565908144160,
            'бирюзовый': 793094309317836801,
            'голубой':   753968921496911902,
            'синий':     753969127194099712,
            'фиолетовый':758710603174510595,
            'розовый':   759344214201991198,
            'чёрный':    758395583026167828,
            'серый':    1053311575517306971,
            'белый':     765174370821210133,
            'тестер':   1027869508708347934,
            'хелпер':    960835410576162966,
        }
        allowed_roles = [
             'красный', 'оранжевый', 'жёлтый', 'лаймовый', 'зелёный', 'бирюзовый', 'голубой', 'синий', 'фиолетовый', 'розовый', 'чёрный', 'серый', 'белый'
        ]
        self.values[0] = self.values[0].lower()
        print(f'changed color > {user}   --->   {self.values[0]}')
        for r in user.roles:
            if r.id in roles.values():
                await user.remove_roles(r,reason="Смена цвета")
            if r.id == 958719352511807568: allowed_roles.append(r.name)
            if r.id == 902109985322987520: allowed_roles.append(r.name)

        if self.values[0] == 'убрать':
            await interaction.response.send_message(f'Убран цвет ника', ephemeral=True)
            return

        if not self.values[0] in allowed_roles:
            await interaction.response.send_message(f':x: Нет нужной роли\nУбран цвет ника', ephemeral=True)
            return

        role = guild.get_role(roles[self.values[0]])
        await user.add_roles(role, reason="Смена цвета")
        await interaction.response.send_message(f'Цвет ника теперь {self.values[0]}', ephemeral=True)

class ColorSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(ColorSelect())

"""
@client.tree.command()
async def send_colorpicker(interaction: discord.Interaction):
    if interaction.user.id != 645877523481362432: return
    rolechannel = client.get_channel(822091925502951424)
    embed=discord.Embed(title="Выбери себе цвет для ника!", color=0x4070d6)
    embed.set_image(url = 'https://cdn.discordapp.com/attachments/759379511585407007/1053318728886001765/roles.png') #src/images/roles.png  
    await rolechannel.send(embed=embed, view=ColorSelectView())
"""
#endregion

#region roleselect
class RoleSelect(discord.ui.Select):
    def __init__(self):
        super().__init__()

        options = [
            discord.SelectOption(label='Пинги', emoji='🔔'),
            discord.SelectOption(label='Эвенты', emoji='📢'),
            discord.SelectOption(label='Тестер', emoji='🧩'),
        ]
        super().__init__(placeholder='Выбери себе дополнительные роли!', options=options, custom_id="rolepicker",max_values=3,min_values=0)

    async def callback(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user
        roles = {
            'Пинги':   1029529953538146315,
            'Эвенты':  1029530113584418870,
            'Тестер':  958719352511807568,
        }

        user_roles = [x.id for x in user.roles]
        print(f'changed roles > {user}   --->   {self.values}')
        for r, id in roles.items():
            role = guild.get_role(id)
            a = r in self.values
            b = id in user_roles
            if a and not b:
                await user.add_roles(role, reason = "Смена роли")
            elif b and not a:
                await user.remove_roles(role,reason="Смена роли")

    
        await interaction.response.send_message(f'Роли сменены!', ephemeral=True)

class RoleSelectView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # Adds the dropdown to our view object.
        self.add_item(RoleSelect())

"""
@client.tree.command()
async def send_rolepicker(interaction: discord.Interaction):
    if interaction.user.id != 645877523481362432: return
    rolechannel = client.get_channel(822091925502951424)
    embed=discord.Embed(title="Выбери себе другие роли!", color=0x4070d6)
    embed.add_field(name="Пинги", value="<@&1029529953538146315>\nОбщедоступная роль которую можно пингнуть",inline=False)
    embed.add_field(name="Эвенты", value="<@&1029530113584418870>\nПолучить пинг когда происходит событие (например jackbox, игры)",inline=False)
    embed.add_field(name="Тестер", value="<@&958719352511807568>\nСоглашаешься быть подопытной крысой у <@645877523481362432>",inline=False)
    await rolechannel.send(embed=embed, view=RoleSelectView())
"""
#endregion



@client.event
async def on_ready():
    global MY_GUILD, MY_GUILD2
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')
    
    MY_GUILD = client.get_guild(714888484565024839)  # nml private
    MY_GUILD2 = client.get_guild(753874251089444874) # gamingru


admin=False
def main():
    global gdz_sites, anwsers, gdz_subj, gdz_extra_subj, fpath

    path = find("8ballAnwsers.txt",".")
    print(path)
    
    fpath = ''
    #fpath = '\\home\\nml\\discordbot\\src'
    with open(find('token.txt','.')) as f:
        tkn = f.readline()
    
    with open(path, "r",encoding="utf-8") as txt:
        lines = txt.readlines()
    
        anwsers=[]
        for i in range(len(lines)):
            if not(lines[i].startswith("/*")or lines[i]=="\n"):anwsers.append(lines[i][:-1])

    print("Logging in...")
    client.run(tkn)                                 # Validate our token

if __name__=="__main__":main()
