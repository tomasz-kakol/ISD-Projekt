# Inteligentne Systemy Decyzyjne - Praktyka nowoczesnego matematyka: Projekt

## Opis projektu

Zakładamy, że znajdujemy się w pozycji osoby zarządzającej hotelem. Głównym celem jest implementacja odpowiedniego algorytmu (bądź algorytmów), który przy panujacych warunkach rynkowych (strukturze klientów) będzie maksymalizował zysk poprzez odpowiednią wycenę pokoi hotelowych. Poza wyznaczeniem odpowiedniego algorytmu, dodatkowe zadania to: implementacja serwera hotelowego umożliwającego komunikację między agencją bookingową, a zarządanym hotelem oraz implementacja trzech person klientów, tj. algorytmów symulujących realistyczne zachowania zakupowe.

## Skład grupy:

- Barbara Chłódek
- Kacper Olczak
- Tomasz Kąkol
- Aleksander Żurowski

# Projekt

## Opis systemu komunikacji i instrukcja uruchomienia

(Wersja z 14/04/2026, do ewentualnych zmian w przyszłości, póki co skrypty umożliwiające komunikację zawierają również prymitywny algorytm wysyłania zapytań i generowania na nie odpowiedzi)

System komunikacji odbywa się za pomocą skryptów napisanych w języku Python z wykorzystaniem funkcji z modułu *Flask*. Użytkownik odpowiadający za serwer hotelowy uruchamia na swoim komputerze skrypt *hotel_server.py* - skutkuje to postawieniem serwera, który nasłuchuje zapytań (w formacie JSON) od innych użytkowników. Drugi użytkownik, odpowiadający za agencję, uruchamia na swoim komputerze skrypt *agency_client.py* uzupełniając w odpowiednim miejscu adres IP serwera hotelowego (oznaczone komentarzem w niniejszym skrypcie). Obecna implementacja agencji przesyła serię zapytań do hotelu oraz podejmuje decyzję (póki co niebędącą wynikiem żadnego wyszukanego algorytmu) w odniesieniu do odpowiedzi hotelu.

## Opis person klientów

(opis klientów, tu uzupełnimy jak już coś wrzucimy :> )

