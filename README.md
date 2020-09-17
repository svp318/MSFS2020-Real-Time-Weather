# MSFS2020 Real Time Weather
A work in progress to create a custom Microsoft Flight Simulator 2020 weather preset with the current METAR conditions of a given airport.

#### To download executable program:
Get the latest version in [Releases].

#### To install (for developers):
`pip install -r requirements.txt`

`pip install .`

### Why this program exists
As of the time of writing, Microsoft Flight Simulator simply has not gotten its live weather right for me. Temperatures, pressures, winds, clouds, etc. are sadly always wrong.

I started this as a personal project to be able to have accurate real world weather when taking off or landing at desired airports.

I started seeing many people have felt my same frustration, so I decided to create this little program in hopes others can have a more realistic flying experience.

### How it works
###### Microsoft Flight Simulator has the option to save custom weather presets. This program takes advantage of that and creates presets in the necessary folder to make them available in game. This is how:

The program looks for the Microsoft Flight Simulator weather presets folder (currently the program only looks for it in the location "C:\Users\<username>\AppData\Roaming\Microsoft Flight Simulator\Weather\Presets").

The user then inputs an ICAO airport code (_KORD, EDDF, etc._) or a complete METAR (_KORD 171751Z 03014KT 10SM FEW040 FEW250 20/08 A3016 RMK AO2 SLP212 T02000083 10200 20178 50003_).

If it's an ICAO code, the program downloads the latest METAR for that airport and parses it. If the user input a METAR, it parses that without downloading anything.

The parsed METAR is then converted into a "WPR" file, which is in XML format, and is saved into the weather presets folder stated above. The file name will be the airport code followed by ".WPR", for example "KORD.WPR"

If said WPR file doesn't exist, it is created. If it already exists, it is updated.

### How to use
###### For now, this program only works if your Microsoft Flight Simulator weather presets folder is in the following location: C:\Users\<username>\AppData\Roaming\Microsoft Flight Simulator\Weather\Presets

Close Microsoft Flight Simulator.

Enter an ICAO airport code (_KORD, EDDF, etc._) or a complete METAR (_KORD 171751Z 03014KT 10SM FEW040 FEW250 20/08 A3016 RMK AO2 SLP212 T02000083 10200 20178 50003_).

The program will create or update a preset file in said folder with the format "AIRPORT_CODE.WPR", for example "KORD.WPR".

Start Microsoft Flight Simulator. When creating a flight, go to Weather and select "PRESET". From the presets dropdown, select the airport you just created a preset for.

Select the airport for the METAR you downloaded, pick your airplane and fly!

**The way I recommend is: make 2 preset files, one for your departure airport and one for your arrival airport. You can set their corresponding presets in game when you're near them, and fly with "Live" weather between the two.**

### Limitations and Bugs

- Please remember this is a personal project built so far only by myself. It is far from perfect. And if you have used Hi-Fi Simulation's Active Sky before, do not expect this to be even remotely close to the fantastic software they make.
- The biggest caveat with this program is that once a weather preset is created and MSFS is started, the preset can't be updated. In other words, it can be updated, but MSFS won't detect the changes. Or if a new preset is created while MSFS is running, it won't be detected. In summary, any changes to the weather preset require a restart of MSFS for them to work. I have sadly not found a workaround to this.
- Wind data is only for the surface. Once you start climbing, you'll notice the wind stays the same all the way up. I guess what can be done is switching the weather to "Live" once you're far enough from the airport.
- Precipitation and lightning are not included in the preset yet. They will be in the future.
- Cloud "thickness" (how tall they are) is determined on an algorithm that is too simple at this time, which means that an overcast sky might be so thin that you can still see the sky. Or that very high cirrus clouds might look more like cumulus. 
- The program crashes if a wrong ICAO code or METAR is input. I need to work on error handling so this doesn't happen.

### Acknowledgements

- This definitely wouldn't have been possible without the awesome [python-metar] package.
- The airport information database found in the file "aiports.dat" was obtained from [OpenFlights]

[Releases]: https://github.com/svp318/MSFS2020-Real-Time-Weather/releases
[python-metar]: https://github.com/python-metar/python-metar
[OpenFlights]: https://openflights.org/data.html