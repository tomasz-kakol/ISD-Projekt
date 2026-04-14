# Inteligentne Systemy Decyzyjne - Praktyka nowoczesnego matematyka: Projekt

## Opis projektu

Zakładamy, że znajdujemy się w pozycji osoby zarządzającej hotelem. Głównym celem jest implementacja odpowiedniego algorytmu (bądź algorytmów), który przy panujacych warunkach rynkowych (strukturze klientów) będzie maksymalizował zysk poprzez odpowiednią wycenę pokoi hotelowych. Poza wyznaczeniem odpowiedniego algorytmu, dodatkowe zadania to: implementacja serwera hotelowego umożliwającego komunikację między agencją bookingową, a zarządanym hotelem oraz implementacja trzech person klientów, tj. algorytmów symulujących realistyczne zachowania zakupowe.

## Skład grupy i podział pracy

Skład grupy:
- Barbara Chłódek
- Kacper Olczak
- Tomasz Kąkol
- Aleksander Żurowski

Podział pracy z okresu od początku projektu do 14/04/2026: wspólna organizacja pracy oraz przedyskutowanie projektu; wstępna implementacja systemu komunikacji (Kacper, Basia); weryfikacja systemu komunikacji między osobnymi urządzeniami (Tomek); wspólna dyskusja nad specyfikacją person klientów (Aleksander, Kacper, Tomek); implementacja person klientów i systemu agencyjnego (Kacper).

Plan pracy na przyszłe tygodnie: wstępny szkielet i początkowe części raportu; ewentualne rozszerzenie person klientów (w szczególności logika akceptacji ofert i generowania zapytań); implementacja algorytmów uczenia maszynowego dokonujących odpowiedniej wyceny pokoi w zależności od szczegółów zapytania.

# Projekt

## Opis systemu komunikacji i instrukcja uruchomienia

(Wersja z 14/04/2026, do ewentualnych zmian w przyszłości, póki co skrypty umożliwiające komunikację zawierają również prymitywny algorytm wysyłania zapytań i generowania na nie odpowiedzi)

System komunikacji odbywa się za pomocą skryptów napisanych w języku Python z wykorzystaniem funkcji z modułu *Flask* (i kilku pobocznych: *random*, *time*, *abc*, *requests*, *uuid*). Użytkownik odpowiadający za serwer hotelowy uruchamia na swoim komputerze skrypt *hotel_server.py* - skutkuje to postawieniem serwera, który nasłuchuje zapytań (w formacie JSON) od innych użytkowników. Drugi użytkownik, odpowiadający za agencję, uruchamia na swoim komputerze skrypt *agency_with_clients.py* uzupełniając w odpowiednim miejscu (oznaczonym komentarzem w niniejszym skrypcie) adres IP serwera hotelowego. Obecna implementacja agencji automatycznie przesyła serię zapytań (zależnych od persony klienta) do hotelu oraz przekazuje odpowiedź hotelu do klienta, który podejmuje decyzję o akceptacji/odrzuceniu oferty zgodnie ze swoim typem persony. Cały proces wymiany zapytań oraz odpowiedzi jest wyświetlany w terminalu w taki sposób, aby użytkownik mógł w czasie rzeczywistym obserwować proces rezerwacji.

## Opis person klientów

(Wersja z 14/04/2026, do ewentualnych zmian w przyszłości)

Obecna implementacja systemu agencyjnego zawiera 3 persony klientów:

- **LastMinutePersona**
- **WeekendPremiumPersona**
- **RareLongStaySuitePersona**

Charakterystyka klasy **LastMinutePersona**:

Typowy klient *last-minute* - rezerwuje pobyt 1-3 dniowy na 1-3 dni do przodu, ma niski/średni budżet. Akceptuje ofertę, jeśli cena pokoju znajduje się w przedziale akceptowanych przez niego cen (przedział o początku w zerze i górnej granicy będącej liczbą losową z przedziału [400, 600]). W przypadku kilku ofert z różnych hoteli akceptuje ofertę z najniższą ceną. Generuje 0-2 zapytań dziennie.

Charakterystyka klasy **WeekendPremiumPersona**:

Klient z wysoką akceptacją ceny - najczęściej celuje aby początkowym dniem rezerwacji był piątek lub sobota, rzadziej wybiera dni robocze; pobyt zawsze na 7 dni. Ma wysoki budżet. Logika decyzyjna co do wyboru oferty jest analogiczna jak w przypadku klasy **LastMinutePersona**, ze zmianą w przedziale akceptowalnych cen, tj.: klient akceptuje ofertę, jeśli cena pokoju znajduje się w przedziale akceptowanych przez niego cen (przedział o początku w zerze i górnej granicy będącej liczbą losową z przedziału [1000, 1200]). W przypadku kilku ofert z różnych hoteli akceptuje ofertę z najniższą ceną. Generuje 0-2 zapytań dziennie.

Charakterystyka klasy **RareLongStaySuitePersona**:

Rzadki klient - 50% szans generowania zapytania w danym dniu, jeśli wysyła zapytanie to tylko jedno. Zawsze bierze *suite* i zawsze pobyt na 3 tygodnie (21 dni); ma wysoki budżet. Akceptuje ofertę, jeśli cena pokoju znajduje się w przedziale akceptowanych przez niego cen (przedział o początku w zerze i górnej granicy będącej liczbą losową z przedziału [1000, 1200]). W przypadku kilku ofert z różnych hoteli faworyzuje hotele w których już był (zmienna kontekstowa *returning_client*).

Plan na potencjalne zmiany w przyszłości: uwzględnienie zmiennych kontekstowych (*city*, *device* i *retuning_client*) w metodach generowania zapytań przez klasy klientów; zmiana logiki akceptacji ofert przez każdą z klas klientów na taką, która korzysta z pewnych rozkładów prawdopodobieństwa (obecnie, jeśli cena znajduje się w przedziale cen akceptowanych klient akceptuje ofertę - bez znaczenia czy cena jest bliska dolnej czy górnej granicy owego przedziału - jedną z naturalnych metod rozszerzenia tej logiki jest zadanie pewnego rozkładu prawdopodobieństwa na tym przedziale).








