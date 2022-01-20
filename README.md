# MSABot
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

MSABot is a private discord bot for the UC Davis MSA Discord server (also private). MSABot serves a couple of functions, mainly to do prayer times but also to serve other smaller functions like telling jokes.

## About MSABot's Code
MSABot is written fully in Python, using [discord.py](https://github.com/Rapptz/discord.py) by [Rapptz](https://github.com/Rapptz/). MSABot is actually derived from [AbidBot](https://github.com/troop129/AbidBot), or at least an earlier version of him. MSABot makes use of cogs to organize the code. The commands are (unlike AbidBot) very organized in which cog they are under.

The majority of the code is from my own brain but some were definitely taken from random StackOverflow posts, and I wish I could remember and link it. Sorry for stealing your code.

## Can I run MSABot on my own server?
No, you probably can't in the form it is in this repo. This is merely an exhibition of some of my favorite snippets of code. You are welcome to take what you like and use it for your own bots, but I did not write MSABot with portability in mind. Sorry.

If you are an MSA and you want me to customize MSA bot for use in your server I will be glad to. Just dm me on Discord, my username is **troop129#6666**.

## Commands
I will break up the commands into the cogs they are under, so you can look at the code for them if you so choose. A `*` denotes an optional parameter.

### [Islamic](https://github.com/troop129/MSABot/blob/master/cogs/cog_islamic.py) Commands
- `!setlocation {loc}` to set your location to where the prayer calculations should be from.
- `!prayertimes *{date} *{prayer}` to get either today's or any other day's complete list of prayers or one specific prayer time.

### [General](https://github.com/troop129/MSABot/blob/master/cogs/cog_general.py) Commands
- `!reverse` sends an uno reverse card.
- `!github` sends a link to this repository to look at the code.

### [Fun](https://github.com/troop129/MSABot/blob/master/cogs/cog_fun.py) Commands
- `!joke` random joke from joke API.
- `!emojify {message}` converts text to emojis. So you can say 🇭 🇪 🇱 🇱 🇴 instead of "hello". Looks better on discord, trust me.
- `!avatar *{mention}` displays either your avatar or the person you mention if you provide that.
- `!clap {message}` 👏 appends 👏 a 👏 clap 👏 emoji 👏 between 👏 everything 👏 you 👏 say. 👏
- `!inspire` get an inspiring quote, courtesy of [zenquotes.io](https://zenquotes.io/api)
- `!f` sends the classic [f gif](https://tenor.com/view/press-f-pay-respect-coffin-burial-gif-12855021).
- `!echo *{#channel} {message}` echoes the message again but in another channel, if you so choose.
- `!sarcasm {message}` tO aDd EmPhAsIs AnD nOt AnNoYaNcE.

### [Tictactoe](https://github.com/troop129/MSABot/blob/master/cogs/cog_tictactoe.py) Commands
This was stolen and modified from someone's cog a long time ago, thanks for the code random dude, sorry I didn't credit.
- `!challenge {mention}` starts a ttt game against a player
- `!ttt {position}` to place your marker on the board. See demo below:

![ttt demo 2](https://i.imgur.com/SMBnuOn.gif)

### [Utility](https://github.com/troop129/MSABot/blob/master/cogs/cog_utility.py) Commands
- `!choose {p1} | {p2} ...` to help you choose between things, unlimited options, just separate with `|`.
- `!countdown {time}` to start a countdown of say `5s` and watch it count down.
- `!vote {question} appends thumbs up and thumbs down to the question.
- `!poll {o1} | {op2} ...` to make a poll of options when voting isn't enough
- `!search {parameter}` to search Bing and get very inaccurate results.
- `!define {word}` searches [Oxford's](https://oxforddictionaries.com/) API for a definition.
- `!coinflip` flips a coin to return "heads" or "tails".
- `!8ball {query}` has a nice graphical interface for returning your 8ball quereies.
- `!numberchoose {#} {#}` returns a random number between the two numbers (inclusive). Forgot why I made this.

## Favorite Commands
### !prayertime *{prayer}

For all my Muslim brothers and sisters, AbidBot can tell you what time the prayers are, either all at once or just one specific prayer. If you don't set a location, it gives the default Roseville one.

![pt demo](https://i.imgur.com/faeDPNs.gif)

(Excuse the MSABot demo, AbidBot command broke.)

This command involved helper commands upon helper commands. It's kind of insane how complex it is. It has to make a request based on text location to a coordinates API, then to a timezone API, then to prayertime API, then process all the data with datetime. Quite fun. This is the main command:

```python
 @commands.group(name='pt',
                    aliases=['prayertimes', 'prayertime', 'whenis', 'wi'],
                    invoke_without_command=True)
    async def pt(self, ctx, day: str = None):
        if day is None:
            day = datetime.datetime.today().strftime("%d-%m-%Y")
            name = 'today'
        else:
            try:
                day = datetime.datetime.strptime(
                    day, "%m/%d/%Y").strftime("%d-%m-%Y")
                name = datetime.datetime.strptime(
                    day, "%d-%m-%Y").strftime("%a, %B %d %Y")
            except:
                await ctx.send('Please format the date correctly: `MM/DD/YYYY`'
                               )
                return
        locations = self.get_location()
        if ctx.author.id in locations:
            lat = locations[ctx.author.id][0]
            long = locations[ctx.author.id][1]
            day = datetime.datetime.now(timezone(
                locations[ctx.author.id][3])).strftime("%d-%m-%Y")
            pt = self.get_ptime(day, lat, long)
            embed = discord.Embed(
                title="BeedoBot Prayer Times",
                description="Prayer times in **{}** from the *aladhan.com* API."
                .format(locations[ctx.author.id][2]))
        else:
            day = datetime.datetime.now(
                timezone('US/Pacific')).strftime("%d-%m-%Y")
            pt = self.get_ptime_roseville(day)
            embed = discord.Embed(
                title="BeedoBot Prayer Times",
                description=
                "Prayer times in Roseville, CA, from the *aladhan.com* API.")
        fajr = self.ctime(pt[0])
        sunrise = self.ctime(pt[1])
        dhuhr = self.ctime(pt[2])
        asr = self.ctime(pt[3])
        maghrib = self.ctime(pt[4])
        sunset = self.ctime(pt[5])
        isha = self.ctime(pt[6])
        embed.add_field(
            name="Prayer times for {}:".format(name),
            value=
            "Fajr: **{}**\n Dhuhr: **{}**\n Asr: **{}**\n Maghrib: **{}**\n Isha: **{}**"
            .format(fajr, dhuhr, asr, maghrib, isha))
        await ctx.send(embed=embed)
```

As you can see, it also makes use of pickle to store locations so you don't have to keep reminding it.

This is the aforementioned **!setlocation**:
```python
@commands.command(name='setlocation')
    async def setlocation(self, ctx, *, location: str = None):
        if location is None:
            await ctx.send("I don't belive it is possible to live nowhere...")
        else:
            try:
                locations = self.get_location()
                new_location = self.get_lat_long(location.lower()).split(',')
                tz = self.get_timezone(new_location[0], new_location[1])
                locations[ctx.author.id] = [
                    new_location[0], new_location[1],
                    location.capitalize(), tz
                ]
                self.update_location(locations)
                await ctx.send('Set new location to **{}**.'.format(
                    location.capitalize()))
            except:
                await ctx.send(
                    'Oops, I was not able to find **{}**. Try checking your spelling.'
                    .format(location))
```
This stores the data in the pickle, both timezone and the text so I can call it back when serving the embed, like "prayer time in Dallas".
