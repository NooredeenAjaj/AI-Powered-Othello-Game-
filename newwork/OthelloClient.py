import socket
import sys


class OthelloClient:
    def __init__(self, server_host, server_port, idstring, color_choice=None):
        """
        :param server_host: T.ex. "vm33.cs.lth.se"
        :param server_port: 9035 (test), 9045 (utvärdering)
        :param idstring: Ditt ID som servern känner igen
        :param color_choice: 'd' (dark) eller 'w' (white) i testläge (port 9035).
        """
        self.server_host = server_host
        self.server_port = server_port
        self.idstring = idstring
        self.color_choice = color_choice  # Relevant endast i testläge (port 9035)
        self.my_color = None
        self.opponent_color = None

    def run(self):
        """Huvudloop för att ansluta till servern och spela spelet."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"Ansluter till {self.server_host}:{self.server_port}...")
                s.connect((self.server_host, self.server_port))
                print("Anslutning lyckades!")
                self._handle_server_interaction(s)
        except Exception as e:
            print(f"Fel uppstod: {e}")
            sys.exit(1)

    def _handle_server_interaction(self, s):
        """Hantera serverns kommunikation steg för steg enligt protokollet."""
        print("Server:", self._read_line(s))  # "Hi! I am your othello server."
        print("Server:", self._read_line(s))  # "What is your name?"

        # Skicka ID
        self._send_line(s, self.idstring)

        # Läs serverinformation
        for _ in range(3):
            print("Server:", self._read_line(s))

        # Hantera färgval i testläge (port 9035)
        if self.server_port == 9045:
            line = self._read_line(s)
            print("Server:", line)  # "choose colour, 'd' for dark, 'w' for white."
            self._send_line(s, self.color_choice if self.color_choice else "d")

        # Få bekräftelse om vald färg
        line = self._read_line(s)
        print("Server:", line)
        if "dark" in line:
            self.my_color, self.opponent_color = "black", "white"
        elif "white" in line:
            self.my_color, self.opponent_color = "white", "black"
        else:
            print("Server:", self._read_line(s))  # Hantera eventuella fel
            return

        # Om vi är vit börjar motståndaren
        if self.my_color == "white":
            self._handle_opponent_move(s)

        # Spelloopen
        while True:
            line = self._read_line(s)
            if not line:
                break
            print("Server:", line)

            if "your move" in line:
                self._handle_my_move(s)
            elif "opponent's move" in line:
                self._handle_opponent_move(s)
            elif "The game is finished" in line:
                self._handle_game_end(s)
                break
            elif "error" in line:
                print("Server:", self._read_line(s))
                break

    def _handle_my_move(self, s):
        """Hantera spelarens drag."""
        print("Din tur! Ange ditt drag (t.ex. 'd3') eller 'PASS':")
        move = input("> ").strip()
        self._send_line(s, move)

    def _handle_opponent_move(self, s):
        """Hantera motståndarens drag."""
        move = self._read_line(s).strip()
        print(f"Motståndaren spelade: {move}")

    def _handle_game_end(self, s):
        """Hanterar spelets avslutningsmeddelanden."""
        print("Server:", self._read_line(s))  # White: #
        print("Server:", self._read_line(s))  # Dark: #
        print("Server:", self._read_line(s))  # White won / Dark won / Draw

    def _read_line(self, sock):
        """Läser en rad från servern."""
        data = b""
        while True:
            chunk = sock.recv(1)
            if not chunk:
                return None
            data += chunk
            if data.endswith(b"\n"):
                return data.decode("utf-8").strip()

    def _send_line(self, sock, text):
        """Skickar en rad till servern."""
        print("Client:", text)
        sock.sendall((text + "\n").encode("utf-8"))


if __name__ == "__main__":
    # Byt ut idstring med ditt tilldelade ID.
    client = OthelloClient(
        server_host="vm33.cs.lth.se",
        server_port=9035,  # 9035 = testläge, 9045 = utvärdering
        idstring="your_unique_id",  # Ersätt med ditt riktiga ID
        color_choice="d",  # Välj 'd' för dark eller 'w' för white (endast testläge)
    )
    client.run()
