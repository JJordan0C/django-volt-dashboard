import re

_RE_STRIP_WHITESPACE = re.compile(r"(?a:^\s+|\s+$)")

top = {
    9: '''
        Internazionali Di Club - UEFA Champions League
        ,Internazionali Di Club - Europa League
        ,Internazionali Di Club - Conference League
        ,Italia - Serie A
        ,Italia - Serie B
        ,Italia - Serie C - Girone A
        ,Italia - Serie C - Girone B
        ,Italia - Serie C - Girone C
        ,Italia - Serie D
        ,Inghilterra - Premier League
        ,Inghilterra - Championship
        ,Inghilterra - League One
        ,Inghilterra - League Two
        ,Spagna - Liga
        ,Spagna - Liga Adelante
        ,Germania - Bundesliga
        ,Germania - Bundesliga 2
        ,Francia - Ligue 1
        ,Francia - Ligue 2
        ,Olanda - Eredivisie
        ,Belgio - Pro League
        ,Portogallo - Primeira Liga
        ,Svizzera - Super League
        ,Svizzera - Challenge League
        ,Danimarca - 1st Division
        ,Austria - Bundesliga
        ,Polonia - 1. Liga
        ,Repubblica Ceca - 1.Liga
        ,Romania - Liga I
        ,Scozia - Premiership
        ,Algeria - Ligue 1
        ,Algeria - Ligue 2
        ,Arabia Saudita - Premier League
        ,Argentina - Campeonato De Riserva De Primera Division
        ,Argentina - Primera B Nacional
        ,Argentina - Primera C 
        ,Argentina - Primera Division
        ,Argentina - Torneo Federal
        ,Armenia - Premier League
        ,Australia - A-League
        ,Australia - FFA Cup
        ,Australia - NPL Capital Football
        ,Austria - Bundesliga Femminile
        ,Austria - Erste Liga
        ,Austria - Regionalliga Centre
        ,Austria - Regionalliga East
        ,Austria - Regionalliga Salzburg
        ,Austria - Regionalliga Tirol
        ,Azerbaijan - Premier League
        ,Belgio - Tweede Klasse
        ,Bielorussia - Premier League
        ,Bolivia - Liga de Futbol Prof
        ,Bosnia - Premier League
        ,Brasile - Serie A
        ,Brasile - Serie B
        ,Brasile - Serie C
        ,Bulgaria - Premier League
        ,Bulgaria - Second Professional League
        ,Canada - Soccer League
        ,Cile - Primera B
        ,Cile - Primera Division
        ,Cina - Super League
        ,Cipro - 1. Divisione
        ,Cipro - 2. Divisione
        ,Colombia - Primera A
        ,Colombia - Torneo Aguila
        ,Corea del Sud - FA Cup
        ,Corea del Sud - K League Challenge
        ,Corea del Sud - K League Classic
        ,Corea del Sud - K3 League
        ,Costa d'Avorio - Ligue 1
        ,Costa Rica - Primera Division
        ,Croazia - 1.HNL
        ,Croazia - 2.HNL
        ,Danimarca - 2nd Division
        ,Danimarca - 3rd Division
        ,Danimarca - Danmarksserien
        ,Danimarca - Elitedivisionen Femminile
        ,Danimarca - Superligaen
        ,Ecuador - Serie A
        ,Estonia - Esiliiga
        ,Estonia - Meistriliiga
        ,Etiopia - Premier League
        ,Finlandia - Kakkonen
        ,Finlandia - Naisten Liga
        ,Finlandia - Veikkausliiga
        ,Finlandia - Ykkonen
        ,Francia - Division 1 Femminile
        ,Francia - National
        ,Galles - Championship North
        ,Galles - Championship South
        ,Galles - Premier League
        ,Georgia - Umaglesi Liga
        ,Germania - Bremen-Liga
        ,Germania - Bundesliga 3
        ,Germania - Bundesliga Femminile
        ,Germania - Hessenliga
        ,Germania - Oberliga Baden Wuerttemberg
        ,Germania - Oberliga Hamburg
        ,Germania - Oberliga Mittelrhein
        ,Germania - Oberliga Niederrhein
        ,Germania - Oberliga Niedersachsen
        ,Germania - Oberliga NOFV North
        ,Germania - Oberliga Rheinland Pfalz Saar
        ,Germania - Regionalliga Bavaria
        ,Germania - Regionalliga North
        ,Germania - Regionalliga Northeast
        ,Germania - Regionalliga Southwest
        ,Germania - Regionalliga West
        ,Germania - Schleswig Holstein Liga
        ,Giappone - Coppa dell'Imperatore
        ,Giappone - J1 League
        ,Giappone - J2 League
        ,Giappone - J3 League
        ,Giappone - Nadeshiko League Div.1 (D)
        ,Gibilterra - Premier Division
        ,Giordania - Premier League
        ,Grecia - Super League
        ,Guatemala - Liga Nacional
        ,Honduras - Liga Nacional
        ,Indonesia - Liga 1
        ,Inghilterra - Conference National
        ,Inghilterra - Conference North
        ,Inghilterra - Conference South
        ,Inghilterra - FA Cup - Qualificazioni
        ,Inghilterra - Isthmian League
        ,Inghilterra - Northern League
        ,Inghilterra - Premier League 2
        ,Inghilterra - Premier League 2 Div 2
        ,Inghilterra - Professional Development League
        ,Inghilterra - Southern League
        ,Internazionali Di Club - Copa Sudamerica
        ,Irlanda - First Division
        ,Irlanda - Premier League
        ,Islanda - Urvalsdeild
        ,Israele - National League
        ,Israele - Premier League
        ,Italia - Campionato Primavera 2
        ,Italia - Serie A Femminile
        ,Kazakistan - Pervaya Liga
        ,Libano - Premier League
        ,Lituania - A Lyga
        ,Lituania - I Lyga
        ,Malesia - Premier League
        ,Malta - Premier League
        ,Marocco - GNEF1
        ,Messico - Campionato U20
        ,Messico - Liga de Expansión MX
        ,Messico - Liga Mx Femminile
        ,Messico - Primera Division
        ,Norvegia - 2. Division, avd 1
        ,Norvegia - 2. Division, avd 2
        ,Norvegia - 3rd Division, Group 1
        ,Norvegia - 3rd Division, Group 2
        ,Norvegia - 3rd Division, Group 3
        ,Norvegia - 3rd Division, Group 4
        ,Norvegia - 3rd Division, Group 5
        ,Norvegia - 3rd Division, Group 6
        ,Norvegia - Eliteserien
        ,Norvegia - OBOS-ligaen
        ,Nuova Zelanda - Premiership
        ,Olanda - Eerste Divisie
        ,Olanda - Eredivisie Femminile
        ,Olanda - Tweede Divisie
        ,Palestina - West Bank League
        ,Panama - Liga
        ,Paraguay - Primera Division
        ,Paraguay - Segunda Division
        ,Peru - Primera Division
        ,Polonia - 2. Liga
        ,Polonia - 3. Liga
        ,Polonia - Ekstraklasa
        ,Portogallo - Segunda Liga
        ,Repubblica Ceca - 1.Liga Femminile
        ,Repubblica Ceca - 2.Liga
        ,Repubblica Ceca - 3.Liga
        ,Repubblica Ceca - U19 League
        ,Romania - Liga 2
        ,San Marino - Campionato Sammarinese
        ,Scozia - Championship
        ,Scozia - League 1 
        ,Scozia - League 2
        ,Serbia - Superliga 
        ,Singapore - S.League
        ,Slovacchia - 2.Liga
        ,Slovacchia - Fortuna Liga
        ,Slovenia - 2. SNL
        ,Slovenia - Prva Liga
        ,Spagna - Primera RFEF Gruppo I
        ,Spagna - Primera RFEF Gruppo II
        ,Spagna - Segunda RFEF Gruppo I
        ,Spagna - Segunda RFEF Gruppo II
        ,Spagna - Segunda RFEF Gruppo III
        ,Spagna - Segunda RFEF Gruppo V
        ,Spagna - Tercera Division
        ,Sudafrica - 1st Division
        ,Svezia - 1. Division Norra
        ,Svezia - 1. Division Sodra
        ,Svezia - 2. Division
        ,Svezia - Allsvenskan
        ,Svezia - Superettan
        ,Tanzania - Premier League
        ,Thailandia - League 2
        ,Thailandia - Premier League
        ,Tunisia - Ligue Professionnelle
        ,Turchia - Super Lig
        ,Turchia - TFF First League
        ,Ucraina - Premier League
        ,Uganda - Premier League
        ,Ungheria - Merkantil Bank Liga
        ,Ungheria - OTP Bank Liga
        ,Uruguay - Primera Division
        ,USA - MLS
        ,USA - NWSL Femminile
        ,USA - USL
        ,Uzbekistan - PFL
        ,Vietnam - V.League 1
        '''
}
for dealer_id, t in top.items():
    top[dealer_id] = [_RE_STRIP_WHITESPACE.sub("", x) for x in t.replace('\n', '').split(',')]
