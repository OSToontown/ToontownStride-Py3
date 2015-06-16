class SequenceList:

    def __init__(self):
        self.list = {}
        for line in sequences.split('\n'):
            if line is '':
                continue
            split = line.split(':')
            self.list[split[0].lower()] = [word.rstrip('\r\n').lower() for word in split[1].split(',')]

    def getList(self, word):
        if word in self.list:
            return self.list[word]
        else:
            return []

sequences = '''
$:exe,kk zzz,k zzz,ex,hit,hits,hole,whole,ole,ooo le,holes
'n:i gg,i grow,i gross,i grr,i grrr,i gah
's:exe,kk zzz,k zzz,ex,hit,hits,u kk,uk
.:,Y .
42:0
4:20,2 0,twenty,chan,twin tea,twin ty
69:ed,ing
8:=,-
<:=,-
=:8,=,-
a,ah,ahh,ahhh,ahhhhh,ahhhhhh:zzz,sees,$,'s
ace,as,ash,ask,asp,ashton:hole,whole,ole,ooo le,holes,zzz,'s
ack:ools
ai,ay,ayy,ayyy,ayyyy:ds
al:coco ol,cool,a ack bar,ah ack bar,ah ache bar,ah snack bar
all:a ack bar,ah ack bar,ah ache bar,ah snack bar
an:a hon,a honda,a con,a cone,ail,ails,ailed,ailing,al,ale,ales,all,awl,us,u.s.,u.s.a.,u si,usa,use,used,using,uses,uss
ann:a hon,a honda,a con,a cone,al,ails,ailed,ailing,ale,ales,all,awl,us,u.s.,u.s.a.,u si,usa,use,used,using,uses,uss
anna:hon,honda,con da,con duh,cone da,cone duh
anne:a hon,a honda,a con,a cone,al,us,u.s.,u.s.a.,u si,usa,use,used,using,uses,uss
ape's:me,you,him,his,their,him,them,your,yourself,ur self
ape:me,you,him,his,their,him,them,your,yourself,ur self
apes:me,you,him,his,their,him,them,your,yourself,ur self
ate:me out,you out,u out,her out
ball:it more
ban:gg
bangs:me,her,him,it,them
bass:hole,whole,ole,stir,stir ed,stair,stair ed,tar,star,stared,tt a r ed,holes
bat:star,stair,stair ed,star,stared
bay:be maker
be,bee,bo,boo:ach,i tea see ache,i tee see ache,i tea sea ache,i tee sea ache,eye tea see ache,eye tee see ache,eye tea sea ache,eye tee sea ache,itches,itch,jay,jays,job,jobs,etch,cheese,itching,each,shh,shhh,shhhh,shhhhhh,it cha,cha,ache
beast:tea al i tea,tea al i ty,tea al i tie
ben:dover,dove err,doves err
bend:over
bet:ouch
big:deck,decks,dock,docks,clock,clocks,cook,cooks
bit,bite:cha,chi,chez,chin,chine,china,chose,chow,chess,itch,itches,ach,cheese,cheddar,shh,shhh,shhhh,shhhhhh
bla:zz it,zzz it,k tar,kk tar
black:tar,k tar,kk tar
blew:job,jobs
bloat:job,jobs
bloo:job,jobs
blowfish:job,jobs
blowy:job,jobs
blue:waffle,job,jobs
bob:zzz,zz
bon:r,or,err,errs,me,him,it,ro,her
bone:r,or,err,errs,me,him,it,ro,her
boo:be,bee,bees,by,ty,bye,byes,tay,tea
boot:bee,bees,ty,y
bos:ton
bow:job,jobs
brass:hole,whole,ole,ooo le,holes
bull:sheep,sheeps,ship,shift
bulls:hit,sheep,sheeps,ship,shift
burn:in hello
but:hole,whole,plug,plugs,sec,toll,head,face
by:itch,itches
cam:bucket,buckets,dumpster,girl,girls,on me,tastes
came:bucket,buckets,dumpster,on me,tastes,in you,in u
cee:man,men,min,mins,moon,ex,a tt le,xii,exe,kk zzz
chic:a go,ago
chin:kk
class:hole,whole,ole
climb:max,maxed,maxes,maxing
climbed:max,maxed,maxes,maxing
climbs:max,maxed,maxes,maxing
clue:luxe,lucks
coca:in,ing
cog:awk
come:bucket,buckets,dumpster,on me,tastes
comes:bucket,buckets,dumpster,on me,tastes
con:dim,dims,dome,domes,dooms,doom,do hm,do hmm,do hmmm,do mm
concentration:camp
coop:kk
cop:kk
corn:oh graphic,ooo,hoo
cunning:link us,link is
curry:man cher,men cher,min cher,moon cher
da:am,mm,yum
dab:itch,itches
dah:am,yum
dat:as,ask,asp,asset,ashton
day:um,yum
dee:bag,kay,k
di:i do,ill do,ill does,kk,ill dot,i'll do,i'll dot,i'll does,ik,i
dill:doe,do,dot,does
ding:us,usa,uss,u.s.a.
dip:stick
dirt:y,ye,eh
docs:me,you,him,his,their,him,them,your
dot:come
dr:ugh,un kk
duck,luck,buck:err,error,errors,my life,everyone,me,ing,yourself,your self,ur self
ducked:your,ur,his,her,you
due:shh,shhh,shhhh,shhhhhh
dug:rugs
dumbo:as,ash,ask,asp
eat:me out,you out,u out,her out
eating:me out,you out,u out,her out
eats:me out,you out,u out,her out
eh:bo la,bowl a,rekt ion,rekt ions,wrekt ion,wrekt ions
el:mayo
ex:tube,tubes,at,cream mint
f.a.q.:ed,err,error,errors,ear,ears,you,ate,eat,gate,goat,got,ing,this,my life,everyone,me,off,king
face:book
fad:gg ate,gg eat,gate,get,it,goat,git
fads:gg ate,gg eat,eat,gate,get,it,goat,git
fake:king,k ing,k eng,kk ing,kk eng,off
family,dad,sister,brother,mom:dead,deads
far:kk,king,k ing,k eng,kk ing,kk eng
fat:as,asset,tas
faye:get,git,got
few:ack or,hack or,kk,king,ok,k ing,k eng,kk ing,kk eng
fill:my kitty,your kitty,her kitty,his kitty,their kitty,ur kitty
finger,fingers,fin gg err:you,me,her,him,them,us,your,ur,yourself,u
flack:you,king,ing,this,my life,everyone,me,off
flick:you,king,ing,this,my life,everyone,me,off
flock:ed,err,error,errors,ear,ears,you,ate,eat,gate,goat,got,ing,this,my life,everyone,me,off,king,u,you,yourself,ur
flowerpot:head,headed,heading,heads
flowerpots:head,headed,heading,heads
flunk:ing,king,eng,in gg,her,u,you,ur,yourself
foe:kk,king,ok,k ing,k eng,kk ing,kk eng
fog:ate,eat,gate,get,it,goat,got
folk:ed,err,error,errors,ear,ears,you,gate,goat,ing,this,my life,everyone,me,off,king
folks:ed,err,error,errors,ear,ears,you,gate,goat,ing,this,my life,everyone,me,off
for:kk,king,k ing,k eng,kk ing,kk eng,twenty,twin ty,20,twin tea
fork:err,error,errors,ear,ears,you,this,my life,everyone,me,off,king,ing,her,eng,in,u,ur,hair,air
four:chan,twenty,20,2 0,twin ty,twin tea
freaky:in,ing
free:kin,k in,k ing,k eng
fuchsia:err,error,errors,ear,ears,you,this,my life,everyone,me,off
fun:king,k ing,k eng,kk ing,kk eng,luck
gah:ay,yay
gee:mail,ay,yay
gen:it,i tall,i tail,i tails
get:wasted,waste ed,bent,hi,high,higher,highest,lay
gets:wasted,waste ed,hi,high,higher,highest,lay
getting:wasted,waste ed,hi,high,higher,highest,lay
gg:ay,a y,ah y,ayy,aye
girl,girls:1 cup,one cup,on cup,won cup,and a cup,plus a cup
give:me head,me pleasure,a truck
glass,glory:hole,whole,ole,ooo le,holes
go:to hello
got:wasted,waste ed,hi,high,higher,highest,ooo hello
grape:me,you,him,his,their,him,them,your,ed,yourself,ur self
grapes:me,you,him,his,their,him,them,your,ed,yourself,ur self
grass:hole,whole,ole,ooo le,holes
half:baked
hand:job,jobs
hang:your,yourself,ur self,myself,my self,me,you
hate:black people,back people,white people
have:sec,see ex
haved:sec,see ex
having:sec,see ex
he:ill,ii,ell,el
her:as,asp,bowls,bowl's,bows,bock,butted,but,come,pew,period,ah,dee,ash
hill:yourself,your self,ur self,u err self,u r self
his:as,asp,bowls,bowl's,bows,bock,butted,but,come,pew,period,ah,dee,ash
hit's:learn
hit:learn
hits:learn
hm:arr y juan,arr y jane,arr y jan,arr y jam
hmm:arr y juan,arr y jane,arr y jan,arr y jam
hmmm:arr y juan,arr y jane,arr y jan,arr y jam
horn:y,horn eh,knee,ie,i
honk:y,eye
hot:mail,come
hue:jazz
huge:as,mass,ashton,ask,asp,jazz,ash
huger:as,mass,ashton,ask,asp,jazz,ash
i'm:moist,wet,hard
i:es,es bean,es beans,es be an,es be ann,es be anne,es be i an,es be i ann,es be i anne,:c k,=c k,;c k,gg a,gg ah,gg ahh,gg ahhh,gg ahhhhh,gg ha
ice:hole,whole,ole,ooo le
id:i
if:uk
im:moist,wet,hard
in:he'll,the assistant,your mom,your mother,your assistant,ur assistant,ur mom,ur mother,the as,your as,ur as
inst:a gram,ah gram,ahh gram,ahhh gram,ahhhhh gram,ahhhhhh gram
instant:graham,grand
inter:course
jack's:ed,ing,me,myself,her,herself,him,himself,of,off,ourselves,they,themselves,us,you,yourself,u late
jack:ed,ing,me,myself,her,herself,him,himself,off,ourselves,they,themselves,us,you,yourself,u late
jacks:ed,ing,me,myself,her,herself,him,himself,of,off,ourselves,they,themselves,us,you,yourself,u late
jazz:hole,ole,on
kay:kay kay
kin:kk y
kind:kk y
king:kk y
kk:awk,bock,err,ill,ills,kk
knee:gg,grow,gross,grr,grrr,gah,gas,gauss
kneed:gg,grow,gross,grr,grrr,gah,gas,gauss
knit:gah
kun:tt
kyle's:yourself,your self,ur self,u err self,u r self
kyle:yourself,your self,ur self,u err self,u r self
kyles:yourself,your self,ur self,u err self,u r self
lap:dance
last:name
less:be i an,be i ann,be i anne,be an,be ann,be anne,bean,beans
little:sit,hitch,itch
lucks:clan
luxe:clan
ma:stir bait
making,make,makes,made:him hard,love
marry:juan a,juan ha,juan ah,jane,jan,jam
mary:juan a,juan ha,juan ah,jane,jan,jam
mass:hole,whole,ole,ooo le,stir bait
mast:are bait,are baits,are baiter,are bait eng,are bait ed,stir bait
master:bait,baits,baiter,bait eng,bait ed
mastered:bait,baits,baiter,bait eng,bait ed
mastering:bait,baits,baiter,bait eng,bait ed
masters:bait,baits,baiter,bait eng,bait ed
mayor:a juan,ah juan
men:str u ate
mexican:brown
mike:hawk,hawks,hunt,hunts
mm:arr y juan,arr y jane,arr y jan,arr y jam
mo,moe,moo:foe,foes,for,four
moon:shine
mother:flick,flicker,fork,fuchsia,duck,ducking,folk,folks,yuck,flock,heck,truck,funky,flunky,fax,quacker,bucker,bicker,faker,fake,flunk,flunking,tru
my,mah:as,asp,bowls,bowl's,bows,bock,butted,but,come,pew,period,ah,dee,ash,di ik,deck,decks,dock,docks,cook,cooks
nada:zen,zeke,z.z.
nag:zen,zeke,z.z.,grr,grrr,a,ah
nah:zen,zeke,z.z.,gg a,gg ah
nay:kit,grow,growl,gah,gg a,gg ah
neigh,nigh,nik:err,grr,grrr,grrrrrrrl,grow,grove,gurl,girl,gear,gears,gross,ah,a,gah
new:york,fork,folk,forks,folks
not:zen,zeke,z.z.
octopus:y,ye,sea,seas
octopuses:y,ye,sea,seas
of:u kk,uk
oh:rn y
old:are you,r you,are u,r u
omg:egg al
on:your knees,your knee
open:legs,leg
or:gah some,gah sum,gg y,gee
other:flick,flicker,fork,fuchsia,duck,folk,folks,yuck,flock,heck,truck,funky,flunky,fax,quacker,bucker,bicker
pah:key,keys
pant:tease,teas,ties
passed:off
pause:i,eek,eh
pea:nest,mess,pea,pi,pie,do file,knees,nice,niece
peck:err
peep:show
pen:ice,iced,ices,icing,island,eh tray,eh tate,15,is,1s,i zzz,his,1 5
pens:ice,iced,ices,icing,island,eh tray,eh tate,15,is,1s,i zzz,his,1 5
period:cramps
pet:oh pile,oh piles,oh file,oh files
pew:cee,say,says,sea,seas,see,sees,she,shes,she's,si
phony:number,numb err
pi:pi,ssw
piece,peace:of shift,of ship,of shut,of shirt
play:boy
pooh:cee,say,says,sea,seas,see,sees,she,shes,she's,si
pose:eh
pound:ed,ing,me,myself,her,herself,him,himself,of,off,ourselves,they,themselves,us,you,yourself
pounds:ed,ing,me,myself,her,herself,him,himself,of,off,ourselves,they,themselves,us,you,yourself
pour:on,no
pro:st i tut,stick tut
purr:cee,say,says,sea,seas,see,sees,she,shes,she's,si
push:y,ye,cee,say,says,sea,seas,see,sees,she,shes,she's,si
put:cee,say,says,sea,seas,see,sees,she,shes,she's,si
queue:ear
rake:you
rap:me,you,her,his,their,him,them,your,ed,35,yourself,ur self,eh me,ping
ray:ping,pi
re:tar ed,tart,tarts,tar tt ed,tar teed,tar dead,tar deed,tar dee ed,tar dad
read:tube,tubes
red:tube,tubes
reed:tube,tubes
rekt:um,hum,u hmm,huh,u hm,u hmmm
roll:grass,in the hay,in the hey
rub:one off,one of,1 off,1 of,on off,on of
san:francisco
sass:hole,whole,ole
sassy:hole,whole,ole
saw:kk
sc:hum,um,u hmm,huh,u hm,u hmmm
sea,see,sec::man,men,min,mins,moon,ex,a tt le,xii,exe,kk zzz
seem:en,an,man,men,min,ex,a tt le
sell,selling,sold:cracked,cracked-uptick,crackin',cracking,crackle,crackle's,crackles,crackly,herbs
sew:kk
she:it,hitting,its,ex i,mail,mails,mailed,mailing,male,males,tt,i,ii
shh,shhh,shhhh,shhhhhh,shy:it,eat,hit,hits,its,ex i,he mail,he mails,he mailed,he mailing,he male,he males,ii tt,i it,i tt
shut:the duck,the luck
si:u tt,exe,kk zzz,k zzz,ex
ski:it,ii tt
skill:your,yourself,ur self,myself,my self,me,you
sky:pea,peas,peel,pen,pet,pi,pie,peta,pico,pens,pop,hype,ape,pets,peep,per,pell,pa
snap,nap:chat
so:exe,kk zzz,k zzz,ex,kk
sock,socks,shucks:it,on it,my deck,my dock,my doc,ur deck,ur dock,your deck,your dock,his deck,his dock,cooks,cook,my cook,ur cook,your cook,his cook,my cooks,ur cooks,your cooks,his cooks,deck,decks,a dock,a deck,a docks,a decks,a cook,a cooks,my duck,my ducks,dock
sofa:king,kin,keen,kings
some:cricket
son,sun:of a bit,of a peach,of a be,of a bee
st:on ed,rip
stone:ed
stu:pit,pod
stuck:my duck,my dock,my deck,ing
sue:kk,lute,lutes
sugar:daddy
tah:tas,tah
tea:bag,bagged,bagging,bags
test:i cools,i cool,tickle,tickles
the:di,hello,flunk
tho:tt,tea,tee,ty
to:he'll,bangs
too:he'll,bangs
truck:eh ru,ing,eng,you,u,up,ed,her,or
tt:its,its,it
two:he'll
uk:you,u
un:tee
under:my skirt,her skirt,your skirt,my dress,her dress,your dress,ur skirt,ur dress
ur:but,bum,as,period,hole,holes
vague:in a,i nah
vern:gen
vet:china
via:grape
wanna:duck,bangs
wat:the hello,the fork,the duck,the freaky,the yuck,your sky,ur sky,the fire truck,the truck,the he'll
we,whee:ed,neigh is,knees
what:the hello,the fork,the duck,the freaky,the yuck,your sky,ur sky,the truck,the fire truck,the he'll
white:power
who:err,errs,re,ree
wrap:me,you,him,them,them
wut:the hello,the fork,the duck,the freaky,the yuck,your sky,ur sky,the truck,the fire truck,the he'll
you:a hole,in me
your:as,but,bum,come,period,hole,holes,ash,sass
yuck:err,error,errors,my life,me,ing,you,dee
zone:tan
zzz:3 ex,33 ex,ex,ugh eng,hole,holes
'''
