# For windows geometry and elements radius
from typing import ClassVar, final


@final
class Geometry:
    MAIN = (1200, 1000)
    HELP = (500, 500)
    # INFO = (500, 200)
    CORNER_RADIUS = 20
    MONITORS = 2


# Colors class for different elements in UI
@final
class Colors:
    TEXTBOX = "#333333"
    BORDER_TEXTBOX = "#B2B2B2"
    ANSWER_BACKGROUND = "#191970"
    ANSWER_TEXT = "#F0E68C"
    BUTTON = "#4169E1"
    BUTTON_HOVER = "#4B0082"
    SETTINGS_BG = "#303030"
    SETTINGS_SEGMENTED_BG = "#4C4C4C"
    SETTINGS_SELECTED_BUTTON = "#191970"
    BORDER_SETTINGS = "#C0C0C0"
    IMAGE_FRAME = "#555555"


@final
class AlertsColors:
    SUCCESS: ClassVar[dict[str, str]] = {"bg": "#d4edda", "text": "#2d693a"}
    DANGER: ClassVar[dict[str, str]] = {"bg": "#f8d7da", "text": "#82323a"}
    INFO: ClassVar[dict[str, str]] = {"bg": "#cce5ff", "text": "#225b99"}


# Fonts class for different elements in UI
@final
class Fonts:
    NORMAL = "Quicksand Medium"
    NORMAL_SIZE = 14
    TITLE = "Special Elite"
    TITLE_SIZE = 36
    ANSWER = "URW Gothic"
    ANSWER_SIZE = 20


# Longer texts:
# Prompt for AI to generate great response in a specific format
PROMPT_EXPLANATION = """
Jesteś specjalistą w dziedzinie informatyki i właśnie otrzymałeś pytanie, na które musisz podać poprawną odpowiedź z podanych opcji. Przed odpowiedzią dokładnie przeanalizuj pytanie i zwróć uwagę, o co pytają autorzy.
Napisz poprawną odpowiedź na to pytanie, wyjaśnij dlaczego wybrałeś tę opcję oraz opisz pozostałe pojęcia, które miałeś do wyboru, z odniesieniem do tematu pytania.
Format twojej wypowiedzi ma być podzielony za pomocą nagłowków, paragrafów i list. Uwzględnij następujące nagłówki: "Poprawna odpowiedź", "Wyjaśnienie wybranej opcji", "Pozostałe odpowiedzi".
Przykład:
"
Poprawna odpowiedź: Odpowiedź: C

Wyjaśnienie wybranej opcji:
Wybrałem protokół SMTP, ponieważ służy on do wysyłania wiadomości e-mail od klientów na serwer poczty e-mail. Protokół ten działa na porcie 25 i może być również używany do przekazywania wiadomości e-mail ze źródłowego do docelowego serwera poczty e-mail. Protokół SMTP rzeczywiście służy do wysyłania wiadomości e-mail, jest więc poprawną odpowiedzią.

Pozostałe odpowiedzi:
 - Odpowiedź A - protokół POP3 jest używany przez klientów poczty e-mail do pobierania wiadomości z serwera poczty e-mail. Działa on na porcie 110. Protokól ten dotyczy więc poczty e-mail, ale ma przeciwne działanie niż wysyłanie e-maili, a mianowicie ich odbieranie.
- Odpowiedź B - DNS to protokół służący do tłumaczenia nazw domenowych (np. www.example.com) na adresy IP. Używa UDP do żądań i transferu informacji między serwerami DNS. W razie potrzeby do odpowiedzi DNS będzie używał TCP. DNS działa na porcie 53. Protokół DNS ma więc inne działanie niż wysyłanie wiadomości e-mail, nie może być to poprawna odpowiedź.
- Odpowiedź D - SSH służy do zdalnego zarządzania i bezpiecznego dostępu do zdalnych systemów. Udostępnia wiersz poleceń na komputerze zdalnym. Działa na porcie 22 i zapewnia silnie uwierzytelnianie i szyfrowany transport danych między klientem a komputerem zdalnym. Protokół SSH nie jest zatem związany z tematem pytania, gdyż posiada on zupełnie odmienne zastosowanie.
"
Używaj zwięzłego, konkretnego języka, który będzie łatwy do zrozumienia.
"""


HELP_TEXT = """
This program is used to help you solve problems from an IT theory exam (in Polish technical schools you need to pass two such examinations to get technician diploma) to speed up the preparation process. Here are step by step instructions: 
1) First you should paste an image of the question you are having trouble with (you should have your cursor inside the right widget) or import it from your disk. This image should be a screenshot of the IT exam theory question before clicking on the answer.
2) Then you edit the text that was extracted from the screenshot and use it as promt after edit. Or you can just use an image directly.
3) Click the button 'get solution'. The program will communicate with AI and insert explanation to the textbox. That can take a while. After that you can edit this text according to your own preferences.
3) The last step is exporting this solution. You are able to this by clicking on 'Export' tab in settings in the bottom left corner. You can choose to create new file (which is required if you are exporting a solution for the first time) or extend a file previously created with this application. You can save your solution to .odt or .md file. You've got also opportunity to export the solution to anki flashcards. You can do that by choosing the correct deck from the menu.
While creating new file you should insert the proper directory and file name. And in the case of file extending you just need to choose the right file.
You don't have to export your solution of course. You can simply paste your next problem or go back to main menu by clicking on one of the buttons in 'Navigate' tab.
"""
