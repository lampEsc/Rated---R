DROP TABLE IF EXISTS albums;

CREATE TABLE albums 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    name TEXT NOT NULL,
    band TEXT NOT NULL,
    songs LONGTEXT NOT NULL

);

INSERT INTO albums (name, year, band, songs)
VALUES
    ("Bullshit as Usual", 2003, "Pase Rock", "Sunrise, Grey Matter, A Fly Love Song, Pase Burger, Bullshit as Usual, Relax for Girls, Interlude, It's About Time, Join the Optimists, Interlude, Fracturedreamadhectic, Move, Post World, The Old Light"),
    ("Ride The Lightening", 1984, "Metallica", "Fight Fire with Fire, Ride the Lightning, For Whom the Bell Tolls, Fade to Black, Trapped Under Ice, Escape, Creeping Death, The Call of Ktulu"),
    ("Seasons In The Abyss", 1990, "Slayer", "War Ensemble, Blood Red, Spirit in Black, Expendable Youth, Dead Skin Mask, Hallowed Point, Skeletons of Society, Temptation, Born of the Fire, Seasons in the Abyss"),
    ("Electric Ladyland", 1968, "Jimi Hendrix", "And The Gods Made Love, Have You Ever Been (To Electric Ladyland), Cross Town Traffic, Voodoo Chile, Little Miss Strange, Long Hot Summer Night, Come On, Gypsy Eyes, The Burning Of The Midnight Lamp, Rainy Day (Dream Away), 1983... (A Merman I Should Turn To Be), Moon (Turn The Tides...), Still Raining (Still Dreaming), House Burning Down, All Along The Watchtower, Voodoo Chile (Slight Return)"),
    ("Homework", 1997, "Daft Punk", "Daftendirekt, WDPK 83.7 FM, Revolution 909, Da Funk, Phœnix, Fresh, Around the World, Rollin' & Scratchin', Teachers, High Fidelity, Rock'n Roll, Oh Yeah, Burnin', Indo Silver Club, Alive, Funk Ad"),
    ("Veni Vidi Vicious", 2000, "The Hives", "Tick Tick Boom, Try It Again, You Got It All... Wrong, Well All Right!, Hey Little World, A Stroll Through Hive Manor Corridors, Won't Be Long, T.H.E.H.I.V.E.S., Return the Favour, Giddy Up!, Square One Here I Come, You Dress Up for Armageddon, Puppet on a String, Bigger Hole to Fill"),
    ("The Black And White Album", 2007, "The Hives", "The Hives – Declare Guerre Nucleaire, Die All Right!, A Get Together to Tear it Apart, Main Offender, Outsmarted, Hate to Say I Told You So, The Hives – Introduce the Metric System in Time, Find Another Girl, Statecontrol, Inspection Wise 1999, Knock Knock, Supply and Demand"),    
    ("Royal Blood", 2014, "Royal Blood", "Out of the Black, Come On Over, Figure It Out, You Can Be So Cruel, Blood Hands, Little Monster, Loose Change, Careless, Ten Tonne Skeleton, Better Strangers"),    
    ("Rated R", 2010, "Queens of the Stone Age", "Feel Good Hit of the Summer, The Lost Art of Keeping a Secret, Leg of Lamb, Auto Pilot, Better Living Through Chemistry, Monsters in the Parasol, Quick and to the Pointless, In the Fade, Tension Head, Lightning Song, I Think I Lost My Headache"),    
    ("Songs for the Deaf", 2002, "Queens of the Stone Age", "You Think I Ain't Worth a Dollar (But I Feel Like a Millionaire), No One Knows, First It Giveth, Song for the Dead, The Sky Is Fallin', Six Shooter, Hangin' Tree, Go with the Flow, Gonna Leave You, Do It Again, God Is In the Radio, Another Love Song, Song for the Deaf, Mosquito Song"),    
    ("An Introduction to The Moody Blues", 1960, "The Moody Blues", "Go Now, I'll Go Crazy, Something You Got, Can't Nobody Love You, I Don't Mind, Stop, It Ain't Necessarily So, Bye Bye Bird, Steal Your Heart Away, Lose Your Money (But Don't Lose Your Mind), I Don't Want to Go on Without You, Time Is on My Side, From the Bottom of My Heart (I Love You), Everyday, This Is My House (But Nobody Calls), Life's Not Life, Boulevard De La Madelaine, People Gotta Go"),    
    ("Kill Em All", 1983, "Metallica", "Hit the Lights, The Four Horsemen, Motorbreath, Jump In The Fire, (Anesthesia) - Pulling Teeth, Whiplash, Phantom Lord, No Remorse, Seek and Destroy, Metal Militia"),
    ("Led Zeppelin II", 1969, "Led Zeppelin", "Whole Lotta Love, What Is and What Should Never Be, The Lemon Song, Thank You, Heartbreaker, Living Loving Maid (She's Just a Woman), Ramble On, Moby Dick, Bring It On Home")  
;

DROP TABLE IF EXISTS users;

CREATE TABLE users 
(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR NOT NULL,
    name VARCHAR NOT NULL

);

DROP TABLE IF EXISTS userdata;

CREATE TABLE userdata
(
    name VARCHAR PRIMARY KEY,
    albums VARCHAR NOT NULL

);

