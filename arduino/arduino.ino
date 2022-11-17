#include <EEPROM.h>
#include <ESP8266WiFi.h>
#define RED_LED 13
#define BLUE_LED 14
#define GREEN_LED 12
bool running = false;

void RED() {
  digitalWrite(RED_LED, HIGH); 
}
void BLUE() {
  digitalWrite(BLUE_LED, HIGH); 
}
void ORANGE() {
  digitalWrite(RED_LED, HIGH); 
  analogWrite(GREEN_LED, 64);
}
void GREEN() {
  digitalWrite(GREEN_LED, HIGH); 
}
void OFF() {
  digitalWrite(RED_LED, LOW); 
  digitalWrite(BLUE_LED, LOW); 
  digitalWrite(GREEN_LED, LOW);
}
const char* ssid = "jgage_netgear";
const char* password = "melodicboat789";

; // 
WiFiServer server(8787);
 
void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(RED_LED, OUTPUT);
  pinMode(BLUE_LED, OUTPUT);
  pinMode(GREEN_LED, OUTPUT);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
 
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request

  if (request.indexOf("/RED") > 0)  {
    OFF();
    RED();
  }
  if (request.indexOf("/ORANGE") >0)  {
    OFF();
    ORANGE();
  }
  if (request.indexOf("/GREEN") > 0)  {
    OFF();
    GREEN();
  }
  if (request.indexOf("/OFF") > 0)  {
    OFF();
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("Led pin is set");
  client.println("<br><br>");
  client.println("<a href=\"/LED=ON\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/LED=OFF\"\"><button>Turn Off </button></a><br />");  
  client.println("</html>");
 }